#!/usr/bin/python
#-*- coding: utf-8 -*-

# SAT communication bridge
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
from bridge_frontend import BridgeFrontend, BridgeException
import dbus
from sat.core.log import getLogger
log = getLogger(__name__)
from sat.core.exceptions import BridgeExceptionNoService, BridgeInitError

from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

import ast

const_INT_PREFIX = "org.goffi.SAT"  # Interface prefix
const_ERROR_PREFIX = const_INT_PREFIX + ".error"
const_OBJ_PATH = '/org/goffi/SAT/bridge'
const_CORE_SUFFIX = ".core"
const_PLUGIN_SUFFIX = ".plugin"
const_TIMEOUT = 120


def dbus_to_bridge_exception(dbus_e):
    """Convert a DBusException to a BridgeException.

    @param dbus_e (DBusException)
    @return: BridgeException
    """
    full_name = dbus_e.get_dbus_name()
    if full_name.startswith(const_ERROR_PREFIX):
        name = dbus_e.get_dbus_name()[len(const_ERROR_PREFIX) + 1:]
    else:
        name = full_name
    # XXX: dbus_e.args doesn't contain the original DBusException args, but we
    # receive its serialized form in dbus_e.args[0]. From that we can rebuild
    # the original arguments list thanks to ast.literal_eval (secure eval).
    message = dbus_e.get_dbus_message()  # similar to dbus_e.args[0]
    try:
        message, condition = ast.literal_eval(message)
    except (SyntaxError, ValueError, TypeError):
        condition = ''
    return BridgeException(name, message, condition)


