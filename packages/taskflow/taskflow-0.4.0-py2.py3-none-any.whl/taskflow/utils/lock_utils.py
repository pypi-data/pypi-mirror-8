# Copyright 2011 OpenStack Foundation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

# This is a modified version of what was in oslo-incubator lockutils.py from
# commit 5039a610355e5265fb9fbd1f4023e8160750f32e but this one does not depend
# on oslo.cfg or the very large oslo-incubator oslo logging module (which also
# pulls in oslo.cfg) and is reduced to only what taskflow currently wants to
# use from that code.

import abc
import collections
import contextlib
import errno
import logging
import os
import threading
import time

import six

from taskflow.utils import misc
from taskflow.utils import threading_utils as tu

LOG = logging.getLogger(__name__)


@contextlib.contextmanager
def try_lock(lock):
    """Attempts to acquire a lock, and autoreleases if acquisition occurred."""
    was_locked = lock.acquire(blocking=False)
    try:
        yield was_locked
    finally:
        if was_locked:
            lock.release()


def locked(*args, **kwargs):
    """A locking decorator.

    It will look for a provided attribute (typically a lock or a list
    of locks) on the first argument of the function decorated (typically this
    is the 'self' object) and before executing the decorated function it
    activates the given lock or list of locks as a context manager,
    automatically releasing that lock on exit.

    NOTE(harlowja): if no attribute is provided then by default the attribute
    named '_lock' is looked for in the instance object this decorator is
    attached to.

    NOTE(harlowja): when we get the wrapt module approved we can address the
    correctness of this decorator with regards to classmethods, to keep sanity
    and correctness it is recommended to avoid using this on classmethods, once
    https://review.openstack.org/#/c/94754/ is merged this will be refactored
    and that use-case can be provided in a correct manner.
    """

    def decorator(f):
        attr_name = kwargs.get('lock', '_lock')

        @six.wraps(f)
        def wrapper(self, *args, **kwargs):
            lock = getattr(self, attr_name)
            if isinstance(lock, (tuple, list)):
                lock = MultiLock(locks=list(lock))
            with lock:
                return f(self, *args, **kwargs)

        return wrapper

    # This is needed to handle when the decorator has args or the decorator
    # doesn't have args, python is rather weird here...
    if kwargs or not args:
        return decorator
    else:
        if len(args) == 1:
            return decorator(args[0])
        else:
            return decorator


@six.add_metaclass(abc.ABCMeta)
class _ReaderWriterLockBase(object):
    """Base class for reader/writer lock implementations."""

    @abc.abstractproperty
    def has_pending_writers(self):
        """Returns if there are writers waiting to become the *one* writer."""

    @abc.abstractmethod
    def is_writer(self, check_pending=True):
        """Returns if the caller is the active writer or a pending writer."""

    @abc.abstractproperty
    def owner(self):
        """Returns whether the lock is locked by a writer or reader."""

    @abc.abstractmethod
    def is_reader(self):
        """Returns if the caller is one of the readers."""

    @abc.abstractmethod
    def read_lock(self):
        """Context manager that grants a read lock.

        Will wait until no active or pending writers.

        Raises a RuntimeError if an active or pending writer tries to acquire
        a read lock.
        """

    @abc.abstractmethod
    def write_lock(self):
        """Context manager that grants a write lock.

        Will wait until no active readers. Blocks readers after acquiring.

        Raises a RuntimeError if an active reader attempts to acquire a lock.
        """


class ReaderWriterLock(_ReaderWriterLockBase):
    """A reader/writer lock.

    This lock allows for simultaneous readers to exist but only one writer
    to exist for use-cases where it is useful to have such types of locks.

    Currently a reader can not escalate its read lock to a write lock and
    a writer can not acquire a read lock while it owns or is waiting on
    the write lock.

    In the future these restrictions may be relaxed.
    """
    WRITER = 'w'
    READER = 'r'

    def __init__(self):
        self._writer = None
        self._pending_writers = collections.deque()
        self._readers = collections.deque()
        self._cond = threading.Condition()

    @property
    def has_pending_writers(self):
        self._cond.acquire()
        try:
            return bool(self._pending_writers)
        finally:
            self._cond.release()

    def is_writer(self, check_pending=True):
        self._cond.acquire()
        try:
            me = tu.get_ident()
            if self._writer is not None and self._writer == me:
                return True
            if check_pending:
                return me in self._pending_writers
            else:
                return False
        finally:
            self._cond.release()

    @property
    def owner(self):
        self._cond.acquire()
        try:
            if self._writer is not None:
                return self.WRITER
            if self._readers:
                return self.READER
            return None
        finally:
            self._cond.release()

    def is_reader(self):
        self._cond.acquire()
        try:
            return tu.get_ident() in self._readers
        finally:
            self._cond.release()

    @contextlib.contextmanager
    def read_lock(self):
        me = tu.get_ident()
        if self.is_writer():
            raise RuntimeError("Writer %s can not acquire a read lock"
                               " while holding/waiting for the write lock"
                               % me)
        self._cond.acquire()
        try:
            while True:
                # No active writer; we are good to become a reader.
                if self._writer is None:
                    self._readers.append(me)
                    break
                # An active writer; guess we have to wait.
                self._cond.wait()
        finally:
            self._cond.release()
        try:
            yield self
        finally:
            # I am no longer a reader, remove *one* occurrence of myself.
            # If the current thread acquired two read locks, then it will
            # still have to remove that other read lock; this allows for
            # basic reentrancy to be possible.
            self._cond.acquire()
            try:
                self._readers.remove(me)
                self._cond.notify_all()
            finally:
                self._cond.release()

    @contextlib.contextmanager
    def write_lock(self):
        me = tu.get_ident()
        if self.is_reader():
            raise RuntimeError("Reader %s to writer privilege"
                               " escalation not allowed" % me)
        if self.is_writer(check_pending=False):
            # Already the writer; this allows for basic reentrancy.
            yield self
        else:
            self._cond.acquire()
            try:
                self._pending_writers.append(me)
                while True:
                    # No readers, and no active writer, am I next??
                    if len(self._readers) == 0 and self._writer is None:
                        if self._pending_writers[0] == me:
                            self._writer = self._pending_writers.popleft()
                            break
                    self._cond.wait()
            finally:
                self._cond.release()
            try:
                yield self
            finally:
                self._cond.acquire()
                try:
                    self._writer = None
                    self._cond.notify_all()
                finally:
                    self._cond.release()


