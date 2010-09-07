# coding=utf-8
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.component import createObject, provideAdapter, adapts
from zope.interface import implements, Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.contentprovider.interfaces import UpdateNotCalled, IContentProvider
from gs.group.member.log.interfaces import ILogContentProvider
from Products.XWFCore.XWFUtils import get_the_actual_instance_from_zope

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
        ctx = get_the_actual_instance_from_zope(self.context)
        groupInfo = createObject('groupserver.GroupInfo', ctx)
        viewingUserInfo = createObject('groupserver.LoggedInUser', ctx)
        isGroupAdmin = (viewingUserInfo.id in [ a.id for a in groupInfo.group_admins ])
        isSiteAdmin = (viewingUserInfo.id in [ a.id for a in groupInfo.site_admins ])
        retval = (isGroupAdmin or isSiteAdmin)
        assert type(retval) == bool
        return retval

provideAdapter(LogContentProvider,
    provides=IContentProvider,
    name='gs.group.member.log.LogContentProvider')

