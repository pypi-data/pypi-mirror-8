#!/usr/bin/python
# -*- coding: utf-8 -*-

# SAT: a jabber client
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
from sat.core.constants import Const as C
from twisted.internet import task, defer
from twisted.words.protocols.jabber import jid, xmlstream
from wokkel import client, disco, xmppim, generic, compat, delay, iwokkel
from sat.core.log import getLogger
log = getLogger(__name__)
from sat.core import exceptions
from calendar import timegm
from zope.interface import implements
try:
    from twisted.words.protocols.xmlstream import XMPPHandler
except ImportError:
    from wokkel.subprotocols import XMPPHandler


class SatXMPPClient(client.XMPPClient):
    implements(iwokkel.IDisco)

    def __init__(self, host_app, profile, user_jid, password, host=None, port=C.XMPP_C2S_PORT):
        # XXX: DNS SRV records are checked when the host is not specified.
        # If no SRV record is found, the host is directly extracted from the JID.
        client.XMPPClient.__init__(self, user_jid, password, host or None, port or C.XMPP_C2S_PORT)
        self.factory.clientConnectionLost = self.connectionLost
        self.__connected = False
        self.profile = profile
        self.host_app = host_app
        self.conn_deferred = defer.Deferred()
        self._waiting_conf = {}  # callback called when a confirmation is received
        self._progress_cb_map = {}  # callback called when a progress is requested (key = progress id)

    def getConnectionDeferred(self):
        """Return a deferred which fire when the client is connected"""
        return self.conn_deferred

    def _authd(self, xmlstream):
        if not self.host_app.trigger.point("XML Initialized", xmlstream, self.profile):
            return
        client.XMPPClient._authd(self, xmlstream)
        self.__connected = True
        log.info(_("********** [%s] CONNECTED **********") % self.profile)
        self.streamInitialized()
        self.host_app.bridge.connected(self.profile)  # we send the signal to the clients

    def streamInitialized(self):
        """Called after _authd"""
        log.debug(_("XML stream is initialized"))
        self.keep_alife = task.LoopingCall(self.xmlstream.send, " ")  # Needed to avoid disconnection (specially with openfire)
        self.keep_alife.start(180)

        self.disco = SatDiscoProtocol(self)
        self.disco.setHandlerParent(self)
        self.discoHandler = disco.DiscoHandler()
        self.discoHandler.setHandlerParent(self)
        disco_d = defer.succeed(None)

        if not self.host_app.trigger.point("Disco handled", disco_d, self.profile):
            return

        def finish_connection(dummy):
            self.roster.requestRoster()
            self.presence.available()
            self.conn_deferred.callback(None)

        disco_d.addCallback(finish_connection)

    def initializationFailed(self, reason):
        log.error(_("ERROR: XMPP connection failed for profile '%(profile)s': %(reason)s" % {'profile': self.profile, 'reason': reason}))
        self.conn_deferred.errback(reason.value)
        try:
            client.XMPPClient.initializationFailed(self, reason)
        except:
            # we already chained an errback, no need to raise an exception
            pass

    def isConnected(self):
        return self.__connected

    def connectionLost(self, connector, unused_reason):
        try:
            self.keep_alife.stop()
        except AttributeError:
            log.debug(_("No keep_alife"))
        if self.__connected:
            log.info(_("********** [%s] DISCONNECTED **********") % self.profile)
            self.host_app.bridge.disconnected(self.profile)  # we send the signal to the clients
            self.host_app.purgeClient(self.profile)  # and we remove references to this client
        self.__connected = False


