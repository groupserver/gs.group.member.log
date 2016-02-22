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
from datetime import date
from zope.cachedescriptors.property import Lazy
from gs.group.member.base import FullMembers
from .queries import JoinLeaveQuery
from .monthlog import MonthLog


class JoinAndLeaveLog(object):
    """ A log of how many members have joined and left
        over each month.
    """

    def __init__(self, groupInfo):
        self.groupInfo = groupInfo

    @Lazy
    def queries(self):
        retval = JoinLeaveQuery(self.groupInfo.groupObj)
        return retval

    @Lazy
    def events(self):
        retval = self.queries.group_join_leave_events(self.groupInfo.id)
        return retval

    @Lazy
    def years(self):
        retval = []
        if self.events:
            earliestYear = min(self.events.keys())
            latestYear = date.today().year
            retval = range(latestYear, (earliestYear - 1), -1)
        return retval

    @Lazy
    def monthLogs(self):
        """ The logs for each month, over the appropriate timespan.
        """
        retval = []
        numMembersMonthEnd = len(FullMembers(self.groupInfo.groupObj))
        for year in self.years:
            latestMonth = 12
            earliestMonth = 1
            if year == self.years[0]:
                latestMonth = date.today().month
            if year == self.years[-1]:
                earliestMonth = min(self.events[year].keys())
            for month in range(latestMonth, (earliestMonth - 1), -1):
                events = {}
                if (year in self.events) and (month in self.events[year]):
                    events = self.events[year][month]
                monthLog = MonthLog(self.groupInfo, year, month, numMembersMonthEnd, events)
                retval.append(monthLog)
                numMembersMonthEnd = monthLog.numMembersMonthStart
        return retval
