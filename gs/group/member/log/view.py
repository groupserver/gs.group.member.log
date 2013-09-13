# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import
from zope.cachedescriptors.property import Lazy
from gs.group.base import GroupPage
from .log import JoinAndLeaveLog


class JoinAndLeaveLogView(GroupPage):
    """ The browser view of a group's join and leave log.
    """

    def __init__(self, group, request):
        super(JoinAndLeaveLogView, self).__init__(group, request)
        self.title = 'Join and Leave Log for %s' % self.groupInfo.name

    @Lazy
    def log(self):
        retval = JoinAndLeaveLog(self.groupInfo)
        return retval