class SatMessageProtocol(xmppim.MessageProtocol):

    def __init__(self, host):
        xmppim.MessageProtocol.__init__(self)
        self.host = host

    def onMessage(self, message):
        log.debug(_(u"got message from: %s") % message["from"])
        post_treat = defer.Deferred() # XXX: plugin can add their treatments to this deferred

        if not self.host.trigger.point("MessageReceived", message, post_treat, profile=self.parent.profile):
            return

        data = {"from": message['from'],
                "to": message['to'],
                "body": "",
                "extra": {}}

        for e in message.elements():
            if e.name == "body":
                data['body'] = e.children[0] if e.children else ""
            elif e.name == "subject" and e.children:
                data['extra']['subject'] = e.children[0]

        data['type'] = message['type'] if message.hasAttribute('type') else 'normal'

        def bridgeSignal(data):
            if data is not None:
                self.host.bridge.newMessage(data['from'], data['body'], data['type'], data['to'], data['extra'], profile=self.parent.profile)
            return data

        def addToHistory(data):
            # set message body to empty string by default, and later
            # also forward message without body (chat state notification...)
            try:
                _delay = delay.Delay.fromElement(filter(lambda elm: elm.name == 'delay', message.elements())[0])
                timestamp = timegm(_delay.stamp.utctimetuple())
                data['extra']['archive'] = str(timestamp)
                if data['type'] != 'groupchat':  # XXX: we don't save delayed messages in history for groupchats
                    #TODO: add delayed messages to history if they aren't already in it
                    self.host.memory.addToHistory(jid.JID(data['from']), jid.JID(data['to']), data['body'], data['type'], data['extra'], timestamp, profile=self.parent.profile)
            except IndexError:
                self.host.memory.addToHistory(jid.JID(data['from']), jid.JID(data['to']), data['body'], data['type'], data['extra'], profile=self.parent.profile)
            return data

        def treatmentsEb(failure):
            failure.trap(exceptions.SkipHistory)
            return data

        def cancelErrorTrap(failure):
            """A message sending can be cancelled by a plugin treatment"""
            failure.trap(exceptions.CancelError)

        post_treat.addCallback(addToHistory)
        post_treat.addErrback(treatmentsEb)
        post_treat.addCallback(bridgeSignal)
        post_treat.addErrback(cancelErrorTrap)
        post_treat.callback(data)


class SatRosterProtocol(xmppim.RosterClientProtocol):

    def __init__(self, host):
        xmppim.RosterClientProtocol.__init__(self)
        self.host = host
        self.got_roster = defer.Deferred()
        #XXX: the two following dicts keep a local copy of the roster
        self._groups = {}  # map from groups to bare jids: key=group value=set of bare jids
        self._jids = {}  # map from bare jids to RosterItem: key=jid value=RosterItem

    def rosterCb(self, roster):
        for raw_jid, item in roster.iteritems():
            self.onRosterSet(item)

    def requestRoster(self):
        """ ask the server for Roster list """
        log.debug("requestRoster")
        d = self.getRoster().addCallback(self.rosterCb)
        d.chainDeferred(self.got_roster)

    def removeItem(self, to_jid):
        """Remove a contact from roster list
        @param to_jid: a JID instance
        """
        xmppim.RosterClientProtocol.removeItem(self, to_jid)
        #TODO: check IQ result

    #XXX: disabled (cf http://wokkel.ik.nu/ticket/56))
    #def addItem(self, to):
        #"""Add a contact to roster list"""
        #xmppim.RosterClientProtocol.addItem(self, to)
        #TODO: check IQ result"""

    def updateItem(self, roster_item):
        """
        Update an item of the contact list.

        @param roster_item: item to update
        """
        iq = compat.IQ(self.xmlstream, 'set')
        iq.addElement((xmppim.NS_ROSTER, 'query'))
        item = iq.query.addElement('item')
        item['jid'] = roster_item.jid.userhost()
        if roster_item.name:
            item['name'] = roster_item.name
        for group in roster_item.groups:
            item.addElement('group', content=group)
        return iq.send()

    def getAttributes(self, item):
        """Return dictionary of attributes as used in bridge from a RosterItem
        @param item: RosterItem
        @return: dictionary of attributes"""
        item_attr = {'to': unicode(item.subscriptionTo),
                     'from': unicode(item.subscriptionFrom),
                     'ask': unicode(item.ask)
                     }
        if item.name:
            item_attr['name'] = item.name
        return item_attr

    def onRosterSet(self, item):
        """Called when a new/update roster item is received"""
        #TODO: send a signal to frontends
        if not item.subscriptionTo and not item.subscriptionFrom and not item.ask:
            #XXX: current behaviour: we don't want contact in our roster list
            # if there is no presence subscription
            # may change in the future
            self.removeItem(item.jid)
            return
        log.info(_("new contact in roster list: %s") % item.jid.full())
        if not item.subscriptionTo:
            log.warning(_("You are not subscribed to this contact !"))
        if not item.subscriptionFrom:
            log.warning(_("This contact is not subscribed to you !"))
        #self.host.memory.addContact(item.jid, item_attr, item.groups, self.parent.profile)

        bare_jid = item.jid.userhostJID()
        self._jids[bare_jid] = item
        for group in item.groups:
            self._groups.setdefault(group, set()).add(bare_jid)
        self.host.bridge.newContact(item.jid.full(), self.getAttributes(item), item.groups, self.parent.profile)

    def onRosterRemove(self, entity):
        """Called when a roster removal event is received"""
        print _("removing %s from roster list") % entity.full()
        bare_jid = entity.userhostJID()

        # we first remove item from local cache (self._groups and self._jids)
        try:
            item = self._jids.pop(bare_jid)
        except KeyError:
            log.warning("Received a roster remove event for an item not in cache")
            return
        for group in item.groups:
            try:
                jids_set = self._groups[group]
                jids_set.remove(bare_jid)
                if not jids_set:
                    del self._groups[group]
            except KeyError:
                log.warning("there is not cache for the group [%(groups)s] of the removed roster item [%(jid)s]" %
                        {"group": group, "jid": bare_jid})

        # then we send the bridge signal
        self.host.bridge.contactDeleted(entity.userhost(), self.parent.profile)

    def getGroups(self):
        """Return a list of groups"""
        return self._groups.keys()

    def getItem(self, jid):
        """Return RosterItem for a given jid
        @param jid: jid of the contact
        @return: RosterItem or None if contact is not in cache"""
        return self._jids.get(jid.userhostJID(), None)

    def getBareJids(self):
        """Return all bare jids (as unicode) of the roster"""
        return self._jids.keys()

    def isJidInRoster(self, entity_jid):
        """Return True if jid is in roster"""
        return entity_jid.userhostJID() in self._jids

    def getItems(self):
        """Return all items of the roster"""
        return self._jids.values()

    def getJidsFromGroup(self, group):
        try:
            return self._groups[group]
        except KeyError:
            raise exceptions.UnknownGroupError


