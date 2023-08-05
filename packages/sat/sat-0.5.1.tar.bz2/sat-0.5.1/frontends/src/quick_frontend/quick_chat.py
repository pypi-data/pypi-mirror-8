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
from sat_frontends.tools.jid  import JID
from sat_frontends.quick_frontend.quick_utils import unescapePrivate
from sat_frontends.quick_frontend.constants import Const


class QuickChat(object):

    def __init__(self, target, host, type_='one2one'):
        self.target = target
        self.host = host
        self.type = type_
        self.id = ""
        self.nick = None
        self.occupants = set()

    def setType(self, type_):
        """Set the type of the chat
        @param type: can be 'one2one' for single conversation or 'group' for chat à la IRC
        """
        self.type = type_

    def setPresents(self, nicks):
        """Set the users presents in the contact list for a group chat
        @param nicks: list of nicknames
        """
        log.debug (_("Adding users %s to room") % nicks)
        if self.type != "group":
            log.error (_("[INTERNAL] trying to set presents nicks for a non group chat window"))
            raise Exception("INTERNAL ERROR") #TODO: raise proper Exception here
        self.occupants.update(nicks)

    def replaceUser(self, nick, show_info=True):
        """Add user if it is not in the group list"""
        log.debug (_("Replacing user %s") % nick)
        if self.type != "group":
            log.error (_("[INTERNAL] trying to replace user for a non group chat window"))
            raise Exception("INTERNAL ERROR") #TODO: raise proper Exception here
        len_before = len(self.occupants)
        self.occupants.add(nick)
        if len_before != len(self.occupants) and show_info:
            self.printInfo("=> %s has joined the room" % nick)

    def removeUser(self, nick, show_info=True):
        """Remove a user from the group list"""
        log.debug(_("Removing user %s") % nick)
        if self.type != "group":
            log.error (_("[INTERNAL] trying to remove user for a non group chat window"))
            raise Exception("INTERNAL ERROR") #TODO: raise proper Exception here
        self.occupants.remove(nick)
        if show_info:
            self.printInfo("<= %s has left the room" % nick)

    def setUserNick(self, nick):
        """Set the nick of the user, usefull for e.g. change the color of the user"""
        self.nick = nick

    def getUserNick(self):
        return unicode(self.nick)

    def changeUserNick(self, old_nick, new_nick):
        """Change nick of a user in group list"""
        log.debug(_("Changing nick of user %(old_nick)s to %(new_nick)s") % {"old_nick": old_nick, "new_nick": new_nick})
        if self.type != "group":
            log.error (_("[INTERNAL] trying to change user nick for a non group chat window"))
            raise Exception("INTERNAL ERROR") #TODO: raise proper Exception here
        self.removeUser(old_nick, show_info=False)
        self.replaceUser(new_nick, show_info=False)
        self.printInfo("%s is now known as %s" % (old_nick, new_nick))

    def setSubject(self, subject):
        """Set title for a group chat"""
        log.debug(_("Setting subject to %s") % subject)
        if self.type != "group":
            log.error (_("[INTERNAL] trying to set subject for a non group chat window"))
            raise Exception("INTERNAL ERROR") #TODO: raise proper Exception here

    def afterHistoryPrint(self):
        """Refresh or scroll down the focus after the history is printed"""
        pass

    def historyPrint(self, size=20, profile='@NONE@'):
        """Print the current history
        @param size (int): number of messages
        @param profile (str): %(doc_profile)s
        """
        log.debug(_("now we print the history (%d messages)") % size)

        def onHistory(history):
            for line in history:
                timestamp, from_jid, to_jid, message, _type, extra = line
                if ((self.type == 'group' and _type != 'groupchat') or
                   (self.type == 'one2one' and _type == 'groupchat')):
                    continue
                self.printMessage(JID(from_jid), message, profile, timestamp)
            self.afterHistoryPrint()

        def onHistoryError(err):
            log.error(_("Can't get history"))

        if self.target.startswith(Const.PRIVATE_PREFIX):
            target = unescapePrivate(self.target)
        else:
            target = self.target.bare

        return self.host.bridge.getHistory(self.host.profiles[profile]['whoami'].bare, target, size, profile=profile, callback=onHistory, errback=onHistoryError)

    def _get_nick(self, jid):
        """Return nick of this jid when possible"""
        if self.target.startswith(Const.PRIVATE_PREFIX):
            unescaped = unescapePrivate(self.target)
            if jid.startswith(Const.PRIVATE_PREFIX) or unescaped.bare == jid.bare:
                return unescaped.resource
        return jid.resource if self.type == "group" else (self.host.contact_list.getCache(jid,'nick') or self.host.contact_list.getCache(jid,'name') or jid.node)

    def printMessage(self, from_jid, msg, profile, timestamp = ''):
        """Print message in chat window. Must be implemented by child class"""
        jid=JID(from_jid)
        nick = self._get_nick(jid)
        mymess = (jid.resource == self.nick) if self.type == "group" else (jid.bare == self.host.profiles[profile]['whoami'].bare) #mymess = True if message comes from local user
        if msg.startswith('/me '):
            self.printInfo('* %s %s' % (nick, msg[4:]), type_='me', timestamp=timestamp)
            return
        return jid, nick, mymess

    def printInfo(self, msg, type_='normal'):
        """Print general info
        @param msg: message to print
        @type_: one of:
            normal: general info like "toto has joined the room"
            me: "/me" information like "/me clenches his fist" ==> "toto clenches his fist"
        """
        raise NotImplementedError

    def startGame(self, game_type, referee, players):
        """Configure the chat window to start a game"""
        #No need to raise an error as game are not mandatory
        log.warning(_('startGame is not implemented in this frontend'))

    def getGame(self, game_type):
        """Return class managing the game type"""
        #No need to raise an error as game are not mandatory
        log.warning(_('getGame is not implemented in this frontend'))

    def updateChatState(self, state, nick=None):
        """Set the chat state (XEP-0085) of the contact. Leave nick to None
        to set the state for a one2one conversation, or give a nickname or
        Const.ALL_OCCUPANTS to set the state of a participant within a MUC.
        @param state: the new chat state
        @param nick: None for one2one, the MUC user nick or ALL_OCCUPANTS
        """
        raise NotImplementedError

