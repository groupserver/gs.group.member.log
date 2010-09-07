# coding=utf-8
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.component import createObject, provideAdapter, adapts
from zope.interface import implements, Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.contentprovider.interfaces import UpdateNotCalled, IContentProvider
from Products.GSGroupMember.groupmembership import user_division_admin_of_group
from Products.GSGroupMember.groupmembership import user_group_admin_of_group
from gs.group.member.log.interfaces import ILogContentProvider

class LogContentProvider(object):
    implements(ILogContentProvider)
    adapts(Interface, IDefaultBrowserLayer, Interface)
    
    def __init__(self, context, request, view):
        self.__parent__ = self.view = view
        self.__updated = False
    
        self.context = context
        self.request = request
        self.log = view.log
        self.groupInfo = view.groupInfo 
        
    def update(self):
        self.__updated = True
            
    def render(self):
        if not self.__updated:
            raise UpdateNotCalled
        if self.isAdmin:
            pageTemplate = ViewPageTemplateFile('browser/templates/adminView.pt')
        else:
            pageTemplate = ViewPageTemplateFile(self.pageTemplateFileName)
        retval = pageTemplate(self,
                              view=self,
                              log=self.log)
        return retval

    @property
    def isAdmin(self):
        viewingUserInfo = createObject('groupserver.LoggedInUser', self.context)
        isGroupAdmin = user_group_admin_of_group(viewingUserInfo, self.groupInfo)
        isSiteAdmin = user_division_admin_of_group(viewingUserInfo, self.groupInfo)
        retval = (isGroupAdmin or isSiteAdmin)
        assert type(retval) == bool
        return retval

provideAdapter(LogContentProvider,
    provides=IContentProvider,
    name='gs.group.member.log.LogContentProvider')

