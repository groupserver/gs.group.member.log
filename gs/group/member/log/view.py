# coding=utf-8
from Products.Five import BrowserView
from zope.component import createObject
from Products.GSGroup.interfaces import IGSGroupInfo
from gs.group.member.log.log import JoinAndLeaveLog 

class JoinAndLeaveLogView(BrowserView):
    """ The browser view of a group's join and leave log. 
    """
    
    def __init__(self, group, request):
        BrowserView.__init__(self, group, request)
        self.groupInfo = IGSGroupInfo(group)
        self.siteInfo = createObject('groupserver.SiteInfo', group)
        self.log = JoinAndLeaveLog(self.groupInfo)
        self.title = 'Join and Leave Log for %s' % self.groupInfo.name
    
