# coding=utf-8
from Products.Five import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.component import createObject
from Products.GSGroup.interfaces import IGSGroupInfo
from Products.GSGroupMember.groupMembersInfo import GSGroupMembersInfo
from gs.group.member.log.queries import JoinLeaveQuery

class JoinAndLeaveLog(BrowserView):
    ''' A log of how many members have joined and left
        over each month. 
    '''
    
    def __init__(self, group, request):
        BrowserView.__init__(self, group, request)
        self.siteInfo = createObject('groupserver.SiteInfo', group)
        self.groupInfo = IGSGroupInfo(group)
        self.membersInfo = GSGroupMembersInfo(group)
        self.queries = JoinLeaveQuery(group, group.zsqlalchemy)
        self.title = 'Join and Leave Log for %s' % self.groupInfo.name
        self.__totalJoined = self.__totalLeft = None
        self.__joinedYears = self.__leftYears = None
        self.__joinedMonths = self.__leftMonths = None
    
    def __call__(self):
        template = ViewPageTemplateFile(self.templateName)
        return template(self, view=self)

    @property
    def templateName(self):
        retval = 'browser/templates/standard.pt'
#        viewer = createObject('groupserver.LoggedInUser', 
#                              self.groupInfo.group)
#        if viewer.id in [a.id for a in self.groupInfo.group_admins]:
#            retval = 'browser/templates/admins.pt'
        return retval
    
    @property
    def totalJoined(self):
        if self.__totalJoined == None:
            self.__totalJoined = \
              self.queries.get_group_join_events(self.groupInfo.id)
        return self.__totalJoined
    
    @property
    def joinedYears(self):
        if self.__joinedYears == None:
            years = self.totalJoined.keys()
            years.sort()
            years.reverse()
            self.__joinedYears = years
        return self.__joinedYears
    
    def joinedMonths(self, year):
        retval = {}
        if self.joinedYears.has_key(year):
            retval = self.joinedYears[year]
        return retval
