# coding=utf-8
from Products.Five import BrowserView
from zope.component import createObject
from Products.GSGroup.interfaces import IGSGroupInfo
from Products.GSGroupMember.groupMembersInfo import GSGroupMembersInfo
from datetime import date
from gs.group.member.log.queries import JoinLeaveQuery
from gs.group.member.log.monthlog import MonthLog

class JoinAndLeaveLog(BrowserView):
    ''' A log of how many members have joined and left
        over each month. 
    '''
    
    def __init__(self, group, request):
        BrowserView.__init__(self, group, request)
        self.siteInfo = createObject('groupserver.SiteInfo', group)
        self.groupInfo = IGSGroupInfo(group)
        self.membersInfo = GSGroupMembersInfo(group)
        
        self.title = 'Join and Leave Log for %s' % self.groupInfo.name
        self.queries = JoinLeaveQuery(group, group.zsqlalchemy)
        self.__events = self.__years = self.__monthsByYear = None
        self.__monthLogs = None
    
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
            for e in self.events:
                if e['year'] not in years:
                    years.append(int(e['year']))
            if years:
                earliestYear = min(years)
                today = date.today()
                latestYear = today.year
                self.__years = range(latestYear, (earliestYear-1), -1)
            self.__years = years
        return self.__years

    @property
    def monthsByYear(self):
        if self.__monthsByYear == None:
            monthsByYear = {}
            if self.years:
                today = date.today()
                latestMonth = today.month
                earliestMonth = \
                  min([ e['month'] for e in self.events 
                        if e['year']==self.years[0] ])
                for year in self.years:
                    if (year==self.years[0]) and (year==self.years[-1]):
                        monthsByYear[year] = \
                          range(latestMonth, (earliestMonth-1), -1)
                    elif (year==self.years[0]):
                        monthsByYear[year] = range(latestMonth, 0, -1)
                    elif (year==self.years[-1]):
                        monthsByYear[year] = \
                          range(12, (earliestMonth-1), -1)
                    else:
                        monthsByYear[year] = range(12, 0, -1)
            self.__monthsByYear = monthsByYear
        return self.__monthsByYear

    @property
    def monthLogs(self):
        if self.__monthLogs == None:
            monthLogs = []
            for year in self.monthsByYear.keys():
                for month in year:
                    events = \
                      [ e for e in self.events 
                        if (e['year']==year) and (e['month']==month) ]
                    monthLog = MonthLog(self.groupInfo, events)
                    monthLogs.append(monthLog)
            self.__monthLogs = monthLogs
        return self.__monthLogs

