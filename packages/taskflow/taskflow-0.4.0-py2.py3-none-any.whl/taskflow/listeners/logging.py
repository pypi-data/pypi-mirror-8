# -*- coding: utf-8 -*-

#    Copyright (C) 2013 Yahoo! Inc. All Rights Reserved.
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

from __future__ import absolute_import

import logging

from taskflow.listeners import base
from taskflow.utils import misc

LOG = logging.getLogger(__name__)


class LoggingListener(base.LoggingBase):
    """Listener that logs notifications it receives.

    It listens for task and flow notifications and writes those
    notifications to provided logger, or logger of its module
    (``taskflow.listeners.logging``) if none provided. Log level
    can also be configured, ``logging.DEBUG`` is used by default.
    """
    def __init__(self, engine,
                 task_listen_for=(misc.Notifier.ANY,),
                 flow_listen_for=(misc.Notifier.ANY,),
                 log=None,
                 level=logging.DEBUG):
        super(LoggingListener, self).__init__(engine,
                                              task_listen_for=task_listen_for,
                                              flow_listen_for=flow_listen_for)
        self._logger = log
        if not self._logger:
            self._logger = LOG
        self._level = level

    def _log(self, message, *args, **kwargs):
        self._logger.log(self._level, message, *args, **kwargs)
