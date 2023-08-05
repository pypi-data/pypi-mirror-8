#!/usr/bin/python
# -*- coding: utf-8 -*-

# wix: a SAT frontend
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
import wx
from sat_frontends.quick_frontend.quick_contact_list import QuickContactList
from sat_frontends.wix.constants import Const
from sat.core.log import getLogger
log = getLogger(__name__)
from cgi import escape
from sat_frontends.tools.jid  import JID
from os.path import join


class Group(unicode):
    """Class used to recognize groups"""

class Contact(unicode):
    """Class used to recognize groups"""

class ContactList(wx.SimpleHtmlListBox, QuickContactList):
    """Customized control to manage contacts."""

    def __init__(self, parent, host, type_="JID"):
        """init the contact list
        @param parent: WxWidgets parent of the widget
        @param host: wix main app class
        @param type_: type of contact list: "JID" for the usual big jid contact list
                                           "CUSTOM" for a customized contact list (self._presentItem must then be overrided)
        """
        wx.SimpleHtmlListBox.__init__(self, parent, -1)
        QuickContactList.__init__(self)
        self.host = host
        self.type = type_
        self.__typeSwitch()
        self.groups = {}  #list contacts in each groups, key = group
        self.empty_avatar = join(host.media_dir, 'misc/empty_avatar')
        self.Bind(wx.EVT_LISTBOX, self.onSelected)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.onActivated)

    def __contains__(self, jid):
        return bool(self.__find_idx(jid))

    def __typeSwitch(self):
        if self.type == "JID":
            self._presentItem = self._presentItemJID
        elif self.type != "CUSTOM":
            self._presentItem = self._presentItemDefault

    def __find_idx(self, entity):
        """Find indexes of given contact (or groups) in contact list, manage jid
        @return: list of indexes"""
        result=[]
        for i in range(self.GetCount()):
            if (type(entity) == JID and type(self.GetClientData(i)) == JID and self.GetClientData(i).bare == entity.bare) or\
                self.GetClientData(i) == entity:
                result.append(i)
        return result

    def update_jid(self, jid):
        self.replace(jid)

    def replace(self, contact, groups=None, attributes=None):
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
        log.debug(_("update %s") % contact)
        if not self.__find_idx(contact):
            self.add(contact, groups)
        else:
            for i in self.__find_idx(contact):
                _present = self._presentItem(contact)
                if _present != None:
                    self.SetString(i, _present)

    def __eraseGroup(self, group):
        """Erase all contacts in group
        @param group: group to erase
        @return: True if something as been erased"""
        erased = False
        indexes = self.__find_idx(group)
        for idx in indexes:
            while idx<self.GetCount()-1 and type(self.GetClientData(idx+1)) != Group:
                erased = True
                self.Delete(idx+1)
        return erased


    def _presentGroup(self, group):
        """Make a nice presentation for the contact groups"""
        html = u"""-- [%s] --""" % group

        return html

    def _presentItemDefault(self, contact):
        """Make a basic presentation of string contacts in the list."""
        return contact

    def _presentItemJID(self, jid):
        """Make a nice presentation of the contact in the list for JID contacts."""
        name = self.getCache(jid,'name')
        nick = self.getCache(jid,'nick')
        _show = self.getCache(jid,'show')
        if _show == None or _show == 'unavailable':
            return None
        show = [x for x in Const.PRESENCE if x[0] == _show][0]

        #show[0]==shortcut
        #show[1]==human readable
        #show[2]==color (or None)
        show_html = "<font color='%s'>[%s]</font>" % (show[2], show[1]) if show[2] else ""
        status = self.getCache(jid,'status') or ''
        avatar = self.getCache(jid,'avatar') or self.empty_avatar #XXX: there is a weird bug here: if the image has an extension (i.e. empty_avatar.png),
        #WxPython segfault, and it doesn't without nothing. I couldn't reproduce the case with a basic test script, so it need further investigation before reporting it
        #to WxPython dev. Anyway, the program crash with a segfault, not a python exception, so there is definitely something wrong with WxPython.
        #The case seems to happen when SimpleHtmlListBox parse the HTML with the <img> tag

        html = """
        <table border='0'>
        <td>
            <img  height='64' width='64' src='%s' />
        </td>
        <td>
            <b>%s</b> %s<br />
            <i>%s</i>
        </td>
        </table>
        """ % (avatar,
               escape(nick or name or jid.node or jid.bare),
               show_html,
               escape(status))

        return html

    def clearContacts(self):
        """Clear all the contact list"""
        self.Clear()

    def add(self, contact, groups = None):
        """add a contact to the list"""
        log.debug (_("adding %s"),contact)
        if not groups:
            _present =  self._presentItem(contact)
            if _present:
                idx = self.Insert(_present, 0, contact)
        else:
            for group in groups:
                indexes = self.__find_idx(group)
                gp_idx = 0
                if not indexes:  #this is a new group, we have to create it
                    gp_idx = self.Append(self._presentGroup(group), Group(group))
                else:
                    gp_idx = indexes[0]

                _present = self._presentItem(contact)
                if _present:
                    self.Insert(_present, gp_idx+1, contact)

    def setSpecial(self, special_jid, special_type, show=False):
        """Set entity as a special
        @param jid: jid of the entity
        @param _type: special type (e.g.: "MUC")
        @param show: True to display the dialog to chat with this entity
        """
        QuickContactList.setSpecial(self, special_jid, special_type, show)
        if show:
            self._showDialog(special_jid)

    def _showDialog(self, jid):
        """Show the dialog associated to the given jid."""
        indexes = self.__find_idx(jid)
        if not indexes:
            return
        self.DeselectAll()
        self.SetSelection(indexes[0])
        self.onActivated(wx.MouseEvent())

    def remove(self, contact):
        """remove a contact from the list"""
        log.debug (_("removing %s"), contact)
        list_idx = self.__find_idx(contact)
        list_idx.reverse()  #as we make some deletions, we have to reverse the order
        for i in list_idx:
            self.Delete(i)

    def onSelected(self, event):
        """Called when a contact is selected."""
        data = self.getSelection()
        if data == None: #we have a group
            first_visible = self.GetVisibleBegin()
            group = self.GetClientData(self.GetSelection())
            erased = self.__eraseGroup(group)
            if not erased: #the group was already erased, we can add again the contacts
                contacts = [JID(contact) for contact in self.host.bridge.getContactsFromGroup(group, self.host.profile)]
                contacts.sort()
                id_insert = self.GetSelection()+1
                for contact in contacts:
                    _present =  self._presentItem(contact)
                    if _present:
                        self.Insert(_present, id_insert, contact)
            self.SetSelection(wx.NOT_FOUND)
            self.ScrollToLine(first_visible)
            event.Skip(False)
        else:
            event.Skip()

    def onActivated(self, event):
        """Called when a contact is clicked or activated with keyboard."""
        data = self.getSelection()
        self.onActivatedCB(data)
        event.Skip()

    def getSelection(self):
        """Return the selected contact, or an empty string if there is not"""
        if self.GetSelection() == wx.NOT_FOUND:
            return None
        data = self.GetClientData(self.GetSelection())
        if type(data) == Group:
            return None
        return data

    def registerActivatedCB(self, cb):
        """Register a callback with manage contact activation."""
        self.onActivatedCB=cb