class DummyReaderWriterLock(_ReaderWriterLockBase):
    """A dummy reader/writer lock.

    This dummy lock doesn't lock anything but provides the same functions as a
    normal reader/writer lock class and can be useful in unit tests or other
    similar scenarios (do *not* use it if locking is actually required).
    """
    @contextlib.contextmanager
    def write_lock(self):
        yield self

    @contextlib.contextmanager
    def read_lock(self):
        yield self

    @property
    def owner(self):
        return None

    def is_reader(self):
        return False

    def is_writer(self, check_pending=True):
        return False

    @property
    def has_pending_writers(self):
        return False


class MultiLock(object):
    """A class which attempts to obtain & release many locks at once.

    It is typically useful as a context manager around many locks (instead of
    having to nest individual lock context managers).
    """

    def __init__(self, locks):
        assert len(locks) > 0, "Zero locks requested"
        self._locks = locks
        self._locked = [False] * len(locks)

    def __enter__(self):
        self.acquire()

    def acquire(self):

        def is_locked(lock):
            # NOTE(harlowja): reentrant locks (rlock) don't have this
            # attribute, but normal non-reentrant locks do, how odd...
            if hasattr(lock, 'locked'):
                return lock.locked()
            return False

        for i in range(0, len(self._locked)):
            if self._locked[i] or is_locked(self._locks[i]):
                raise threading.ThreadError("Lock %s not previously released"
                                            % (i + 1))
            self._locked[i] = False

        for (i, lock) in enumerate(self._locks):
            self._locked[i] = lock.acquire()

    def __exit__(self, type, value, traceback):
        self.release()

    def release(self):
        for (i, locked) in enumerate(self._locked):
            try:
                if locked:
                    self._locks[i].release()
                    self._locked[i] = False
            except threading.ThreadError:
                LOG.exception("Unable to release lock %s", i + 1)


class _InterProcessLock(object):
    """An interprocess locking implementation.

    This is a lock implementation which allows multiple locks, working around
    issues like bugs.debian.org/cgi-bin/bugreport.cgi?bug=632857 and does
    not require any cleanup. Since the lock is always held on a file
    descriptor rather than outside of the process, the lock gets dropped
    automatically if the process crashes, even if __exit__ is not executed.

    There are no guarantees regarding usage by multiple green threads in a
    single process here. This lock works only between processes.

    Note these locks are released when the descriptor is closed, so it's not
    safe to close the file descriptor while another green thread holds the
    lock. Just opening and closing the lock file can break synchronisation,
    so lock files must be accessed only using this abstraction.
    """

    def __init__(self, name):
        self.lockfile = None
        self.fname = name

    def acquire(self):
        basedir = os.path.dirname(self.fname)

        if not os.path.exists(basedir):
            misc.ensure_tree(basedir)
            LOG.debug('Created lock path: %s', basedir)

        self.lockfile = open(self.fname, 'w')

        while True:
            try:
                # Using non-blocking locks since green threads are not
                # patched to deal with blocking locking calls.
                # Also upon reading the MSDN docs for locking(), it seems
                # to have a laughable 10 attempts "blocking" mechanism.
                self.trylock()
                LOG.debug('Got file lock "%s"', self.fname)
                return True
            except IOError as e:
                if e.errno in (errno.EACCES, errno.EAGAIN):
                    # external locks synchronise things like iptables
                    # updates - give it some time to prevent busy spinning
                    time.sleep(0.01)
                else:
                    raise threading.ThreadError("Unable to acquire lock on"
                                                " `%(filename)s` due to"
                                                " %(exception)s" %
                                                {
                                                    'filename': self.fname,
                                                    'exception': e,
                                                })

    def __enter__(self):
        self.acquire()
        return self

    def release(self):
        try:
            self.unlock()
            self.lockfile.close()
            LOG.debug('Released file lock "%s"', self.fname)
        except IOError:
            LOG.exception("Could not release the acquired lock `%s`",
                          self.fname)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def exists(self):
        return os.path.exists(self.fname)

    def trylock(self):
        raise NotImplementedError()

    def unlock(self):
        raise NotImplementedError()


class _WindowsLock(_InterProcessLock):
    def trylock(self):
        msvcrt.locking(self.lockfile.fileno(), msvcrt.LK_NBLCK, 1)

    def unlock(self):
        msvcrt.locking(self.lockfile.fileno(), msvcrt.LK_UNLCK, 1)


class _PosixLock(_InterProcessLock):
    def trylock(self):
        fcntl.lockf(self.lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def unlock(self):
        fcntl.lockf(self.lockfile, fcntl.LOCK_UN)


if os.name == 'nt':
    import msvcrt
    InterProcessLock = _WindowsLock
else:
    import fcntl
    InterProcessLock = _PosixLock
