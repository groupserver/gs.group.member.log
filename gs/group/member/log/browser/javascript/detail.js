// Copyright © 2013 OnlineGroups.net and Contributors.
// All Rights Reserved.
//
// This software is subject to the provisions of the Zope Public License,
// Version 2.1 (ZPL). A copy of the ZPL is avaliable at 
//  <http://groupserver.org/downloads/license/>

jQuery.noConflict();

function GSMemberLog (menuId, listId) {
    var menu = null, list = null, joinShown = true, leaveShown = true,
        TICK = '<span class="tick">&#10003;&#160;</span>',
        NOT_TICK = '<span class="not-tick">&#160;&#160;</span>';

    function show_just_join(event) {
        remove_tick(menu.find('li a'));
        hide_leave();
        show_join();
        hide_comma();
        add_tick(menu.find('a.join'));
    }

    function show_join() {
        joinShown = true;
        list.find('.join-event').removeClass('hide');
    }

    function hide_join() {
        joinShown = false;
        list.find('.join-event').addClass('hide');
    }

    function show_just_leave(event) {
        remove_tick(menu.find('li a'));
        hide_join();
        show_leave();
        hide_comma();
        add_tick(menu.find('a.leave'));
    }

    function show_leave() {
        leaveShown = true;
        list.find('.leave-event').removeClass('hide');
    }

    function hide_leave() {
        leaveShown = false;
        list.find('.leave-event').addClass('hide');
    }

    function show_all(event) {
        remove_tick(menu.find('li a'));
        if ( !joinShown ) {
            show_join();
        }
        if ( !leaveShown ) {
            show_leave();
        }
        show_comma();
        add_tick(menu.find('a.all'));
    }

    function show_comma() {
        list.find('.comma').removeClass('hide');
    }

    function hide_comma() {
        list.find('.comma').addClass('hide');
    }


    function add_tick(element) {
        element.find('.not-tick').remove();
        element.prepend(TICK);
    }
    function remove_tick(element) {
        element.find('.tick').remove();
        element.prepend(NOT_TICK);
    }

    function init() {
        menu = jQuery(menuId);
        list = jQuery(listId);

        menu.find('a').removeAttr('href');
        menu.find('a.all').click(show_all);
        menu.find('a.join').click(show_just_join);
        menu.find('a.leave').click(show_just_leave);
        show_all();
    }
    init(); // Note the automatic execution.

    return {
    }
}

jQuery(window).ready(function () {
    var log = null;
    log = GSMemberLog('#gs-group-member-log-all-menu', 
                      '#gs-group-member-log-all-list');
});
