# coding=utf-8
from zope.interface import Attribute
from zope.schema import Date, Int, List

class IMonthLog(object):
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
    numMembersMonthEnd = Int(title=u'Number of Members',
      description=u'The number of members at the end of the month',
      required=False)
    joinedMembers = List(title=u'Joined Members',
      description=u'A list of JoinedMember objects who joined during the month',
      required=False)
    numMembersJoined = Int(title=u'Number of Members Joined',
      description=u'The number of members who joined during the month',
      required=False)
    leftMembers = List(title=u'Left Members',
      description=u'A list of LeftMember objects who left during the month',
      required=False)
    numMembersLeft = Int(title=u'Number of Members Left',
      description=u'The number of members who left during the month',
      required=False)
    
class IJoinedMember(object):
    """ Information about a joining event.
    """
    userInfo = Attribute("""A userInfo instance""")
    groupInfo = Attribute("""A groupInfo instance""")
    eventDate = Date(title=u'Event Date',
      description=u'The joining date',
      required=True)
    addingUser = Attribute("""Optional: The user who added the member to the group""")
    
class ILeftMember(object):
    """ Information about a leaving event.
    """
    userInfo = Attribute("""A userInfo instance""")
    groupInfo = Attribute("""A groupInfo instance""")
    eventDate = Date(title=u'Event Date',
      description=u'The joining date',
      required=True)
    removingUser = Attribute("""Optional: The user who removed the member from the group""")
    
    
