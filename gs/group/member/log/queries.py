# coding=utf-8
import sqlalchemy as sa
from gs.group.member.join.audit import JOIN_GROUP as JOIN
from gs.group.member.join.audit import SUBSYSTEM as JOIN_SUBSYSTEM
from gs.group.member.leave.audit import LEAVE
from gs.group.member.leave.audit import SUBSYSTEM as LEAVE_SUBSYSTEM

class JoinLeaveQuery(object):
    
    def __init__(self, context, da):
        self.auditEventTable = da.createTable('audit_event')
    
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
        joinClauses = ((aet.c.subsystem == JOIN_SUBSYSTEM) & (aet.c.event_code == JOIN))
        leaveClauses = ((aet.c.subsystem == LEAVE_SUBSYSTEM) & (aet.c.event_code == LEAVE))
        s.append_whereclause(joinClauses | leaveClauses)
        s.append_whereclause(aet.c.group_id == group_id)
        
        r = s.execute()
        if r.rowcount:
            rows = [{
              'year': int(row['year']),
              'month': int(row['month']),
              'date': row['event_date'],
              'subsystem': row['subsystem'],
              'user_id': row['instance_user_id'],
              'admin_id': row['user_id']
            } for row in r ]
        years = {}
        for row in rows:
            if row['year'] not in years.keys():
                years[row['year']] = {}
        for row in rows:
            if row['month'] not in years[row['year']].keys():
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

