# coding=utf-8
from datetime import date
from zope.interface import implements
from zope.component import createObject
from Products.XWFCore.XWFUtils import munge_date
from Products.CustomUserFolder.userinfo import userInfo_to_anchor
from gs.group.member.join.audit import SUBSYSTEM as JOIN_SUBSYSTEM
from gs.group.member.leave.audit import SUBSYSTEM as LEAVE_SUBSYSTEM
from gs.group.member.log.interfaces import IMonthLog
from gs.group.member.log.interfaces import IJoinEvent, ILeaveEvent

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
        return (self.numMembersMonthEnd + \
                self.numMembersJoined - \
                self.numMembersLeft)

    @property
    def numMembersJoined(self):
        return len(self.joinEvents)
    
    @property
    def numMembersLeft(self):
        return len(self.leaveEvents)
    
    @property
    def joinEvents(self):
        if self.__joinEvents == None:
            joinEvents = \
              [ JoinEvent(self.groupInfo, e) for e 
                in self.events.get(JOIN_SUBSYSTEM, []) ]
            # If we start displaying join and leave events separately,
            #  we'll need to switch this sorting on.
            #joinEvents.sort(key=lambda e: e.date, reverse=True)
            self.__joinEvents = joinEvents
        return self.__joinEvents

    @property
    def leaveEvents(self):
        if self.__leaveEvents == None:
            leaveEvents = \
              [ LeaveEvent(self.groupInfo, e) for e 
                in self.events.get(LEAVE_SUBSYSTEM, []) ]
            # If we start displaying join and leave events separately,
            #  we'll need to switch this sorting on.
            #leaveEvents.sort(key=lambda e: e.date, reverse=True)
            self.__leaveEvents = leaveEvents
        return self.__leaveEvents

    @property
    def allEvents(self):
        if self.__allEvents == None:
            allEvents = self.joinEvents + self.leaveEvents
            allEvents.sort(key=lambda e: e.date, reverse=True)
            self.__allEvents = allEvents
        return self.__allEvents


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
        retval = u'%s joined' % \
          userInfo_to_anchor(self.userInfo)
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
        retval = u'%s left' % \
          userInfo_to_anchor(self.userInfo)
        if not(self.removingUserInfo.anonymous) and\
          self.removingUserInfo.id != self.userInfo.id:
            retval = u'%s &#8212; removed by %s' % \
              (retval, userInfo_to_anchor(self.removingUserInfo))              
        retval = u'%s (%s)' % \
          (retval, munge_date(self.groupInfo.groupObj, self.date))
        return retval
        
