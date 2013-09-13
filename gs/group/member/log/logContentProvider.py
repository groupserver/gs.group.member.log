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
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy
from zope.component import provideAdapter, adapts
from zope.interface import implements, Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.contentprovider.interfaces import UpdateNotCalled, IContentProvider
from Products.GSGroupMember.groupmembership import user_division_admin_of_group
from Products.GSGroupMember.groupmembership import user_group_admin_of_group
from gs.group.member.log.interfaces import ILogContentProvider
from gs.group.base import GroupContentProvider


class LogContentProvider(GroupContentProvider):
    implements(ILogContentProvider)
    adapts(Interface, IDefaultBrowserLayer, Interface)

    def __init__(self, group, request, view):
        super(LogContentProvider, self).__init__(group, request, view)
        self.__updated = False

    def update(self):
        self.__updated = True

    def render(self):
        if not self.__updated:
            raise UpdateNotCalled
        if self.isAdmin:
            adminFile = 'browser/templates/adminView.pt'
            pageTemplate = ViewPageTemplateFile(adminFile)
        else:
            pageTemplate = ViewPageTemplateFile(self.pageTemplateFileName)
        retval = pageTemplate(self,
                              view=self,
                              log=self.log)
        return retval

    @Lazy
    def isAdmin(self):
        isGroupAdmin = user_group_admin_of_group(self.loggedInUser,
                                                    self.groupInfo)
        isSiteAdmin = user_division_admin_of_group(self.loggedInUser,
                                                    self.groupInfo)
        retval = (isGroupAdmin or isSiteAdmin)
        assert type(retval) == bool
        return retval

provideAdapter(LogContentProvider,
    provides=IContentProvider,
    name='gs.group.member.log.LogContentProvider')
