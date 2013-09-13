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
from datetime import date
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from zope.interface import implements
from Products.CustomUserFolder.userinfo import userInfo_to_anchor
from Products.XWFCore.XWFUtils import munge_date
from gs.group.member.join.audit import SUBSYSTEM as JOIN_SUBSYSTEM
from gs.group.member.leave.audit import SUBSYSTEM as LEAVE_SUBSYSTEM
from .interfaces import IMonthLog, IJoinEvent, ILeaveEvent


class MonthLog(object):
    implements(IMonthLog)
    """ A class that implements the IMonthLog interface, and
        therefore knows all the joining and leaving for
        one particular month
    """

    def __init__(self, groupInfo, year, month, numMembersMonthEnd, events):
        self.groupInfo = groupInfo
        self.year = year
        self.month = month
        self.events = events
        self.numMembersMonthEnd = numMembersMonthEnd
        self.label = date(year, month, 1).strftime('%B %Y')
        self.__numMembersMonthStart = None
        self.__joinEvents = self.__leaveEvents = self.__allEvents = None

    def __nonzero__(self):
        return bool(self.events)

    def __bool__(self):
        return self.__nonzero__()

    @property
    def numMembersMonthStart(self):
        return (self.numMembersMonthEnd -
                self.numMembersJoined +
                self.numMembersLeft)

    @property
    def numMembersJoined(self):
        return len(self.joinEvents)

    @property
    def numMembersLeft(self):
        return len(self.leaveEvents)

    @Lazy
    def joinEvents(self):
        retval = [JoinEvent(self.groupInfo, e)
                    for e in self.events.get(JOIN_SUBSYSTEM, [])]
        return retval

    @Lazy
    def leaveEvents(self):
        retval = [LeaveEvent(self.groupInfo, e)
                    for e in self.events.get(LEAVE_SUBSYSTEM, [])]
        return retval

    @Lazy
    def allEvents(self):
        retval = self.joinEvents + self.leaveEvents
        retval.sort(key=lambda e: e.date, reverse=True)
        return retval


class JoinEvent(object):
    implements(IJoinEvent)

    def __init__(self, groupInfo, eDict):
        self.groupInfo = groupInfo
        self.userInfo = \
          createObject('groupserver.UserFromId',
            self.groupInfo.groupObj, eDict['user_id'])
        self.date = eDict['date']
        self.addingUserInfo = \
          createObject('groupserver.UserFromId',
            self.groupInfo.groupObj, eDict['admin_id'])

    @property
    def xhtml(self):
        cssClass = u'join-event'
        retval = u'<li class="%s">%s joined' % \
          (cssClass, userInfo_to_anchor(self.userInfo))
        if not(self.addingUserInfo.anonymous) and\
          (self.addingUserInfo.id != self.userInfo.id):
            retval = u'%s &#8212; invited by %s' % \
              (retval, userInfo_to_anchor(self.addingUserInfo))
        retval = u'%s (%s)' % \
          (retval, munge_date(self.groupInfo.groupObj, self.date))
        return retval


class LeaveEvent(object):
    implements(ILeaveEvent)

    def __init__(self, groupInfo, eDict):
        self.groupInfo = groupInfo
        self.userInfo = \
          createObject('groupserver.UserFromId',
            self.groupInfo.groupObj, eDict['user_id'])
        self.date = eDict['date']
        self.removingUserInfo = \
          createObject('groupserver.UserFromId',
            self.groupInfo.groupObj, eDict['admin_id'])

    @property
    def xhtml(self):
        cssClass = u'leave-event'
        retval = u'<li class="%s">%s left' % \
          (cssClass, userInfo_to_anchor(self.userInfo))
        if not(self.removingUserInfo.anonymous) and\
          self.removingUserInfo.id != self.userInfo.id:
            retval = u'%s &#8212; removed by %s' % \
              (retval, userInfo_to_anchor(self.removingUserInfo))
        retval = u'%s (%s)</li>' % \
          (retval, munge_date(self.groupInfo.groupObj, self.date))
        return retval
