# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2016 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals, print_function
from datetime import date
from mock import (MagicMock, patch, PropertyMock)
from unittest import TestCase
from gs.group.member.log.log import (JoinAndLeaveLog, )


class TestJoinAndLeaveLog(TestCase):
    '''Test the ``JoinAndLeaveLog`` class'''

    @patch.object(JoinAndLeaveLog, 'events', new_callable=PropertyMock)
    def test_years_none(self, m_e):
        'Test that we have no years if we have no events'
        m_e.return_value = []
        l = JoinAndLeaveLog(MagicMock())
        r = l.years

        self.assertEqual([], r)

    @patch.object(JoinAndLeaveLog, 'events', new_callable=PropertyMock)
    def test_years(self, m_e):
        'Test that we return all the years'
        m_e.return_value = {2011: None}
        l = JoinAndLeaveLog(MagicMock())
        r = l.years

        thisYear = date.today().year
        self.assertIn(2011, r)
        self.assertIn(thisYear, r)
        self.assertEqual(len(r), thisYear - 2011 + 1)

    @patch.object(JoinAndLeaveLog, 'events', new_callable=PropertyMock)
    @patch('gs.group.member.log.log.date')
    @patch('gs.group.member.log.log.FullMembers')
    @patch('gs.group.member.log.log.MonthLog')
    def test_monthLogs_today(self, m_ML, m_FM, m_d, m_e):
        m_FM.return_value = ['a', 'b', ]
        m_e.return_value = {2016: {1: None, 2: None}}
        m_d.today().year = 2016
        m_d.today().month = 2
        groupInfo = MagicMock()
        groupInfo.id = 'example'
        l = JoinAndLeaveLog(groupInfo)
        r = l.monthLogs

        self.assertEqual(2, len(r))

    @patch.object(JoinAndLeaveLog, 'events', new_callable=PropertyMock)
    @patch('gs.group.member.log.log.date')
    @patch('gs.group.member.log.log.FullMembers')
    @patch('gs.group.member.log.log.MonthLog')
    def test_monthLogs(self, m_ML, m_FM, m_d, m_e):
        m_FM.return_value = ['a', 'b', ]
        m_e.return_value = {2015: {6: None}}
        m_d.today().year = 2016
        m_d.today().month = 1
        groupInfo = MagicMock()
        groupInfo.id = 'example'
        l = JoinAndLeaveLog(groupInfo)
        r = l.monthLogs

        self.assertEqual(8, len(r))
