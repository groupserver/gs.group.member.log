# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013, 2016 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import, unicode_literals, print_function
from zope.cachedescriptors.property import Lazy
from gs.group.base import GroupViewlet
from .log import JoinAndLeaveLog
from . import GSMessageFactory as _


class LogViewlet(GroupViewlet):

    def __init__(self, group, request, view, manager):
        super(LogViewlet, self).__init__(group, request, view, manager)

    @Lazy
    def log(self):
        retval = JoinAndLeaveLog(self.groupInfo)
        return retval


class SummaryViewlet(LogViewlet):

    def __init__(self, group, request, view, manager):
        super(SummaryViewlet, self).__init__(group, request, view, manager)
        self.title = _('summary-title', 'Log')


class DetailViewlet(LogViewlet):

    def __init__(self, group, request, view, manager):
        super(DetailViewlet, self).__init__(group, request, view, manager)
        self.title = _('detail-title', 'Detailed log')
