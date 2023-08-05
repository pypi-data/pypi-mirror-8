#!/usr/bin/python
# -*- coding: utf-8 -*-

# SAT plugin for managing xep-0045
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

from sat.core.i18n import _, D_
from sat.core.constants import Const as C
from sat.core.log import getLogger
log = getLogger(__name__)
from twisted.internet import defer
from twisted.words.protocols.jabber import jid

from sat.core import exceptions
from sat.memory import memory

import uuid

from wokkel import muc
from sat.tools import xml_tools


PLUGIN_INFO = {
    "name": "XEP 0045 Plugin",
    "import_name": "XEP-0045",
    "type": "XEP",
    "protocols": ["XEP-0045"],
    "dependencies": [],
    "recommendations": [C.TEXT_CMDS],
    "main": "XEP_0045",
    "handler": "yes",
    "description": _("""Implementation of Multi-User Chat""")
}

AFFILIATIONS = ('owner', 'admin', 'member', 'none', 'outcast')


class UnknownRoom(Exception):
    pass


class NotReadyYet(Exception):
    pass


class XEP_0045(object):
    # TODO: this plugin is messy, need a big cleanup/refactoring

    def __init__(self, host):
        log.info(_("Plugin XEP_0045 initialization"))
        self.host = host
        self.clients = {}
        self._sessions = memory.Sessions()
        host.bridge.addMethod("joinMUC", ".plugin", in_sign='ssa{ss}s', out_sign='s', method=self._join)
        host.bridge.addMethod("mucNick", ".plugin", in_sign='sss', out_sign='', method=self.mucNick)
        host.bridge.addMethod("mucLeave", ".plugin", in_sign='ss', out_sign='', method=self.mucLeave, async=True)
        host.bridge.addMethod("getRoomsJoined", ".plugin", in_sign='s', out_sign='a(sass)', method=self.getRoomsJoined)
        host.bridge.addMethod("getRoomsSubjects", ".plugin", in_sign='s', out_sign='a(ss)', method=self.getRoomsSubjects)
        host.bridge.addMethod("getUniqueRoomName", ".plugin", in_sign='ss', out_sign='s', method=self._getUniqueName)
        host.bridge.addMethod("configureRoom", ".plugin", in_sign='ss', out_sign='s', method=self._configureRoom, async=True)
        host.bridge.addSignal("roomJoined", ".plugin", signature='sasss')  # args: room_jid, room_nicks, user_nick, profile
        host.bridge.addSignal("roomLeft", ".plugin", signature='ss')  # args: room_jid, profile
        host.bridge.addSignal("roomUserJoined", ".plugin", signature='ssa{ss}s')  # args: room_jid, user_nick, user_data, profile
        host.bridge.addSignal("roomUserLeft", ".plugin", signature='ssa{ss}s')  # args: room_jid, user_nick, user_data, profile
        host.bridge.addSignal("roomUserChangedNick", ".plugin", signature='ssss')  # args: room_jid, old_nick, new_nick, profile
        host.bridge.addSignal("roomNewSubject", ".plugin", signature='sss')  # args: room_jid, subject, profile
        self.__submit_conf_id = host.registerCallback(self._submitConfiguration, with_data=True)
        host.importMenu((D_("MUC"), D_("configure")), self._configureRoomMenu, security_limit=4, help_string=D_("Configure Multi-User Chat room"), type_=C.MENU_ROOM)
        try:
            self.host.plugins[C.TEXT_CMDS].registerTextCommands(self)
            self.host.plugins[C.TEXT_CMDS].addWhoIsCb(self._whois, 100)
        except KeyError:
            log.info(_("Text commands not available"))

    def profileConnected(self, profile):
        def assign_service(service):
            client = self.host.getClient(profile)
            client.muc_service = service
        return self.getMUCService(profile_key=profile).addCallback(assign_service)

    def checkClient(self, profile):
        """Check if the profile is connected and has used the MUC feature.

        If profile was using MUC feature but is now disconnected, remove it from the client list.
        @param profile: profile to check
        @return: True if the profile is connected and has used the MUC feature, else False"""
        if not profile or profile not in self.clients or not self.host.isConnected(profile):
            log.error(_('Unknown or disconnected profile (%s)') % profile)
            if profile in self.clients:
                del self.clients[profile]
            return False
        return True

    def getProfileAssertInRoom(self, room_jid, profile_key):
        """Retrieve the profile name, assert that it's connected and participating in the given room.

        @param room_jid (JID): room JID
        @param profile_key (str): %(doc_profile_key)
        @return: the profile name
        """
        profile = self.host.memory.getProfileName(profile_key)
        if not self.checkClient(profile):
            raise exceptions.ProfileUnknownError("Unknown or disconnected profile")
        if room_jid.userhost() not in self.clients[profile].joined_rooms:
            raise UnknownRoom("This room has not been joined")
        return profile

    def __room_joined(self, room, profile):
        """Called when the user is in the requested room"""

        def _sendBridgeSignal(ignore=None):
            self.host.bridge.roomJoined(room.roomJID.userhost(), [user.nick for user in room.roster.values()], room.nick, profile)

        room_jid_s = room.roomJID.userhost()
        self.host.memory.updateEntityData(room.roomJID, "type", "chatroom", profile)
        self.clients[profile].joined_rooms[room_jid_s] = room
        if room.locked:
            #FIXME: the current behaviour is to create an instant room
            #and send the signal only when the room is unlocked
            #a proper configuration management should be done
            print "room locked !"
            self.clients[profile].configure(room.roomJID, {}).addCallbacks(_sendBridgeSignal, lambda x: log.error(_('Error while configuring the room')))
        else:
            _sendBridgeSignal()
        return room

    def __err_joining_room(self, failure, room_jid, nick, history_options, password, profile):
        """Called when something is going wrong when joining the room"""
        if hasattr(failure.value, "condition") and failure.value.condition == 'conflict':
            # we have a nickname conflict, we try again with "_" suffixed to current nickname
            nick += '_'
            return self.clients[profile].join(room_jid, nick, history_options, password).addCallbacks(self.__room_joined, self.__err_joining_room, callbackKeywords={'profile': profile}, errbackArgs=[room_jid, nick, history_options, password, profile])
        mess = D_("Error while joining the room %s" % room_jid.userhost())
        try:
            mess += " with condition '%s'" % failure.value.condition
        except AttributeError:
            pass
        log.error(mess)
        self.host.bridge.newAlert(mess, D_("Group chat error"), "ERROR", profile)
        raise failure

    def getRoomsJoined(self, profile_key=C.PROF_KEY_NONE):
        """Return room where user is"""
        profile = self.host.memory.getProfileName(profile_key)
        result = []
        if not self.checkClient(profile):
            return result
        for room in self.clients[profile].joined_rooms.values():
            result.append((room.roomJID.userhost(), [user.nick for user in room.roster.values()], room.nick))
        return result

    def getRoomNick(self, room_jid_s, profile_key=C.PROF_KEY_NONE):
        """return nick used in room by user

        @param room_jid_s: unicode room id
        @profile_key: profile
        @return: nick or empty string in case of error"""
        profile = self.host.memory.getProfileName(profile_key)
        if not self.checkClient(profile) or room_jid_s not in self.clients[profile].joined_rooms:
            return ''
        return self.clients[profile].joined_rooms[room_jid_s].nick

    def getRoomNickOfUser(self, room, user_jid, secure=True):
        """Returns the nick of the given user in the room.

        @room: instance of wokkel.muc.Room
        @user: JID or unicode (JID userhost).
        @param secure: set to True for a secure check
        @return: the nick or None if the user didn't join the room.
        """
        if not isinstance(user_jid, jid.JID):
            user_jid = jid.JID(user_jid).userhostJID()
        for user in room.roster.values():
            if user.entity is not None:
                if user.entity.userhostJID() == user_jid.userhostJID():
                    return user.nick
            elif not secure:
                # FIXME: this is NOT ENOUGH to check an identity!!
                # See in which conditions user.entity could be None.
                if user.nick == user_jid.user:
                    return user.nick
        return None

    def getRoomNicksOfUsers(self, room, users=[], secure=True):
        """Returns the nicks of the given users in the room.

        @room: instance of wokkel.muc.Room
        @users: list of JID or unicode (JID userhost).
        @param secure: set to True for a secure check
        @return: (x, y) with x a list containing the nicks of
        the users who are in the room, and y the missing users.
        """
        nicks = []
        missing = []
        for user in users:
            nick = self.getRoomNickOfUser(room, user, secure)
            if nick is None:
                missing.append(user)
            else:
                nicks.append(nick)
        return nicks, missing

    def _configureRoom(self, room_jid_s, profile_key=C.PROF_KEY_NONE):
        d = self.configureRoom(jid.JID(room_jid_s), profile_key)
        d.addCallback(lambda xmlui: xmlui.toXml())
        return d

    def _configureRoomMenu(self, menu_data, profile):
        """Return room configuration form

        @param menu_data: %(menu_data)s
        @param profile: %(doc_profile)s
        """
        try:
            room_jid = jid.JID(menu_data['room_jid'])
        except KeyError:
            log.error(_("room_jid key is not present !"))
            return defer.fail(exceptions.DataError)
        def xmluiReceived(xmlui):
            return {"xmlui": xmlui.toXml()}
        return self.configureRoom(room_jid, profile).addCallback(xmluiReceived)

    def configureRoom(self, room_jid, profile_key=C.PROF_KEY_NONE):
        """return the room configuration form

        @param room: jid of the room to configure
        @param profile_key: %(doc_profile_key)s
        @return: configuration form as XMLUI
        """
        profile = self.getProfileAssertInRoom(room_jid, profile_key)

        def config2XMLUI(result):
            if not result:
                return ""
            session_id, session_data = self._sessions.newSession(profile=profile)
            session_data["room_jid"] = room_jid
            xmlui = xml_tools.dataForm2XMLUI(result, submit_id=self.__submit_conf_id)
            xmlui.session_id = session_id
            return xmlui

        d = self.clients[profile].getConfiguration(room_jid)
        d.addCallback(config2XMLUI)
        return d

    def _submitConfiguration(self, raw_data, profile):
        try:
            session_data = self._sessions.profileGet(raw_data["session_id"], profile)
        except KeyError:
            log.warning(D_("Session ID doesn't exist, session has probably expired."))
            _dialog = xml_tools.XMLUI('popup', title=D_('Room configuration failed'))
            _dialog.addText(D_("Session ID doesn't exist, session has probably expired."))
            return defer.succeed({'xmlui': _dialog.toXml()})

        data = xml_tools.XMLUIResult2DataFormResult(raw_data)
        d = self.clients[profile].configure(session_data['room_jid'], data)
        _dialog = xml_tools.XMLUI('popup', title=D_('Room configuration succeed'))
        _dialog.addText(D_("The new settings have been saved."))
        d.addCallback(lambda ignore: {'xmlui': _dialog.toXml()})
        del self._sessions[raw_data["session_id"]]
        return d

    def isNickInRoom(self, room_jid, nick, profile):
        """Tell if a nick is currently present in a room"""
        profile = self.getProfileAssertInRoom(room_jid, profile)
        return self.clients[profile].joined_rooms[room_jid.userhost()].inRoster(muc.User(nick))

    def getRoomsSubjects(self, profile_key=C.PROF_KEY_NONE):
        """Return received subjects of rooms"""
        profile = self.host.memory.getProfileName(profile_key)
        if not self.checkClient(profile):
            return []
        return self.clients[profile].rec_subjects.values()

    @defer.inlineCallbacks
    def getMUCService(self, jid_=None, profile_key=C.PROF_KEY_NONE):
        """Return first found MUC service of an entity

        @param jid_: entity which may have a MUC service, or None for our own server
        @param profile_key: %(doc_profile_key)s
        """
        muc_service = None
        services = yield self.host.findServiceEntities("conference", "text", jid_, profile_key=profile_key)
        for service in services:
            if not ".irc." in service.userhost():
                # FIXME:
                # This ugly hack is here to avoid an issue with openfire: the IRC gateway
                # use "conference/text" identity (instead of "conference/irc")
                muc_service = service
                break
        defer.returnValue(muc_service)

    def _getUniqueName(self, muc_service="", profile_key=C.PROF_KEY_NONE):
        return self.getUniqueName(muc_service or None, profile_key).full()

    def getUniqueName(self, muc_service=None, profile_key=C.PROF_KEY_NONE):
        """Return unique name for a room, avoiding collision

        @param muc_service: leave empty string to use the default service
        @return: unique room userhost, or '' if an error occured.
        """
        #TODO: we should use #RFC-0045 10.1.4 when available here
        client = self.host.getClient(profile_key)
        room_name = uuid.uuid1()
        if muc_service is None:
            try:
                muc_service = client.muc_service
            except AttributeError:
                raise NotReadyYet("Main server MUC service has not been checked yet")
            if muc_service is None:
                log.warning(_("No MUC service found on main server"))
                raise exceptions.FeatureNotFound

        muc_service = muc_service.userhost()
        return jid.JID("%s@%s" % (room_name, muc_service))

    def join(self, room_jid, nick, options, profile_key=C.PROF_KEY_NONE):
        def _errDeferred(exc_obj=Exception, txt='Error while joining room'):
            d = defer.Deferred()
            d.errback(exc_obj(txt))
            return d

        profile = self.host.memory.getProfileName(profile_key)
        if not self.checkClient(profile):
            return _errDeferred()
        if room_jid.userhost() in self.clients[profile].joined_rooms:
            log.warning(_('%(profile)s is already in room %(room_jid)s') % {'profile': profile, 'room_jid': room_jid.userhost()})
            return _errDeferred()
        log.info(_("[%(profile)s] is joining room %(room)s with nick %(nick)s") % {'profile': profile, 'room': room_jid.userhost(), 'nick': nick})

        history_options = options["history"] == "True" if "history" in options else None
        password = options["password"] if "password" in options else None

        return self.clients[profile].join(room_jid, nick, history_options, password).addCallbacks(self.__room_joined, self.__err_joining_room, callbackKeywords={'profile': profile}, errbackArgs=[room_jid, nick, history_options, password, profile])
        # FIXME: how to set the cancel method on the Deferred created by wokkel?
        # This happens when the room is not reachable, e.g. no internet connection:
        # > /usr/local/lib/python2.7/dist-packages/twisted/internet/defer.py(480)_startRunCallbacks()
        # -> raise AlreadyCalledError(extra)

    def _join(self, room_jid_s, nick, options={}, profile_key=C.PROF_KEY_NONE):
        """join method used by bridge: use the join method, but doesn't return any deferred
        @return the room userhost (given value or unique generated name)
        """
        profile = self.host.memory.getProfileName(profile_key)
        if not self.checkClient(profile):
            return
        if room_jid_s == "":
            room_jid_s = self.getUniqueName(profile_key=profile_key)
        try:
            room_jid = jid.JID(room_jid_s)
        except:
            mess = _("Invalid room jid: %s") % room_jid_s
            log.warning(mess)
            self.host.bridge.newAlert(mess, _("Group chat error"), "ERROR", profile)
            return
        self.join(room_jid, nick, options, profile)
        # TODO: error management + signal in bridge
        return room_jid_s

    def nick(self, room_jid, nick, profile_key):
        profile = self.getProfileAssertInRoom(room_jid, profile_key)
        return self.clients[profile].nick(room_jid, nick)

    def leave(self, room_jid, profile_key):
        profile = self.getProfileAssertInRoom(room_jid, profile_key)
        return self.clients[profile].leave(room_jid)

    def subject(self, room_jid, subject, profile_key):
        profile = self.getProfileAssertInRoom(room_jid, profile_key)
        return self.clients[profile].subject(room_jid, subject)

    def mucNick(self, room_jid_s, nick, profile_key=C.PROF_KEY_NONE):
        """Change nickname in a room"""
        return self.nick(jid.JID(room_jid_s), nick, profile_key)

    def mucLeave(self, room_jid_s, profile_key=C.PROF_KEY_NONE):
        """Leave a room"""
        return self.leave(jid.JID(room_jid_s), profile_key)

    def getHandler(self, profile):
        self.clients[profile] = SatMUCClient(self)
        return self.clients[profile]

    def profileDisconnected(self, profile):
        try:
            del self.clients[profile]
        except KeyError:
            pass

    def kick(self, nick, room_jid, options={}, profile_key=C.PROF_KEY_NONE):
        """
        Kick a participant from the room
        @param nick (str): nick of the user to kick
        @param room_jid_s (JID): jid of the room
        @param options (dict): attribute with extra info (reason, password) as in #XEP-0045
        @param profile_key (str): %(doc_profile_key)s
        """
        profile = self.getProfileAssertInRoom(room_jid, profile_key)
        return self.clients[profile].kick(room_jid, nick, reason=options.get('reason', None))

    def ban(self, entity_jid, room_jid, options={}, profile_key=C.PROF_KEY_NONE):
        """
        Ban an entity from the room
        @param entity_jid (JID): bare jid of the entity to be banned
        @param room_jid_s (JID): jid of the room
        @param options: attribute with extra info (reason, password) as in #XEP-0045
        @param profile_key (str): %(doc_profile_key)s
        """
        assert(not entity_jid.resource)
        assert(not room_jid.resource)
        profile = self.getProfileAssertInRoom(room_jid, profile_key)
        return self.clients[profile].ban(room_jid, entity_jid, reason=options.get('reason', None))

    def affiliate(self, entity_jid, room_jid, options=None, profile_key=C.PROF_KEY_NONE):
        """
        Change the affiliation of an entity
        @param entity_jid (JID): bare jid of the entity
        @param room_jid_s (JID): jid of the room
        @param options: attribute with extra info (reason, nick) as in #XEP-0045
        @param profile_key (str): %(doc_profile_key)s
        """
        assert(not entity_jid.resource)
        assert(not room_jid.resource)
        assert('affiliation' in options)
        profile = self.getProfileAssertInRoom(room_jid, profile_key)
        # TODO: handles reason and nick
        return self.clients[profile].modifyAffiliationList(room_jid, [entity_jid], options['affiliation'])

    # Text commands #

    def cmd_nick(self, mess_data, profile):
        """change nickname"""
        log.debug("Catched nick command")

        if mess_data['type'] != "groupchat":
            self.host.plugins[C.TEXT_CMDS].feedBackWrongContext('nick', 'groupchat', mess_data, profile)
            return False

        nick = mess_data["unparsed"].strip()
        room = mess_data["to"]

        self.nick(room, nick, profile)

        return False

    def cmd_join(self, mess_data, profile):
        """join a new room (on the same service if full jid is not specified)"""
        log.debug("Catched join command")

        if mess_data['type'] != "groupchat":
            self.host.plugins[C.TEXT_CMDS].feedBackWrongContext('join', 'groupchat', mess_data, profile)
            return False

        if mess_data["unparsed"].strip():
            room = self.host.plugins[C.TEXT_CMDS].getRoomJID(mess_data["unparsed"].strip(), mess_data["to"].host)
            nick = (self.getRoomNick(mess_data["to"].userhost(), profile) or
                    self.host.getClient(profile).jid.user)
            self.join(room, nick, {}, profile)

        return False

    def cmd_leave(self, mess_data, profile):
        """quit a room"""
        log.debug("Catched leave command")

        if mess_data['type'] != "groupchat":
            self.host.plugins[C.TEXT_CMDS].feedBackWrongContext('leave', 'groupchat', mess_data, profile)
            return False

        if mess_data["unparsed"].strip():
            room = self.host.plugins[C.TEXT_CMDS].getRoomJID(mess_data["unparsed"].strip(), mess_data["to"].host)
        else:
            room = mess_data["to"]

        self.leave(room, profile)

        return False

    def cmd_part(self, mess_data, profile):
        """just a synonym of /leave"""
        return self.cmd_leave(mess_data, profile)

    def cmd_kick(self, mess_data, profile):
        """kick a room member

        @command (group): (nick)
            - nick: the nick of the person to kick
        """
        log.debug("Catched kick command")

        if mess_data['type'] != "groupchat":
            self.host.plugins[C.TEXT_CMDS].feedBackWrongContext('kick', 'groupchat', mess_data, profile)
            return False

        options = mess_data["unparsed"].strip().split()
        try:
            nick = options[0]
            assert(self.isNickInRoom(mess_data["to"], nick, profile))
        except (IndexError, AssertionError):
            feedback = _(u"You must provide a member's nick to kick.")
            self.host.plugins[C.TEXT_CMDS].feedBack(feedback, mess_data, profile)
            return False

        d = self.kick(nick, mess_data["to"], {} if len(options) == 1 else {'reason': options[1]}, profile)

        def cb(dummy):
            mess_data['message'] = _('%s has been kicked') % nick
            if len(options) > 1:
                mess_data['message'] += _(' for the following reason: %s') % options[1]
            return True
        d.addCallback(cb)
        return d

    def cmd_ban(self, mess_data, profile):
        """ban an entity from the room

        @command (group): (JID) [reason]
            - JID: the JID of the entity to ban
            - reason: the reason why this entity is being banned
        """
        log.debug("Catched ban command")

        if mess_data['type'] != "groupchat":
            self.host.plugins[C.TEXT_CMDS].feedBackWrongContext('ban', 'groupchat', mess_data, profile)
            return False

        options = mess_data["unparsed"].strip().split()
        try:
            jid_s = options[0]
            entity_jid = jid.JID(jid_s).userhostJID()
            assert(entity_jid.user)
            assert(entity_jid.host)
        except (IndexError, jid.InvalidFormat, AssertionError):
            feedback = _(u"You must provide a valid JID to ban, like in '/ban contact@example.net'")
            self.host.plugins[C.TEXT_CMDS].feedBack(feedback, mess_data, profile)
            return False

        d = self.ban(entity_jid, mess_data["to"], {} if len(options) == 1 else {'reason': options[1]}, profile)

        def cb(dummy):
            mess_data['message'] = _('%s has been banned') % entity_jid
            if len(options) > 1:
                mess_data['message'] += _(' for the following reason: %s') % options[1]
            return True
        d.addCallback(cb)
        return d

    def cmd_affiliate(self, mess_data, profile):
        """affiliate an entity to the room

        @command (group): (JID) [owner|admin|member|none|outcast]
            - JID: the JID of the entity to affiliate
            - owner: grant owner privileges
            - admin: grant admin privileges
            - member: grant member privileges
            - none: reset entity privileges
            - outcast: ban entity
        """
        log.debug("Catched affiliate command")

        if mess_data['type'] != "groupchat":
            self.host.plugins[C.TEXT_CMDS].feedBackWrongContext('affiliate', 'groupchat', mess_data, profile)
            return False

        options = mess_data["unparsed"].strip().split()
        try:
            jid_s = options[0]
            entity_jid = jid.JID(jid_s).userhostJID()
            assert(entity_jid.user)
            assert(entity_jid.host)
        except (IndexError, jid.InvalidFormat, AssertionError):
            feedback = _(u"You must provide a valid JID to affiliate, like in '/affiliate contact@example.net member'")
            self.host.plugins[C.TEXT_CMDS].feedBack(feedback, mess_data, profile)
            return False

        affiliation = options[1] if len(options) > 1 else 'none'
        if affiliation not in AFFILIATIONS:
            feedback = _(u"You must provide a valid affiliation: %s") % ' '.join(AFFILIATIONS)
            self.host.plugins[C.TEXT_CMDS].feedBack(feedback, mess_data, profile)
            return False

        d = self.affiliate(entity_jid, mess_data["to"], {'affiliation': affiliation}, profile)

        def cb(dummy):
            mess_data['message'] = _('New affiliation for %(entity)s: %(affiliation)s') % {'entity': entity_jid, 'affiliation': affiliation}
            return True
        d.addCallback(cb)
        return d

    def cmd_title(self, mess_data, profile):
        """change room's subject"""
        log.debug("Catched title command")

        if mess_data['type'] != "groupchat":
            self.host.plugins[C.TEXT_CMDS].feedBackWrongContext('title', 'groupchat', mess_data, profile)
            return False

        subject = mess_data["unparsed"].strip()

        if subject:
            room = mess_data["to"]
            self.subject(room, subject, profile)

        return False

    def cmd_topic(self, mess_data, profile):
        """just a synonym of /title"""
        return self.cmd_title(mess_data, profile)

    def _whois(self, whois_msg, mess_data, target_jid, profile):
        """ Add MUC user informations to whois """
        if mess_data['type'] != "groupchat":
            return
        if target_jid.userhost() not in self.clients[profile].joined_rooms:
            log.warning(_("This room has not been joined"))
            return
        user = self.clients[profile].joined_rooms[target_jid.userhost()].getUser(target_jid.resource)
        whois_msg.append(_("Nickname: %s") % user.nick)
        if user.entity:
            whois_msg.append(_("Entity: %s") % user.entity)
        if user.affiliation != 'none':
            whois_msg.append(_("Affiliation: %s") % user.affiliation)
        if user.role != 'none':
            whois_msg.append(_("Role: %s") % user.role)
        if user.status:
            whois_msg.append(_("Status: %s") % user.status)
        if user.show:
            whois_msg.append(_("Show: %s") % user.show)


