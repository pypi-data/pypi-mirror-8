#!/usr/bin/python
# -*- coding: utf-8 -*-

# helper class for making a SAT frontend
# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014 Jérôme Poisson (goffi@goffi.org)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from sat.core.i18n import _
from sat.core.log import getLogger
log = getLogger(__name__)


class QuickContactList(object):
    """This class manage the visual representation of contacts"""

    def __init__(self):
        log.debug(_("Contact List init"))
        self._cache = {}
        self.specials={}

    def update_jid(self, jid):
        """Update the jid in the list when something changed"""
        raise NotImplementedError

    def getCache(self, jid, name):
        try:
            jid_cache = self._cache[jid.bare]
            if name == 'status': #XXX: we get the first status for 'status' key
                return jid_cache['statuses'].get('default','')
            return jid_cache[name]
        except (KeyError, IndexError):
            return None

    def setCache(self, jid, name, value):
        jid_cache = self._cache.setdefault(jid.bare, {})
        jid_cache[name] = value

    def __contains__(self, jid):
        raise NotImplementedError

    def clearContacts(self):
        """Clear all the contact list"""
        self.specials.clear()

    def replace(self, jid, groups=None, attributes=None):
        """Add a contact to the list if doesn't exist, else update it.

        This method can be called with groups=None for the purpose of updating
        the contact's attributes (e.g. nickname). In that case, the groups
        attribute must not be set to the default group but ignored. If not,
        you may move your contact from its actual group(s) to the default one.

        None value for 'groups' has a different meaning than [None] which is for the default group.

        @param jid (JID)
        @param groups (list): list of groups or None to ignore the groups membership.
        @param attributes (dict)
        """
        if attributes and 'name' in attributes:
            self.setCache(jid, 'name', attributes['name'])

    def remove(self, jid):
        """remove a contact from the list"""
        try:
            del self.specials[jid.bare]
        except KeyError:
            pass

    def add(self, jid, param_groups=None):
        """add a contact to the list"""
        raise NotImplementedError

    def getSpecial(self, jid):
        """Return special type of jid, or None if it's not special"""
        return self.specials.get(jid.bare)

    def setSpecial(self, jid, _type, show=False):
        """Set entity as a special
        @param jid: jid of the entity
        @param _type: special type (e.g.: "MUC")
        @param show: True to display the dialog to chat with this entity
        """
        self.specials[jid.bare] = _type

    def updatePresence(self, jid, show, priority, statuses):
        """Update entity's presence status
        @param jid: entity to update's jid
        @param show: availability
        @parap priority: resource's priority
        @param statuses: dict of statuses"""
        self.setCache(jid, 'show', show)
        self.setCache(jid, 'prority', priority)
        self.setCache(jid, 'statuses', statuses)
        self.update_jid(jid)
