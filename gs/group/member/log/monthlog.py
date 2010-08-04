# coding=utf-8
from datetime import date
from zope.interface import implements
from zope.component import createObject
from gs.group.member.join.audit import SUBSYSTEM as JOIN_SUBSYSTEM
from gs.group.member.leave.audit import SUBSYSTEM as LEAVE_SUBSYSTEM
from gs.group.member.log.interfaces import IMonthLog

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
        self.label = date(year, month, 1).strftime('%B %Y')
        self.numMembersMonthEnd = numMembersMonthEnd
        self.events = events
        self.joinedMembers = events.get(JOIN_SUBSYSTEM, [])
        self.numMembersJoined = len(self.joinedMembers)
        self.leftMembers = events.get(LEAVE_SUBSYSTEM, [])
        self.numMembersLeft = len(self.leftMembers)
        self.numMembersMonthStart = \
          (self.numMembersMonthEnd + self.numMembersJoined - self.numMembersLeft) 

    def __nonzero__(self):
        return self.events

    def __bool__(self):
        return self.__nonzero__()
    
