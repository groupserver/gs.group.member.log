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
from zope.interface import Attribute
from zope.interface.interface import Interface
from zope.schema import Date, Dict, Int, List, Text
from zope.viewlet.interfaces import IViewletManager


class IJoinAndLeaveLog(Interface):
    """ A class which collates all the joining and leaving
        data for a group
    """
    groupInfo = Attribute("""A groupInfo instance""")
    membersInfo = Attribute("""A GSGroupMembersInfo instance""")
    queries = Attribute("""A JoinLeaveQuery instance""")
    events = Dict(title=u'Join and Leave Events',
      description=u'A dictionary, of which the keys are years.'
        u'Each corresponding value is another dictionary, of which '
        u'the keys are months. Each month value is another dictionary, '
        u'which has two keys: one for joining and one for leaving. Each '
        u'of these values are a list of joining or leaving events.',
      required=False)
    years = List(title=u'Years',
      description=u'A range of integers, ranging from the current '
        u'year to the first one for which we have joining or leaving data.',
      required=False)
    monthLogs = List(title=u'Monthly Logs',
      description=u'A list of MonthLog instances',
      required=False)


class IMonthLog(Interface):
    """ A class which knows all the joining and leaving for
        one particular month
    """
    groupInfo = Attribute("""A groupInfo instance""")
    year = Int(title=u'Year',
      description=u'The year',
      required=True)
    month = Int(title=u'Month',
      description=u'The month',
      required=True)
    numMembersMonthEnd = Int(title=u'End Number of Members',
      description=u'The number of members at the end of the month',
      required=False)
    events = Dict(title=u'Events',
      description=u'A dictionary with two keys: one with a list of '
        'joining events, the other with a list of leaving events',
      required=False)
    joinEvents = List(title=u'Join Events',
      description=u'A list of join events for the month',
      required=False)
    numMembersJoined = Int(title=u'Number of Members Joined',
      description=u'The number of members who joined during the month',
      required=False)
    leaveEvents = List(title=u'Leave Events',
      description=u'A list of leave events for the month',
      required=False)
    numMembersLeft = Int(title=u'Number of Members Left',
      description=u'The number of members who left during the month',
      required=False)
    numMembersMonthStart = Int(title=u'Start Number of Members',
      description=u'The number of members at the start of the month',
      required=False)


class IJoinEvent(Interface):
    """ Information about a joining event.
    """
    userInfo = Attribute("""A userInfo instance""")
    groupInfo = Attribute("""A groupInfo instance""")
    eventDate = Date(title=u'Event Date',
      description=u'The joining date',
      required=True)
    addingUserInfo = Attribute("Optional: The user who added the member to "
                                "the group")
    xhtml = Text(title=u'XHTML',
      description=u'XHTML description of event',
      required=True)


class ILeaveEvent(Interface):
    """ Information about a leaving event.
    """
    userInfo = Attribute("""A userInfo instance""")
    groupInfo = Attribute("""A groupInfo instance""")
    eventDate = Date(title=u'Event Date',
      description=u'The joining date',
      required=True)
    removingUserInfo = Attribute("Optional: The user who removed the member "
                                    "from the group")
    xhtml = Text(title=u'XHTML',
      description=u'XHTML description of event',
      required=True)


class ILogContentProvider(Interface):
    """The content provider for the group membership log """
    log = Attribute("""A JoinAndLeaveLog instance """)
    pageTemplateFileName = Text(title=u"Page Template File Name",
      description=u'The name of the ZPT file that is used to render the log.',
      required=False,
      default=u"browser/templates/standardView.pt")


class IJoinAndLeaveLog(IViewletManager):
    pass
