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
from sat_frontends.primitivus.constants import Const as C
import wx
from sat.core.log import getLogger
log = getLogger(__name__)


NO_SELECTION_ENTRY = ' '


class ProfileManager(wx.Panel):
    def __init__(self, host):
        super(ProfileManager, self).__init__(host)
        self.host = host

        #self.sizer = wx.FlexGridSizer(cols=2)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        self.selected_profile = NO_SELECTION_ENTRY  # allow to reselect the previous selection until the profile is authenticated
        self.profile_name = wx.ComboBox(self, -1, style=wx.CB_READONLY|wx.CB_SORT)
        self.__refillProfiles()
        self.Bind(wx.EVT_COMBOBOX, self.onProfileChange)
        self.panel_id = wx

        self.sizer.Add(wx.Window(self, -1), 1)
        self.sizer.Add(wx.StaticText(self, -1, _("Profile:")), 0, flag=wx.ALIGN_CENTER)
        self.sizer.Add(self.profile_name, 0, flag=wx.ALIGN_CENTER)
        button_panel = wx.Panel(self)
        button_panel.sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_panel.SetSizer(button_panel.sizer)
        button_new = wx.Button(button_panel, -1, _("New"))
        button_del = wx.Button(button_panel, -1, _("Delete"))
        button_panel.sizer.Add(button_new)
        button_panel.sizer.Add(button_del)
        self.sizer.Add(button_panel, flag=wx.CENTER)
        self.Bind(wx.EVT_BUTTON, self.onNewProfile, button_new)
        self.Bind(wx.EVT_BUTTON, self.onDeleteProfile, button_del)

        login_box = wx.StaticBox(self, -1, _("Login"))
        self.login_sizer = wx.StaticBoxSizer(login_box, wx.VERTICAL)
        self.sizer.Add(self.login_sizer, 1, wx.EXPAND | wx.ALL)
        self.login_jid = wx.TextCtrl(self, -1)
        self.login_sizer.Add(wx.StaticText(self, -1, "JID:"), 0, flag=wx.ALIGN_CENTER)
        self.login_sizer.Add(self.login_jid, flag=wx.EXPAND)
        self.login_pass = wx.TextCtrl(self, -1, style = wx.TE_PASSWORD)
        self.login_sizer.Add(wx.StaticText(self, -1, _("Password:")), 0, flag=wx.ALIGN_CENTER)
        self.login_sizer.Add(self.login_pass, flag=wx.EXPAND)

        loggin_button = wx.Button(self, -1, _("Connect"))
        self.Bind(wx.EVT_BUTTON, self.onConnectButton, loggin_button)
        self.login_sizer.Add(loggin_button, flag=wx.ALIGN_CENTER)

        self.sizer.Add(wx.Window(self, -1), 1)

        #Now we can set the default value
        self.__setDefault()

    def __setDefault(self):
        profile_default = NO_SELECTION_ENTRY if self.host.options.profile else self.host.bridge.getProfileName("@DEFAULT@")
        if profile_default:
            self.profile_name.SetValue(profile_default)
            self.onProfileChange(None)

    def __refillProfiles(self):
        """Update profiles with current names. Must be called after a profile change"""
        self.profile_name.Clear()
        profiles = self.host.bridge.getProfilesList()
        profiles.sort()
        self.profile_name.Append(NO_SELECTION_ENTRY)
        for profile in profiles:
            self.profile_name.Append(profile)

    def onNewProfile(self, event):
        dlg = wx.TextEntryDialog(self, _("Please enter the new profile name"), _("New profile"), style = wx.OK | wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue()
            if name:
                if name[0]=='@':
                    wx.MessageDialog(self, _("A profile name can't start with a @"), _("Bad profile name"), wx.ICON_ERROR).ShowModal()
                else:
                    def cb():
                        self.__refillProfiles()
                        self.profile_name.SetValue(name)
                        self.selected_profile = name
                        self.getXMPPParams(name)
                    self.host.bridge.asyncCreateProfile(name, callback=cb)
        dlg.Destroy()

    def onDeleteProfile(self, event):
        name = self.profile_name.GetValue()
        if not name:
            return
        dlg = wx.MessageDialog(self, _("Are you sure to delete the profile [%s]") % name, _("Confirmation"), wx.ICON_QUESTION | wx.YES_NO)
        if dlg.ShowModal() == wx.ID_YES:
            def cb():
                self.__refillProfiles()
                self.__setDefault()
            self.host.bridge.asyncDeleteProfile(name, callback=cb)
        dlg.Destroy()

    def getXMPPParams(self, profile):
        """This is called from MainWindow.launchAction when the profile has been authenticated.

        @param profile: %(doc_profile)s
        """
        def setJID(jabberID):
            self.login_jid.SetValue(jabberID)

        def setPassword(password):
            self.login_pass.SetValue(password)

        self.profile_name.SetValue(profile)
        self.selected_profile = profile
        self.host.bridge.asyncGetParamA("JabberID", "Connection", profile_key=profile, callback=setJID, errback=self.getParamError)
        self.host.bridge.asyncGetParamA("Password", "Connection", profile_key=profile, callback=setPassword, errback=self.getParamError)

    def onProfileChange(self, event):
        """Called when a profile is choosen in the combo box"""
        profile_name = self.profile_name.GetValue()
        if not profile_name or profile_name == self.selected_profile:
            return  # avoid infinite loop
        if profile_name == NO_SELECTION_ENTRY:
            self.selected_profile = NO_SELECTION_ENTRY
            return
        if self.selected_profile:
            self.profile_name.SetValue(self.selected_profile)
        self.host.profile = profile_name  # FIXME: EXTREMELY DIRTY, needed for sat_frontends.tools.xmlui.XMLUI.submit
        self.host.launchAction(C.AUTHENTICATE_PROFILE_ID, {'caller': 'profile_manager'}, profile_key=profile_name)

    def onConnectButton(self, event):
        """Called when the Connect button is pressed"""
        name = self.profile_name.GetValue()
        assert(name == self.selected_profile)  # if not, there's a bug somewhere...
        if not name or name == NO_SELECTION_ENTRY:
            wx.MessageDialog(self, _("You must select a profile or create a new one before connecting"), _("No profile selected"), wx.ICON_ERROR).ShowModal()
            return
        if name[0]=='@':
            wx.MessageDialog(self, _("A profile name can't start with a @"), _("Bad profile name"), wx.ICON_ERROR).ShowModal()
            return
        profile = self.host.bridge.getProfileName(name)
        assert(profile)

        self.host.bridge.asyncGetParamA("JabberID", "Connection", profile_key=profile, callback=lambda old_jid: self.__old_jidReceived(old_jid, profile), errback=self.getParamError)

    def __old_jidReceived(self, old_jid, profile):
        self.host.bridge.asyncGetParamA("Password", "Connection", profile_key=profile, callback=lambda old_pass: self.__old_passReceived(old_jid, old_pass, profile), errback=self.getParamError)

    def __old_passReceived(self, old_jid, old_pass, profile):
        new_jid = self.login_jid.GetValue()
        new_pass = self.login_pass.GetValue()
        if old_jid != new_jid:
            log.debug(_('Saving new JID and server'))
            self.host.bridge.setParam("JabberID", new_jid, "Connection", profile_key=profile)
        if old_pass != new_pass:
            log.debug(_('Saving new password'))
            self.host.bridge.setParam("Password", new_pass, "Connection", profile_key=profile)
        self.host.plug_profile(profile)


    def getParamError(self, ignore):
        wx.MessageDialog(self, _("Can't get profile parameter"), _("Profile error"), wx.ICON_ERROR).ShowModal()
