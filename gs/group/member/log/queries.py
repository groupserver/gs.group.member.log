# coding=utf-8
import sqlalchemy as sa
from gs.group.member.join.audit import JOIN_GROUP as JOIN
from gs.group.member.join.audit import SUBSYSTEM as JOIN_SUBSYSTEM
from gs.group.member.leave.audit import LEAVE
from gs.group.member.leave.audit import SUBSYSTEM as LEAVE_SUBSYSTEM

class JoinLeaveQuery(object):
    
    def __init__(self, context, da):
        self.auditEventTable = da.createTable('audit')
    
    def get_group_join_events(self, group_id):
        aet = self.auditEventTable
        s = aet.select([
          sa.extract('year',  aet.c.date).label('year'),
          sa.extract('month', aet.c.date).label('month'),
          aet.c.user_id,
          aet.c.instance_user_id,
          aet.c.group_id,
          aet.c.instanceDatum,
          aet.c.supplementaryDatum
        ])
        s.append_whereclause(aet.c.subsystem == JOIN_SUBSYSTEM)
        s.append_whereclause(aet.c.code == JOIN)
        s.append_whereclause(aet.c.group_id == group_id)
        s.group_by('year', 'month', aet.c.group_id)
        s.order_by(sa.desc('year'), sa.desc('month'), aet.c.group_id)
    
        r = s.execute()
        retval = []
        if r.rowcount:
            retval = [{
              'year':                int(x['year']),
              'month':               int(x['month']),
              'user_id':             x['user_id'],
              'instance_user_id':    x['instance_user_id'],
              'group_id':            x['group_id'],
              'instanceDatum':       x['instance_datum'],
              'supplementaryDatum':  x['supplementary_datum']} for x in r]
        assert type(retval) == list
        return retval