class SatMUCClient (muc.MUCClient):
    #implements(iwokkel.IDisco)

    def __init__(self, plugin_parent):
        self.plugin_parent = plugin_parent
        self.host = plugin_parent.host
        muc.MUCClient.__init__(self)
        self.joined_rooms = {}  # FIXME: seem to do the same thing as MUCClient's _rooms attribute, must be removed
        self.rec_subjects = {}
        self.__changing_nicks = set()  # used to keep trace of who is changing nick,
                                       # and to discard userJoinedRoom signal in this case
        print "init SatMUCClient OK"

    def subject(self, room, subject):
        return muc.MUCClientProtocol.subject(self, room, subject)

    def unavailableReceived(self, presence):
        #XXX: we override this method to manage nickname change
        #TODO: feed this back to Wokkel
        """
        Unavailable presence was received.

        If this was received from a MUC room occupant JID, that occupant has
        left the room.
        """
        room, user = self._getRoomUser(presence)

        if room is None or user is None:
            return

        room.removeUser(user)

        if muc.STATUS_CODE.NEW_NICK in presence.mucStatuses:
            self.__changing_nicks.add(presence.nick)
            self.userChangedNick(room, user, presence.nick)
        else:
            self.__changing_nicks.discard(presence.nick)
            self.userLeftRoom(room, user)

    def receivedGroupChat(self, room, user, body):
        log.debug('receivedGroupChat: room=%s user=%s body=%s' % (room, user, body))

    def userJoinedRoom(self, room, user):
        if user.nick in self.__changing_nicks:
            self.__changing_nicks.remove(user.nick)
        else:
            log.debug(_("user %(nick)s has joined room (%(room_id)s)") % {'nick': user.nick, 'room_id': room.occupantJID.userhost()})
            if not self.host.trigger.point("MUC user joined", room, user, self.parent.profile):
                return
            user_data = {'entity': user.entity.full() if user.entity else '', 'affiliation': user.affiliation, 'role': user.role}
            self.host.bridge.roomUserJoined(room.roomJID.userhost(), user.nick, user_data, self.parent.profile)

    def userLeftRoom(self, room, user):
        if not self.host.trigger.point("MUC user left", room, user, self.parent.profile):
            return
        if user.nick == room.nick:
            # we left the room
            room_jid_s = room.roomJID.userhost()
            log.info(_("Room [%(room)s] left (%(profile)s))") % {"room": room_jid_s,
                                                             "profile": self.parent.profile})
            self.host.memory.delEntityCache(room.roomJID, profile_key=self.parent.profile)
            del self.plugin_parent.clients[self.parent.profile].joined_rooms[room_jid_s]
            self.host.bridge.roomLeft(room.roomJID.userhost(), self.parent.profile)
        else:
            log.debug(_("user %(nick)s left room (%(room_id)s)") % {'nick': user.nick, 'room_id': room.occupantJID.userhost()})
            user_data = {'entity': user.entity.full() if user.entity else '', 'affiliation': user.affiliation, 'role': user.role}
            self.host.bridge.roomUserLeft(room.roomJID.userhost(), user.nick, user_data, self.parent.profile)

    def userChangedNick(self, room, user, new_nick):
        self.host.bridge.roomUserChangedNick(room.roomJID.userhost(), user.nick, new_nick, self.parent.profile)

    def userUpdatedStatus(self, room, user, show, status):
        print("FIXME: MUC status not managed yet")
        #FIXME:

    def receivedSubject(self, room, user, subject):
        log.debug(_("New subject for room (%(room_id)s): %(subject)s") % {'room_id': room.roomJID.full(), 'subject': subject})
        self.rec_subjects[room.roomJID.userhost()] = (room.roomJID.userhost(), subject)
        self.host.bridge.roomNewSubject(room.roomJID.userhost(), subject, self.parent.profile)
