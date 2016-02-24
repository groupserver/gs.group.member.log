=======================
``gs.group.member.log``
=======================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The changing membership of a GroupServer group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2016-02-24
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.Net`_.

.. _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/
            
Introduction
============

This product provides two viewlets_ that provide a log of who has
joined and left a group. The viewlets are registered for the
*Members* page [#list]_.

Viewlets
========

There are two viewlets:

`Summary viewlet`_:
  A summary of the joining and leaving events, shown to everyone
  that can see the page.

`Detailed viewlet`_:
  The details of who joined and left, shown to just the
  administrators.

Summary viewlet
---------------

The summary viewlet is designed to show people how much *churn*
there is in the membership of the group. For each month it shows:

* The total membership of the group,
* How many people joined, and
* How many people left.

The details about who joined and left is shown in the `detailed
viewlet`_.

Detailed viewlet
----------------

The detailed viewlet shows, for each month:

* The total membership of the group,
* How many people joined, and
* How many people left, 
* **Who** joined and why, and
* **Who** left and why.

For privacy reasons only the administrators are shown the
detailed viewlet.

There are two ways to control the amount of information that is
show. First, each month is a disclosure [#disclosure]_, with the
details of the members that joined and left hidden by
default. Second, a menu allows the administrator to show just the
joining events, just the leaving events, or all the events. The
menu is powered by some JavaScript_.

JavaScript
~~~~~~~~~~

The JavaScript resource
``gs-group-member-log-detail-20130919.js`` provides the
client-side code to power the menu on the detailed viewlet.

Resources
=========

- Translations:
  https://www.transifex.com/groupserver/gs-group-member-log/
- Code repository:
  https://github.com/groupserver/gs.group.member.log
- Questions and comments to
  http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
.. _Creative Commons Attribution-Share Alike 3.0 New Zealand License:
   http://creativecommons.org/licenses/by-sa/3.0/nz/

.. [#list] See ``gs.group.member.list``
           <https://github.com/groupserver/gs.group.member.list>

.. [#disclosure] See ``gs.content.js.disclosure``
           <https://github.com/groupserver/gs.content.js.disclosure>

..  LocalWords:  viewlets