class SatPresenceProtocol(xmppim.PresenceClientProtocol):

    def __init__(self, host):
        xmppim.PresenceClientProtocol.__init__(self)
        self.host = host

    def send(self, obj):
        if not self.host.trigger.point("Presence send", self.parent, obj):
            return
        super(SatPresenceProtocol, self).send(obj)

    def availableReceived(self, entity, show=None, statuses=None, priority=0):
        log.debug(_("presence update for [%(entity)s] (available, show=%(show)s statuses=%(statuses)s priority=%(priority)d)") % {'entity': entity, 'show': show, 'statuses': statuses, 'priority': priority})

        if not statuses:
            statuses = {}

        if None in statuses:  # we only want string keys
            statuses["default"] = statuses[None]
            del statuses[None]

        self.host.memory.setPresenceStatus(entity, show or "",
                                           int(priority), statuses,
                                           self.parent.profile)

        # uncomment these two lines if you need the trigger
        #if not self.host.trigger.point("presenceReceived", entity, "unavailable", 0, statuses, self.parent.profile):
        #    return

        # now it's time to notify frontends
        self.host.bridge.presenceUpdate(entity.full(), show or "",
                                        int(priority), statuses,
                                        self.parent.profile)

    def unavailableReceived(self, entity, statuses=None):
        log.debug(_("presence update for [%(entity)s] (unavailable, statuses=%(statuses)s)") % {'entity': entity, 'statuses': statuses})

        if not statuses:
            statuses = {}

        if None in statuses:  # we only want string keys
            statuses["default"] = statuses[None]
            del statuses[None]
        self.host.memory.setPresenceStatus(entity, "unavailable", 0, statuses, self.parent.profile)

        if not self.host.trigger.point("presenceReceived", entity, "unavailable", 0, statuses, self.parent.profile):
            return

        # now it's time to notify frontends
        self.host.bridge.presenceUpdate(entity.full(), "unavailable", 0, statuses, self.parent.profile)

    def available(self, entity=None, show=None, statuses=None, priority=None):
        if priority is None:
            try:
                priority = int(self.host.memory.getParamA("Priority", "Connection", profile_key=self.parent.profile))
            except ValueError:
                priority = 0

        if statuses is None:
            statuses = {}

        # default for us is None for wokkel
        # so we must temporarily switch to wokkel's convention...
        if 'default' in statuses:
            statuses[None] = statuses['default']
            del statuses['default']

        presence_elt = xmppim.AvailablePresence(entity, show, statuses, priority)

        # ... before switching back
        if None in statuses:
            statuses['default'] = statuses[None]
            del statuses[None]

        if not self.host.trigger.point("presence_available", presence_elt, self.parent):
            return
        self.send(presence_elt)

    def subscribed(self, entity):
        xmppim.PresenceClientProtocol.subscribed(self, entity)
        self.host.memory.delWaitingSub(entity.userhost(), self.parent.profile)
        item = self.parent.roster.getItem(entity)
        if not item or not item.subscriptionTo:  # we automatically subscribe to 'to' presence
            log.debug(_('sending automatic "from" subscription request'))
            self.subscribe(entity)

    def unsubscribed(self, entity):
        xmppim.PresenceClientProtocol.unsubscribed(self, entity)
        self.host.memory.delWaitingSub(entity.userhost(), self.parent.profile)

    def subscribedReceived(self, entity):
        log.debug(_("subscription approved for [%s]") % entity.userhost())
        self.host.bridge.subscribe('subscribed', entity.userhost(), self.parent.profile)

    def unsubscribedReceived(self, entity):
        log.debug(_("unsubscription confirmed for [%s]") % entity.userhost())
        self.host.bridge.subscribe('unsubscribed', entity.userhost(), self.parent.profile)

    def subscribeReceived(self, entity):
        log.debug(_("subscription request from [%s]") % entity.userhost())
        item = self.parent.roster.getItem(entity)
        if item and item.subscriptionTo:
            # We automatically accept subscription if we are already subscribed to contact presence
            log.debug(_('sending automatic subscription acceptance'))
            self.subscribed(entity)
        else:
            self.host.memory.addWaitingSub('subscribe', entity.userhost(), self.parent.profile)
            self.host.bridge.subscribe('subscribe', entity.userhost(), self.parent.profile)

    def unsubscribeReceived(self, entity):
        log.debug(_("unsubscription asked for [%s]") % entity.userhost())
        item = self.parent.roster.getItem(entity)
        if item and item.subscriptionFrom:  # we automatically remove contact
            log.debug(_('automatic contact deletion'))
            self.host.delContact(entity, self.parent.profile)
        self.host.bridge.subscribe('unsubscribe', entity.userhost(), self.parent.profile)