class DBusBridgeFrontend(BridgeFrontend):
    def __init__(self):
        try:
            self.sessions_bus = dbus.SessionBus()
            self.db_object = self.sessions_bus.get_object(const_INT_PREFIX,
                                                          const_OBJ_PATH)
            self.db_core_iface = dbus.Interface(self.db_object,
                                                dbus_interface=const_INT_PREFIX + const_CORE_SUFFIX)
            self.db_plugin_iface = dbus.Interface(self.db_object,
                                                  dbus_interface=const_INT_PREFIX + const_PLUGIN_SUFFIX)
        except dbus.exceptions.DBusException, e:
            if e._dbus_error_name == 'org.freedesktop.DBus.Error.ServiceUnknown':
                raise BridgeExceptionNoService
            elif e._dbus_error_name == 'org.freedesktop.DBus.Error.NotSupported':
                log.error(_(u"D-Bus is not launched, please see README to see instructions on how to launch it"))
                raise BridgeInitError
            else:
                raise e
        #props = self.db_core_iface.getProperties()

    def register(self, functionName, handler, iface="core"):
        if iface == "core":
            self.db_core_iface.connect_to_signal(functionName, handler)
        elif iface == "plugin":
            self.db_plugin_iface.connect_to_signal(functionName, handler)
        else:
            log.error(_('Unknown interface'))

    def __getattribute__(self, name):
        """ usual __getattribute__ if the method exists, else try to find a plugin method """
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            # The attribute is not found, we try the plugin proxy to find the requested method

            def getPluginMethod(*args, **kwargs):
                # We first check if we have an async call. We detect this in two ways:
                #   - if we have the 'callback' and 'errback' keyword arguments
                #   - or if the last two arguments are callable

                async = False

                if kwargs:
                    if 'callback' in kwargs and 'errback' in kwargs:
                        async = True
                        _callback = kwargs.pop('callback')
                        _errback = kwargs.pop('errback')
                elif len(args) >= 2 and callable(args[-1]) and callable(args[-2]):
                    async = True
                    args = list(args)
                    _errback = args.pop()
                    _callback = args.pop()

                method = getattr(self.db_plugin_iface, name)

                if async:
                    kwargs['timeout'] = const_TIMEOUT
                    kwargs['reply_handler'] = _callback
                    kwargs['error_handler'] = lambda err: _errback(dbus_to_bridge_exception(err))

                return method(*args, **kwargs)

            return getPluginMethod
    def addContact(self, entity_jid, profile_key="@DEFAULT@"):
        return self.db_core_iface.addContact(entity_jid, profile_key)

    def asyncConnect(self, profile_key="@DEFAULT@", password='', callback=None, errback=None):
        return self.db_core_iface.asyncConnect(profile_key, password, timeout=const_TIMEOUT, reply_handler=callback, error_handler=lambda err:errback(dbus_to_bridge_exception(err)))

    def asyncCreateProfile(self, profile, password='', callback=None, errback=None):
        return self.db_core_iface.asyncCreateProfile(profile, password, timeout=const_TIMEOUT, reply_handler=callback, error_handler=lambda err:errback(dbus_to_bridge_exception(err)))

    def asyncDeleteProfile(self, profile, callback=None, errback=None):
        return self.db_core_iface.asyncDeleteProfile(profile, timeout=const_TIMEOUT, reply_handler=callback, error_handler=lambda err:errback(dbus_to_bridge_exception(err)))

    def asyncGetParamA(self, name, category, attribute="value", security_limit=-1, profile_key="@DEFAULT@", callback=None, errback=None):
        return unicode(self.db_core_iface.asyncGetParamA(name, category, attribute, security_limit, profile_key, timeout=const_TIMEOUT, reply_handler=callback, error_handler=lambda err:errback(dbus_to_bridge_exception(err))))

    def confirmationAnswer(self, id, accepted, data, profile):
        return self.db_core_iface.confirmationAnswer(id, accepted, data, profile)

    def delContact(self, entity_jid, profile_key="@DEFAULT@"):
        return self.db_core_iface.delContact(entity_jid, profile_key)

    def discoInfos(self, entity_jid, profile_key, callback=None, errback=None):
        return self.db_core_iface.discoInfos(entity_jid, profile_key, timeout=const_TIMEOUT, reply_handler=callback, error_handler=lambda err:errback(dbus_to_bridge_exception(err)))

    def discoItems(self, entity_jid, profile_key, callback=None, errback=None):
        return self.db_core_iface.discoItems(entity_jid, profile_key, timeout=const_TIMEOUT, reply_handler=callback, error_handler=lambda err:errback(dbus_to_bridge_exception(err)))

    def disconnect(self, profile_key="@DEFAULT@"):
        return self.db_core_iface.disconnect(profile_key)

    def getConfig(self, section, name):
        return unicode(self.db_core_iface.getConfig(section, name))

    def getContacts(self, profile_key="@DEFAULT@"):
        return self.db_core_iface.getContacts(profile_key)

    def getContactsFromGroup(self, group, profile_key="@DEFAULT@"):
        return self.db_core_iface.getContactsFromGroup(group, profile_key)

    def getEntityData(self, jid, keys, profile):
        return self.db_core_iface.getEntityData(jid, keys, profile)

    def getHistory(self, from_jid, to_jid, limit, between=True, profile="@NONE@", callback=None, errback=None):
        return self.db_core_iface.getHistory(from_jid, to_jid, limit, between, profile, timeout=const_TIMEOUT, reply_handler=callback, error_handler=lambda err:errback(dbus_to_bridge_exception(err)))

    def getLastResource(self, contact_jid, profile_key="@DEFAULT@"):
        return unicode(self.db_core_iface.getLastResource(contact_jid, profile_key))

    def getMenuHelp(self, menu_id, language):
        return unicode(self.db_core_iface.getMenuHelp(menu_id, language))

    def getMenus(self, language, security_limit):
        return self.db_core_iface.getMenus(language, security_limit)

    def getParamA(self, name, category, attribute="value", profile_key="@DEFAULT@"):
        return unicode(self.db_core_iface.getParamA(name, category, attribute, profile_key))

    def getParams(self, security_limit=-1, app='', profile_key="@DEFAULT@", callback=None, errback=None):
        return unicode(self.db_core_iface.getParams(security_limit, app, profile_key, timeout=const_TIMEOUT, reply_handler=callback, error_handler=lambda err:errback(dbus_to_bridge_exception(err))))

    def getParamsCategories(self, ):
        return self.db_core_iface.getParamsCategories()

    def getParamsForCategory(self, category, security_limit=-1, app='', profile_key="@DEFAULT@", callback=None, errback=None):
        return unicode(self.db_core_iface.getParamsForCategory(category, security_limit, app, profile_key, timeout=const_TIMEOUT, reply_handler=callback, error_handler=lambda err:errback(dbus_to_bridge_exception(err))))

    def getParamsUI(self, security_limit=-1, app='', profile_key="@DEFAULT@", callback=None, errback=None):
        return unicode(self.db_core_iface.getParamsUI(security_limit, app, profile_key, timeout=const_TIMEOUT, reply_handler=callback, error_handler=lambda err:errback(dbus_to_bridge_exception(err))))

    def getPresenceStatuses(self, profile_key="@DEFAULT@"):
        return self.db_core_iface.getPresenceStatuses(profile_key)

    def getProfileName(self, profile_key="@DEFAULT@"):
        return unicode(self.db_core_iface.getProfileName(profile_key))

    def getProfilesList(self, ):
        return self.db_core_iface.getProfilesList()

    def getProgress(self, id, profile):
        return self.db_core_iface.getProgress(id, profile)

    def getReady(self, callback=None, errback=None):
        return self.db_core_iface.getReady(timeout=const_TIMEOUT, reply_handler=callback, error_handler=lambda err:errback(dbus_to_bridge_exception(err)))

    def getVersion(self, ):
        return unicode(self.db_core_iface.getVersion())

    def getWaitingConf(self, profile_key):
        return self.db_core_iface.getWaitingConf(profile_key)

    def getWaitingSub(self, profile_key="@DEFAULT@"):
        return self.db_core_iface.getWaitingSub(profile_key)

    def isConnected(self, profile_key="@DEFAULT@"):
        return self.db_core_iface.isConnected(profile_key)

    def launchAction(self, callback_id, data, profile_key="@DEFAULT@", callback=None, errback=None):
        return self.db_core_iface.launchAction(callback_id, data, profile_key, timeout=const_TIMEOUT, reply_handler=callback, error_handler=lambda err:errback(dbus_to_bridge_exception(err)))

    def loadParamsTemplate(self, filename):
        return self.db_core_iface.loadParamsTemplate(filename)

    def paramsRegisterApp(self, xml, security_limit=-1, app=''):
        return self.db_core_iface.paramsRegisterApp(xml, security_limit, app)

    def saveParamsTemplate(self, filename):
        return self.db_core_iface.saveParamsTemplate(filename)

    def sendMessage(self, to_jid, message, subject='', mess_type="auto", extra={}, profile_key="@NONE@", callback=None, errback=None):
        return self.db_core_iface.sendMessage(to_jid, message, subject, mess_type, extra, profile_key, timeout=const_TIMEOUT, reply_handler=callback, error_handler=lambda err:errback(dbus_to_bridge_exception(err)))

    def setParam(self, name, value, category, security_limit=-1, profile_key="@DEFAULT@"):
        return self.db_core_iface.setParam(name, value, category, security_limit, profile_key)

    def setPresence(self, to_jid='', show='', statuses={}, profile_key="@DEFAULT@"):
        return self.db_core_iface.setPresence(to_jid, show, statuses, profile_key)

    def subscription(self, sub_type, entity, profile_key="@DEFAULT@"):
        return self.db_core_iface.subscription(sub_type, entity, profile_key)

    def updateContact(self, entity_jid, name, groups, profile_key="@DEFAULT@"):
        return self.db_core_iface.updateContact(entity_jid, name, groups, profile_key)
