# -*- coding: utf-8 -*-

#    Copyright (C) 2012 Yahoo! Inc. All Rights Reserved.
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

from taskflow import exceptions
from taskflow import flow


class Flow(flow.Flow):
    """Unordered Flow pattern.

    A unordered (potentially nested) flow of *tasks/flows* that can be
    executed in any order as one unit and rolled back as one unit.

    NOTE(harlowja): Since the flow is unordered there can *not* be any
    dependency between task/flow inputs (requirements) and
    task/flow outputs (provided names/values).
    """

    def __init__(self, name, retry=None):
        super(Flow, self).__init__(name, retry)
        # NOTE(imelnikov): A unordered flow is unordered, so we use
        # set instead of list to save children, children so that
        # people using it don't depend on the ordering
        self._children = set()

    def add(self, *items):
        """Adds a given task/tasks/flow/flows to this flow."""
        if not items:
            return self

        # check that items don't provide anything that other
        # part of flow provides or requires
        provides = self.provides
        old_requires = self.requires
        for item in items:
            item_provides = item.provides
            bad_provs = item_provides & old_requires
            if bad_provs:
                raise exceptions.DependencyFailure(
                    "%(item)s provides %(oo)s that are required "
                    "by other item(s) of unordered flow %(flow)s"
                    % dict(item=item.name, flow=self.name,
                           oo=sorted(bad_provs)))
            same_provides = provides & item.provides
            if same_provides:
                raise exceptions.DependencyFailure(
                    "%(item)s provides %(value)s but is already being"
                    " provided by %(flow)s and duplicate producers"
                    " are disallowed"
                    % dict(item=item.name, flow=self.name,
                           value=sorted(same_provides)))
            provides |= item.provides

        # check that items don't require anything other children provides
        if self.retry:
            # NOTE(imelnikov): it is allowed to depend on value provided
            # by retry controller of the flow
            provides -= self.retry.provides
        for item in items:
            bad_reqs = provides & item.requires
            if bad_reqs:
                raise exceptions.DependencyFailure(
                    "%(item)s requires %(oo)s that are provided "
                    "by other item(s) of unordered flow %(flow)s"
                    % dict(item=item.name, flow=self.name,
                           oo=sorted(bad_reqs)))

        self._children.update(items)
        return self

    def __len__(self):
        return len(self._children)

    def __iter__(self):
        for child in self._children:
            yield child

    def iter_links(self):
        # NOTE(imelnikov): children in unordered flow have no dependencies
        # between each other due to invariants retained during construction.
        return iter(())
