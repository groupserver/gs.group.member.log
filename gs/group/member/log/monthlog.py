# coding=utf-8
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
    
    def __init__(self, groupInfo, events):
        self.groupInfo = groupInfo
        self.events = events

