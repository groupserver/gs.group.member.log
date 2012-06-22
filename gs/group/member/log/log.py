# coding=utf-8
from datetime import date
from zope.interface import implements
from Products.GSGroupMember.groupMembersInfo import GSGroupMembersInfo
from gs.group.member.log.queries import JoinLeaveQuery
from gs.group.member.log.monthlog import MonthLog
from gs.group.member.log.interfaces import IJoinAndLeaveLog

class JoinAndLeaveLog(object):
    implements(IJoinAndLeaveLog)
    """ A log of how many members have joined and left
        over each month. 
    """
    
    def __init__(self, groupInfo):
        group = groupInfo.groupObj
        self.groupInfo = groupInfo
        self.membersInfo = GSGroupMembersInfo(group)
        self.queries = JoinLeaveQuery(group)
        self.__events = self.__years = self.__monthLogs = None
    
    @property
    def events(self):
        if self.__events == None:
            self.__events = \
              self.queries.group_join_leave_events(self.groupInfo.id)
        return self.__events

    @property
    def years(self):
        if self.__years == None:
            years = []
            if self.events:
                earliestYear = min(self.events.keys())
                latestYear = date.today().year
                years = range(latestYear, (earliestYear - 1), -1)
            self.__years = years
        return self.__years
                
    @property
    def monthLogs(self):
        """ The logs for each month, over the appropriate timespan.
        """
        if self.__monthLogs == None:
            monthLogs = []
            numMembersMonthEnd = self.membersInfo.fullMemberCount
            for year in self.years:
                latestMonth = 12
                earliestMonth = 1
                if year == self.years[0]:
                    latestMonth = date.today().month
                if year == self.years[-1]:
                    earliestMonth = min(self.events[year].keys())
                for month in range(latestMonth, (earliestMonth - 1), -1):
                    events = {}
                    if self.events.has_key(year) and self.events[year].has_key(month):
                        events = self.events[year][month]
                    monthLog = MonthLog(self.groupInfo, year, month,
                                          numMembersMonthEnd, events)
                    monthLogs.append(monthLog)
                    numMembersMonthEnd = monthLog.numMembersMonthStart
            self.__monthLogs = monthLogs
        return self.__monthLogs