class SatDiscoProtocol(disco.DiscoClientProtocol):
    def __init__(self, host):
        disco.DiscoClientProtocol.__init__(self)


class SatFallbackHandler(generic.FallbackHandler):
    def __init__(self, host):
        generic.FallbackHandler.__init__(self)

    def iqFallback(self, iq):
        if iq.handled is True:
            return
        log.debug(u"iqFallback: xml = [%s]" % (iq.toXml()))
        generic.FallbackHandler.iqFallback(self, iq)


class RegisteringAuthenticator(xmlstream.ConnectAuthenticator):

    def __init__(self, host, jabber_host, user_login, user_pass, email, deferred, profile):
        xmlstream.ConnectAuthenticator.__init__(self, jabber_host)
        self.host = host
        self.jabber_host = jabber_host
        self.user_login = user_login
        self.user_pass = user_pass
        self.user_email = email
        self.deferred = deferred
        self.profile = profile
        log.debug(_("Registration asked for %(user)s@%(host)s") % {'user': user_login, 'host': jabber_host})

    def connectionMade(self):
        log.debug(_("Connection made with %s" % self.jabber_host))
        self.xmlstream.namespace = "jabber:client"
        self.xmlstream.sendHeader()

        iq = compat.IQ(self.xmlstream, 'set')
        iq["to"] = self.jabber_host
        query = iq.addElement(('jabber:iq:register', 'query'))
        _user = query.addElement('username')
        _user.addContent(self.user_login)
        _pass = query.addElement('password')
        _pass.addContent(self.user_pass)
        if self.user_email:
            _email = query.addElement('email')
            _email.addContent(self.user_email)
        d = iq.send(self.jabber_host).addCallbacks(self.registrationAnswer, self.registrationFailure)
        d.chainDeferred(self.deferred)

    def registrationAnswer(self, answer):
        log.debug(_("Registration answer: %s") % answer.toXml())
        self.xmlstream.sendFooter()

    def registrationFailure(self, failure):
        log.info(_("Registration failure: %s") % str(failure.value))
        self.xmlstream.sendFooter()
        raise failure.value


class SatVersionHandler(generic.VersionHandler):

    def getDiscoInfo(self, requestor, target, node):
        #XXX: We need to work around wokkel's behaviour (namespace not added if there is a
        # node) as it cause issues with XEP-0115 & PEP (XEP-0163): there is a node when server
        # ask for disco info, and not when we generate the key, so the hash is used with different
        # disco features, and when the server (seen on ejabberd) generate its own hash for security check
        # it reject our features (resulting in e.g. no notification on PEP)
        return generic.VersionHandler.getDiscoInfo(self, requestor, target, None)

class SatIdentityHandler(XMPPHandler):
    """ Manage disco Identity of SàT. Currently, we use "client/pc/Salut à Toi", but as
    SàT is multi-frontends and can be used on mobile devices, as a bot, with a web frontend,
    etc, we should implement a way to dynamically update identities through the bridge """
    #TODO: dynamic identity update (see docstring). Note that a XMPP entity can have several identities
    implements(iwokkel.IDisco)

    def getDiscoInfo(self, requestor, target, nodeIdentifier=''):
        return [disco.DiscoIdentity(u"client", u"pc", C.APP_NAME)]

    def getDiscoItems(self, requestor, target, nodeIdentifier=''):
        return []
