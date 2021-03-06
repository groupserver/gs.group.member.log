# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2013, 2015, 2016 OnlineGroups.net and Contributors.
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
import sqlalchemy as sa
from gs.database import getSession, getTable
from gs.group.member.join.audit import JOIN_GROUP as JOIN, \
    SUBSYSTEM as JOIN_SUBSYSTEM
from gs.group.member.leave.base.audit import LEAVE, SUBSYSTEM as LEAVE_SUBSYSTEM


class JoinLeaveQuery(object):

    def __init__(self, context):
        self.auditEventTable = getTable('audit_event')

    def group_join_leave_events(self, group_id):
        aet = self.auditEventTable
#        SELECT EXTRACT(year FROM event_date) AS year,
#          EXTRACT(month FROM event_date) AS month,
#          subsystem, event_date, instance_user_id, user_id
#        FROM audit_event
#        WHERE
#          ((subsystem = 'gs.group.member.join' AND event_code = '1')
#           OR
#           (subsystem = 'gs.group.member.leave' AND event_code = '1'))
#          AND group_id = 'example_group';
        s = sa.select([
            sa.extract('year', aet.c.event_date).label('year'),
            sa.extract('month', aet.c.event_date).label('month'),
            aet.c.subsystem,
            aet.c.event_date,
            aet.c.instance_user_id,
            aet.c.user_id
        ])
        joinClauses = ((aet.c.subsystem == JOIN_SUBSYSTEM)
                       & (aet.c.event_code == JOIN))
        leaveClauses = ((aet.c.subsystem == LEAVE_SUBSYSTEM)
                        & (aet.c.event_code == LEAVE))
        s.append_whereclause(joinClauses | leaveClauses)
        s.append_whereclause(aet.c.group_id == group_id)

        session = getSession()
        r = session.execute(s)
        rows = []
        if r.rowcount:
            rows = [{
                'year': int(row['year']),
                'month': int(row['month']),
                'date': row['event_date'],
                'subsystem': row['subsystem'],
                'user_id': row['instance_user_id'],
                'admin_id': row['user_id']
            } for row in r]
        years = {}
        for row in rows:
            if row['year'] not in years:
                years[row['year']] = {}
        for row in rows:
            if row['month'] not in years[row['year']]:
                years[row['year']][row['month']] = {
                    JOIN_SUBSYSTEM: [],
                    LEAVE_SUBSYSTEM: []
                }
        for row in rows:
            years[row['year']][row['month']][row['subsystem']].append({
                'date': row['date'],
                'user_id': row['user_id'],
                'admin_id': row['admin_id']
            })
        retval = years
        assert type(retval) == dict
        return retval
