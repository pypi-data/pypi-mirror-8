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

from sat.core import exceptions
from sat.core.constants import Const as C
from sat.memory.crypto import BlockCipher, PasswordHasher
from xml.dom import minidom, NotFoundErr
from sat.core.log import getLogger
log = getLogger(__name__)
from twisted.internet import defer
from twisted.python.failure import Failure
from sat.tools.xml_tools import paramsXML2XMLUI


class Params(object):
    """This class manage parameters with xml"""
    ### TODO: add desciption in params

    #TODO: move Watched in a plugin
    #TODO: when priority is changed, a new presence stanza must be emitted
    #TODO: int type (Priority should be int instead of string)
    default_xml = u"""
    <params>
    <general>
    </general>
    <individual>
        <category name="General" label="%(category_general)s">
            <param name="Password" value="" type="password" />
        </category>
        <category name="Connection" label="%(category_connection)s">
            <param name="JabberID" value="name@example.org/SàT" type="string" />
            <param name="Password" value="" type="password" />
            <param name="Priority" value="50" type="string" />
            <param name="%(force_server_param)s" value="" type="string" />
            <param name="%(force_port_param)s" value="" type="string" />
            <param name="NewAccount" label="%(label_NewAccount)s" type="button" callback_id="registerNewAccount"/>
            <param name="autoconnect" label="%(label_autoconnect)s" value="true" type="bool" />
            <param name="autodisconnect" label="%(label_autodisconnect)s" value="false"  type="bool" />
        </category>
        <category name="Misc" label="%(category_misc)s">
            <param name="Watched" value="test@Jabber.goffi.int" type="string" />
        </category>
    </individual>
    </params>
    """ % {
        'category_general': _("General"),
        'category_connection': _("Connection"),
        'label_NewAccount': _("Register new account"),
        'label_autoconnect': _('Connect on frontend startup'),
        'label_autodisconnect': _('Disconnect on frontend closure'),
        'category_misc': _("Misc"),
        'force_server_param': C.FORCE_SERVER_PARAM,
        'force_port_param': C.FORCE_PORT_PARAM,
    }

    def load_default_params(self):
        self.dom = minidom.parseString(Params.default_xml.encode('utf-8'))

    def _mergeParams(self, source_node, dest_node):
        """Look for every node in source_node and recursively copy them to dest if they don't exists"""

        def getNodesMap(children):
            ret = {}
            for child in children:
                if child.nodeType == child.ELEMENT_NODE:
                    ret[(child.tagName, child.getAttribute('name'))] = child
            return ret
        source_map = getNodesMap(source_node.childNodes)
        dest_map = getNodesMap(dest_node.childNodes)
        source_set = set(source_map.keys())
        dest_set = set(dest_map.keys())
        to_add = source_set.difference(dest_set)

        for node_key in to_add:
            dest_node.appendChild(source_map[node_key].cloneNode(True))

        to_recurse = source_set - to_add
        for node_key in to_recurse:
            self._mergeParams(source_map[node_key], dest_map[node_key])

    def load_xml(self, xml_file):
        """Load parameters template from xml file"""
        self.dom = minidom.parse(xml_file)
        default_dom = minidom.parseString(Params.default_xml.encode('utf-8'))
        self._mergeParams(default_dom.documentElement, self.dom.documentElement)

    def loadGenParams(self):
        """Load general parameters data from storage
        @return: deferred triggered once params are loaded"""
        return self.storage.loadGenParams(self.params_gen)

    def loadIndParams(self, profile, cache=None):
        """Load individual parameters
        set self.params cache or a temporary cache
        @param profile: profile to load (*must exist*)
        @param cache: if not None, will be used to store the value, as a short time cache
        @return: deferred triggered once params are loaded"""
        if cache is None:
            self.params[profile] = {}
        return self.storage.loadIndParams(self.params[profile] if cache is None else cache, profile)

    def purgeProfile(self, profile):
        """Remove cache data of a profile
        @param profile: %(doc_profile)s"""
        try:
            del self.params[profile]
        except KeyError:
            log.error(_("Trying to purge cache of a profile not in memory: [%s]") % profile)

    def save_xml(self, filename):
        """Save parameters template to xml file"""
        with open(filename, 'wb') as xml_file:
            xml_file.write(self.dom.toxml('utf-8'))

    def __init__(self, host, storage):
        log.debug("Parameters init")
        self.host = host
        self.storage = storage
        self.default_profile = None
        self.params = {}
        self.params_gen = {}

    def asyncCreateProfile(self, profile):
        """Create a new profile
        @param profile: name of the profile
        @param callback: called when the profile actually exists in database and memory
        @return: a Deferred instance
        """
        if self.storage.hasProfile(profile):
            log.info(_('The profile name already exists'))
            return defer.fail(Failure(exceptions.ConflictError))
        if not self.host.trigger.point("ProfileCreation", profile):
            return defer.fail(Failure(exceptions.CancelError))
        return self.storage.createProfile(profile)

    def asyncDeleteProfile(self, profile, force=False):
        """Delete an existing profile

        @param profile: name of the profile
        @param force: force the deletion even if the profile is connected.
        To be used for direct calls only (not through the bridge).
        @return: a Deferred instance
        """
        if not self.storage.hasProfile(profile):
            log.info(_('Trying to delete an unknown profile'))
            return defer.fail(Failure(exceptions.ProfileUnknownError))
        if self.host.isConnected(profile):
            if force:
                self.host.disconnect(profile)
            else:
                log.info(_("Trying to delete a connected profile"))
                return defer.fail(Failure(exceptions.ConnectedProfileError))
        return self.storage.deleteProfile(profile)

    def getProfileName(self, profile_key, return_profile_keys = False):
        """return profile according to profile_key

        @param profile_key: profile name or key which can be
                            @ALL@ for all profiles
                            @DEFAULT@ for default profile
        @param return_profile_keys: if True, return unmanaged profile keys (like "@ALL@"). This keys must be managed by the caller
        @return: requested profile name or emptry string if it doesn't exist"""
        if profile_key == '@DEFAULT@':
            default = self.host.memory.memory_data.get('Profile_default')
            if not default:
                log.info(_('No default profile, returning first one'))  # TODO: manage real default profile
                try:
                    default = self.host.memory.memory_data['Profile_default'] = self.storage.getProfilesList()[0]
                except IndexError:
                    log.info(_('No profile exist yet'))
                    return ""
            return default  # FIXME: temporary, must use real default value, and fallback to first one if it doesn't exists
        elif profile_key == C.PROF_KEY_NONE:
            raise exceptions.ProfileNotSetError
        elif return_profile_keys and profile_key in ["@ALL@"]:
            return profile_key # this value must be managed by the caller
        if not self.storage.hasProfile(profile_key):
            log.error(_('Trying to access an unknown profile (%s)') % profile_key)
            return "" # FIXME: raise exceptions.ProfileUnknownError here (must be well checked, this method is used in lot of places)
        return profile_key

    def __get_unique_node(self, parent, tag, name):
        """return node with given tag
        @param parent: parent of nodes to check (e.g. documentElement)
        @param tag: tag to check (e.g. "category")
        @param name: name to check (e.g. "JID")
        @return: node if it exist or None
        """
        for node in parent.childNodes:
            if node.nodeName == tag and node.getAttribute("name") == name:
                #the node already exists
                return node
        #the node is new
        return None

    def updateParams(self, xml, security_limit=C.NO_SECURITY_LIMIT, app=''):
        """import xml in parameters, update if the param already exists
        If security_limit is specified and greater than -1, the parameters
        that have a security level greater than security_limit are skipped.
        @param xml: parameters in xml form
        @param security_limit: -1 means no security, 0 is the maximum security then the higher the less secure
        @param app: name of the frontend registering the parameters or empty value
        """
        src_parent = minidom.parseString(xml.encode('utf-8')).documentElement

        def pre_process_app_node(src_parent, security_limit, app):
            """Parameters that are registered from a frontend must be checked"""
            to_remove = []
            for type_node in src_parent.childNodes:
                if type_node.nodeName != C.INDIVIDUAL:
                    to_remove.append(type_node)  # accept individual parameters only
                    continue
                for cat_node in type_node.childNodes:
                    if cat_node.nodeName != 'category':
                        to_remove.append(cat_node)
                        continue
                    to_remove_count = 0  # count the params to be removed from current category
                    for node in cat_node.childNodes:
                        if node.nodeName != "param" or not self.checkSecurityLimit(node, security_limit):
                            to_remove.append(node)
                            to_remove_count += 1
                            continue
                        node.setAttribute('app', app)
                    if len(cat_node.childNodes) == to_remove_count:  # remove empty category
                        for dummy in xrange(0, to_remove_count):
                            to_remove.pop()
                        to_remove.append(cat_node)
            for node in to_remove:
                node.parentNode.removeChild(node)

        def import_node(tgt_parent, src_parent):
            for child in src_parent.childNodes:
                if child.nodeName == '#text':
                    continue
                node = self.__get_unique_node(tgt_parent, child.nodeName, child.getAttribute("name"))
                if not node:  # The node is new
                    tgt_parent.appendChild(child.cloneNode(True))
                else:
                    if child.nodeName == "param":
                        # The child updates an existing parameter, we replace the node
                        tgt_parent.replaceChild(child, node)
                    else:
                        # the node already exists, we recurse 1 more level
                        import_node(node, child)

        if app:
            pre_process_app_node(src_parent, security_limit, app)
        import_node(self.dom.documentElement, src_parent)

    def paramsRegisterApp(self, xml, security_limit, app):
        """Register frontend's specific parameters
        If security_limit is specified and greater than -1, the parameters
        that have a security level greater than security_limit are skipped.
        @param xml: XML definition of the parameters to be added
        @param security_limit: -1 means no security, 0 is the maximum security then the higher the less secure
        @param app: name of the frontend registering the parameters
        """
        if not app:
            log.warning(_("Trying to register frontends parameters with no specified app: aborted"))
            return
        if not hasattr(self, "frontends_cache"):
            self.frontends_cache = []
        if app in self.frontends_cache:
            log.debug(_("Trying to register twice frontends parameters for %(app)s: aborted" % {"app": app}))
            return
        self.frontends_cache.append(app)
        self.updateParams(xml, security_limit, app)
        log.debug("Frontends parameters registered for %(app)s" % {'app': app})

    def __default_ok(self, value, name, category):
        #FIXME: will not work with individual parameters
        self.setParam(name, value, category)

    def __default_ko(self, failure, name, category):
        log.error(_("Can't determine default value for [%(category)s/%(name)s]: %(reason)s") % {'category': category, 'name': name, 'reason': str(failure.value)})

    def setDefault(self, name, category, callback, errback=None):
        """Set default value of parameter
        'default_cb' attibute of parameter must be set to 'yes'
        @param name: name of the parameter
        @param category: category of the parameter
        @param callback: must return a string with the value (use deferred if needed)
        @param errback: must manage the error with args failure, name, category
        """
        #TODO: send signal param update if value changed
        #TODO: manage individual paramaters
        log.debug ("setDefault called for %(category)s/%(name)s" % {"category": category, "name": name})
        node = self._getParamNode(name, category, '@ALL@')
        if not node:
            log.error(_("Requested param [%(name)s] in category [%(category)s] doesn't exist !") % {'name': name, 'category': category})
            return
        if node[1].getAttribute('default_cb') == 'yes':
            # del node[1].attributes['default_cb'] # default_cb is not used anymore as a flag to know if we have to set the default value,
                                                   # and we can still use it later e.g. to call a generic setDefault method
            value = self._getParam(category, name, C.GENERAL)
            if value is None: # no value set by the user: we have the default value
                log.debug ("Default value to set, using callback")
                d = defer.maybeDeferred(callback)
                d.addCallback(self.__default_ok, name, category)
                d.addErrback(errback or self.__default_ko, name, category)

    def _getAttr_internal(self, node, attr, value):
        """Get attribute value.

        /!\ This method would return encrypted password values.

        @param node: XML param node
        @param attr: name of the attribute to get (e.g.: 'value' or 'type')
        @param value: user defined value
        @return: str
        """
        if attr == 'value':
            value_to_use = value if value is not None else node.getAttribute(attr)  # we use value (user defined) if it exist, else we use node's default value
            if node.getAttribute('type') == 'bool':
                return value_to_use.lower() not in ('false', '0', 'no')
            elif node.getAttribute('type') == 'list':
                options = [option for option in node.childNodes if option.nodeName == 'option']
                values = [option.getAttribute('value') for option in options]
                if value_to_use not in values:  # value_to_use is probably empty
                    selected = [option for option in options if option.getAttribute('selected') == 'true']
                    cat, param = node.parentNode.getAttribute('name'), node.getAttribute('name')
                    if len(selected) == 1:
                        value_to_use = selected[0].getAttribute('value')
                        log.info(_("Unset parameter (%(cat)s, %(param)s) of type list will use the default option '%(value)s'") %
                                 {'cat': cat, 'param': param, 'value': value_to_use})
                        return value_to_use
                    if len(selected) == 0:
                        log.error(_('Parameter (%(cat)s, %(param)s) of type list has no default option!') % {'cat': cat, 'param': param})
                    else:
                        log.error(_('Parameter (%(cat)s, %(param)s) of type list has more than one default option!') % {'cat': cat, 'param': param})
                    raise exceptions.DataError
            return value_to_use
        return node.getAttribute(attr)

    def _getAttr(self, node, attr, value):
        """Get attribute value (synchronous).

        /!\ This method can not be used to retrieve password values.

        @param node: XML param node
        @param attr: name of the attribute to get (e.g.: 'value' or 'type')
        @param value: user defined value
        @return: str
        """
        if attr == 'value' and node.getAttribute('type') == 'password':
            raise exceptions.InternalError('To retrieve password values, use _asyncGetAttr instead of _getAttr')
        return self._getAttr_internal(node, attr, value)

    def _asyncGetAttr(self, node, attr, value, profile=None):
        """Get attribute value.

        Profile passwords are returned hashed (if not empty),
        other passwords are returned decrypted (if not empty).

        @param node: XML param node
        @param attr: name of the attribute to get (e.g.: 'value' or 'type')
        @param value: user defined value
        @param profile: %(doc_profile)s
        @return: a deferred str
        """
        value = self._getAttr_internal(node, attr, value)
        if attr != 'value' or node.getAttribute('type') != 'password':
            return defer.succeed(value)
        param_cat = node.parentNode.getAttribute('name')
        param_name = node.getAttribute('name')
        if ((param_cat, param_name) == C.PROFILE_PASS_PATH) or not value:
            return defer.succeed(value)  # profile password and empty passwords are returned "as is"
        if not profile:
            raise exceptions.ProfileUnknownError('The profile is needed to decrypt a password')
        d = self.host.memory.decryptValue(value, profile)

        def gotPlainPassword(password):
            if password is None:  # empty value means empty password, None means decryption failure
                raise exceptions.InternalError(_('The stored password could not be decrypted!'))
            return password

        return d.addCallback(gotPlainPassword)

    def __type_to_string(self, result):
        """ convert result to string, according to its type """
        if isinstance(result, bool):
            return "true" if result else "false"
        return result

    def getStringParamA(self, name, category, attr="value", profile_key=C.PROF_KEY_NONE):
        """ Same as getParamA but for bridge: convert non string value to string """
        return self.__type_to_string(self.getParamA(name, category, attr, profile_key))

    def getParamA(self, name, category, attr="value", profile_key=C.PROF_KEY_NONE):
        """Helper method to get a specific attribute.

        /!\ This method would return encrypted password values,
            to get the plain values you have to use _asyncGetParamA.

       @param name: name of the parameter
       @param category: category of the parameter
       @param attr: name of the attribute (default: "value")
       @param profile: owner of the param (@ALL@ for everyone)
       @return: attribute
       """
        #FIXME: looks really dirty and buggy, need to be reviewed/refactored
        node = self._getParamNode(name, category)
        if not node:
            log.error(_("Requested param [%(name)s] in category [%(category)s] doesn't exist !") % {'name': name, 'category': category})
            raise exceptions.NotFound

        if attr == 'value' and node[1].getAttribute('type') == 'password':
            raise exceptions.InternalError('To retrieve password values, use asyncGetParamA instead of getParamA')

        if node[0] == C.GENERAL:
            value = self._getParam(category, name, C.GENERAL)
            return self._getAttr(node[1], attr, value)

        assert node[0] == C.INDIVIDUAL

        profile = self.getProfileName(profile_key)
        if not profile:
            log.error(_('Requesting a param for an non-existant profile'))
            raise exceptions.ProfileUnknownError

        if profile not in self.params:
            log.error(_('Requesting synchronous param for not connected profile'))
            raise exceptions.NotConnectedProfileError(profile)

        if attr == "value":
            value = self._getParam(category, name, profile=profile)
            return self._getAttr(node[1], attr, value)

    def asyncGetStringParamA(self, name, category, attr="value", security_limit=C.NO_SECURITY_LIMIT, profile_key=C.PROF_KEY_NONE):
        d = self.asyncGetParamA(name, category, attr, security_limit, profile_key)
        d.addCallback(self.__type_to_string)
        return d

    def asyncGetParamA(self, name, category, attr="value", security_limit=C.NO_SECURITY_LIMIT, profile_key=C.PROF_KEY_NONE):
        """Helper method to get a specific attribute.
        @param name: name of the parameter
        @param category: category of the parameter
        @param attr: name of the attribute (default: "value")
        @param profile: owner of the param (@ALL@ for everyone)
        @return: Deferred
        """
        node = self._getParamNode(name, category)
        if not node:
            log.error(_("Requested param [%(name)s] in category [%(category)s] doesn't exist !") % {'name': name, 'category': category})
            return defer.succeed(None)

        if not self.checkSecurityLimit(node[1], security_limit):
            log.warning(_("Trying to get parameter '%(param)s' in category '%(cat)s' without authorization!!!"
                      % {'param': name, 'cat': category}))
            return defer.succeed(None)

        if node[0] == C.GENERAL:
            value = self._getParam(category, name, C.GENERAL)
            return self._asyncGetAttr(node[1], attr, value)

        assert node[0] == C.INDIVIDUAL

        profile = self.getProfileName(profile_key)
        if not profile:
            raise exceptions.InternalError(_('Requesting a param for a non-existant profile'))

        if attr != "value":
            return defer.succeed(node[1].getAttribute(attr))
        try:
            value = self._getParam(category, name, profile=profile)
            return self._asyncGetAttr(node[1], attr, value, profile)
        except exceptions.ProfileNotInCacheError:
            #We have to ask data to the storage manager
            d = self.storage.getIndParam(category, name, profile)
            return d.addCallback(lambda value: self._asyncGetAttr(node[1], attr, value, profile))

    def _getParam(self, category, name, type_=C.INDIVIDUAL, cache=None, profile=C.PROF_KEY_NONE):
        """Return the param, or None if it doesn't exist
        @param category: param category
        @param name: param name
        @param type_: GENERAL or INDIVIDUAL
        @param cache: temporary cache, to use when profile is not logged
        @param profile: the profile name (not profile key, i.e. name and not something like @DEFAULT@)
        @return: param value or None if it doesn't exist
        """
        if type_ == C.GENERAL:
            if (category, name) in self.params_gen:
                return self.params_gen[(category, name)]
            return None  # This general param has the default value
        assert (type_ == C.INDIVIDUAL)
        if profile == C.PROF_KEY_NONE:
            raise exceptions.ProfileNotSetError
        if profile in self.params:
            cache = self.params[profile]  # if profile is in main cache, we use it,
                                          # ignoring the temporary cache
        elif cache is None:  # else we use the temporary cache if it exists, or raise an exception
            raise exceptions.ProfileNotInCacheError
        if (category, name) not in cache:
            return None
        return cache[(category, name)]

    def __constructProfileXml(self, security_limit, app, profile):
        """Construct xml for asked profile, filling values when needed
        /!\ as noticed in doc, don't forget to unlink the minidom.Document
        @param security_limit: NO_SECURITY_LIMIT (-1) to return all the params.
        Otherwise sole the params which have a security level defined *and*
        lower or equal to the specified value are returned.
        @param app: name of the frontend requesting the parameters, or '' to get all parameters
        @param profile: profile name (not key !)
        @return: a deferred that fire a minidom.Document of the profile xml (cf warning above)
        """

        def checkNode(node):
            """Check the node against security_limit and app"""
            return self.checkSecurityLimit(node, security_limit) and self.checkApp(node, app)

        def constructProfile(ignore, profile_cache):
            # init the result document
            prof_xml = minidom.parseString('<params/>')
            cache = {}

            for type_node in self.dom.documentElement.childNodes:
                if type_node.nodeName != C.GENERAL and type_node.nodeName != C.INDIVIDUAL:
                    continue
                # we use all params, general and individual
                for cat_node in type_node.childNodes:
                    if cat_node.nodeName != 'category':
                        continue
                    category = cat_node.getAttribute('name')
                    dest_params = {}  # result (merged) params for category
                    if category not in cache:
                        # we make a copy for the new xml
                        cache[category] = dest_cat = cat_node.cloneNode(True)
                        to_remove = []
                        for node in dest_cat.childNodes:
                            if node.nodeName != "param":
                                continue
                            if not checkNode(node):
                                to_remove.append(node)
                                continue
                            dest_params[node.getAttribute('name')] = node
                        for node in to_remove:
                            dest_cat.removeChild(node)
                        new_node = True
                    else:
                        # It's not a new node, we use the previously cloned one
                        dest_cat = cache[category]
                        new_node = False
                    params = cat_node.getElementsByTagName("param")

                    for param_node in params:
                        # we have to merge new params (we are parsing individual parameters, we have to add them
                        # to the previously parsed general ones)
                        name = param_node.getAttribute('name')
                        if not checkNode(param_node):
                            continue
                        if name not in dest_params:
                            # this is reached when a previous category exists
                            dest_params[name] = param_node.cloneNode(True)
                            dest_cat.appendChild(dest_params[name])

                        profile_value = self._getParam(category,
                                                        name, type_node.nodeName,
                                                        cache=profile_cache, profile=profile)
                        if profile_value is not None:
                            # there is a value for this profile, we must change the default
                            if dest_params[name].getAttribute('type') == 'list':
                                for option in dest_params[name].getElementsByTagName("option"):
                                    if option.getAttribute('value') == profile_value:
                                        option.setAttribute('selected', 'true')
                                    else:
                                        try:
                                            option.removeAttribute('selected')
                                        except NotFoundErr:
                                            pass
                            else:
                                dest_params[name].setAttribute('value', profile_value)
                    if new_node:
                        prof_xml.documentElement.appendChild(dest_cat)

            to_remove = []
            for cat_node in prof_xml.documentElement.childNodes:
                # we remove empty categories
                if cat_node.getElementsByTagName("param").length == 0:
                    to_remove.append(cat_node)
            for node in to_remove:
                prof_xml.documentElement.removeChild(node)
            return prof_xml

        if profile in self.params:
            d = defer.succeed(None)
            profile_cache = self.params[profile]
        else:
            #profile is not in cache, we load values in a short time cache
            profile_cache = {}
            d = self.loadIndParams(profile, profile_cache)

        return d.addCallback(constructProfile, profile_cache)

    def getParamsUI(self, security_limit, app, profile_key):
        """
        @param security_limit: NO_SECURITY_LIMIT (-1) to return all the params.
        Otherwise sole the params which have a security level defined *and*
        lower or equal to the specified value are returned.
        @param app: name of the frontend requesting the parameters, or '' to get all parameters
        @param profile_key: Profile key which can be either a magic (eg: @DEFAULT@) or the name of an existing profile.
        @return: a SàT XMLUI for parameters
        """
        profile = self.getProfileName(profile_key)
        if not profile:
            log.error(_("Asking params for inexistant profile"))
            return ""
        d = self.getParams(security_limit, app, profile)
        return d.addCallback(lambda param_xml: paramsXML2XMLUI(param_xml))

    def getParams(self, security_limit, app, profile_key):
        """Construct xml for asked profile, take params xml as skeleton
        @param security_limit: NO_SECURITY_LIMIT (-1) to return all the params.
        Otherwise sole the params which have a security level defined *and*
        lower or equal to the specified value are returned.
        @param app: name of the frontend requesting the parameters, or '' to get all parameters
        @param profile_key: Profile key which can be either a magic (eg: @DEFAULT@) or the name of an existing profile.
        @return: XML of parameters
        """
        profile = self.getProfileName(profile_key)
        if not profile:
            log.error(_("Asking params for inexistant profile"))
            return defer.succeed("")

        def returnXML(prof_xml):
            return_xml = prof_xml.toxml()
            prof_xml.unlink()
            return '\n'.join((line for line in return_xml.split('\n') if line))

        return self.__constructProfileXml(security_limit, app, profile).addCallback(returnXML)

    def getParamsForCategory(self, category, security_limit, app, profile_key):
        """
        @param category: the desired category
        @param security_limit: NO_SECURITY_LIMIT (-1) to return all the params.
        Otherwise sole the params which have a security level defined *and*
        lower or equal to the specified value are returned.
        @param app: name of the frontend requesting the parameters, or '' to get all parameters
        @param profile_key: Profile key which can be either a magic (eg: @DEFAULT@) or the name of an existing profile.
        @return: node's xml for selected category
        """
        #TODO: manage category of general type (without existant profile)
        profile = self.getProfileName(profile_key)
        if not profile:
            log.error(_("Asking params for inexistant profile"))
            return ""

        def returnCategoryXml(prof_xml):
            for node in prof_xml.getElementsByTagName("category"):
                if node.nodeName == "category" and node.getAttribute("name") == category:
                    result = node.toxml()
                    prof_xml.unlink()
                    return result

            prof_xml.unlink()
            return "<category />"

        d = self.__constructProfileXml(security_limit, app, profile)
        return d.addCallback(returnCategoryXml)

    def _getParamNode(self, name, category, type_="@ALL@"):  # FIXME: is type_ useful ?
        """Return a node from the param_xml
        @param name: name of the node
        @param category: category of the node
        @param type_: keyword for search:
                                    @ALL@ search everywhere
                                    @GENERAL@ only search in general type
                                    @INDIVIDUAL@ only search in individual type
        @return: a tuple (node type, node) or None if not found"""

        for type_node in self.dom.documentElement.childNodes:
            if (((type_ == "@ALL@" or type_ == "@GENERAL@") and type_node.nodeName == C.GENERAL)
                    or ((type_ == "@ALL@" or type_ == "@INDIVIDUAL@") and type_node.nodeName == C.INDIVIDUAL)):
                for node in type_node.getElementsByTagName('category'):
                    if node.getAttribute("name") == category:
                        params = node.getElementsByTagName("param")
                        for param in params:
                            if param.getAttribute("name") == name:
                                return (type_node.nodeName, param)
        return None

    def getParamsCategories(self):
        """return the categories availables"""
        categories = []
        for cat in self.dom.getElementsByTagName("category"):
            name = cat.getAttribute("name")
            if name not in categories:
                categories.append(cat.getAttribute("name"))
        return categories

    def setParam(self, name, value, category, security_limit=C.NO_SECURITY_LIMIT, profile_key=C.PROF_KEY_NONE):
        """Set a parameter, return None if the parameter is not in param xml.

        Parameter of type 'password' that are not the SàT profile password are
        stored encrypted (if not empty). The profile password is stored hashed
        (if not empty).

        @param name (str): the parameter name
        @param value (str): the new value
        @param category (str): the parameter category
        @param security_limit (int)
        @param profile_key (str): %(doc_profile_key)s
        @return: a deferred None value when everything is done
        """
        if profile_key != C.PROF_KEY_NONE:
            profile = self.getProfileName(profile_key)
            if not profile:
                log.error(_('Trying to set parameter for an unknown profile'))
                raise exceptions.ProfileUnknownError

        node = self._getParamNode(name, category, '@ALL@')
        if not node:
            log.error(_('Requesting an unknown parameter (%(category)s/%(name)s)')
                  % {'category': category, 'name': name})
            return defer.succeed(None)

        if not self.checkSecurityLimit(node[1], security_limit):
            log.warning(_("Trying to set parameter '%(param)s' in category '%(cat)s' without authorization!!!"
                          % {'param': name, 'cat': category}))
            return defer.succeed(None)

        type_ = node[1].getAttribute("type")
        log.info(_("Setting parameter (%(category)s, %(name)s) = %(value)s") %
                 {'category': category, 'name': name, 'value': value if type_ != 'password' else '********'})

        if node[0] == C.GENERAL:
            self.params_gen[(category, name)] = value
            self.storage.setGenParam(category, name, value)
            for profile in self.storage.getProfilesList():
                if self.host.isConnected(profile):
                    self.host.bridge.paramUpdate(name, value, category, profile)
                    self.host.trigger.point("paramUpdateTrigger", name, value, category, node[0], profile)
            return defer.succeed(None)

        assert (node[0] == C.INDIVIDUAL)
        assert (profile_key != C.PROF_KEY_NONE)

        d_list = []
        if type_ == "button":
            log.debug("Clicked param button %s" % node.toxml())
            return defer.succeed(None)
        d = defer.succeed(value)
        if type_ == "password":
            try:
                personal_key = self.host.memory.auth_sessions.profileGetUnique(profile)[C.MEMORY_CRYPTO_KEY]
            except TypeError:
                raise exceptions.InternalError(_('Trying to encrypt a password while the personal key is undefined!'))
            if (category, name) == C.PROFILE_PASS_PATH:
                # using 'value' as the encryption key to encrypt another encryption key... could be confusing!
                d_list.append(self.host.memory.encryptPersonalData(data_key=C.MEMORY_CRYPTO_KEY,
                                                                    data_value=personal_key,
                                                                    crypto_key=value,
                                                                    profile=profile))
                d = PasswordHasher.hash(value)  # profile password is hashed (empty value stays empty)
            elif value:  # other non empty passwords are encrypted with the personal key
                d = BlockCipher.encrypt(personal_key, value)

        def gotFinalValue(value):
            if self.host.isConnected(profile):  # key can not exists if profile is not connected
                self.params[profile][(category, name)] = value
            self.host.bridge.paramUpdate(name, value, category, profile)
            self.host.trigger.point("paramUpdateTrigger", name, value, category, node[0], profile)
            return self.storage.setIndParam(category, name, value, profile)

        d.addCallback(gotFinalValue)
        d_list.append(d)
        return defer.DeferredList(d_list).addCallback(lambda dummy: None)

    def _getNodesOfTypes(self, attr_type, node_type="@ALL@"):
        """Return all the nodes matching the given types.

        TODO: using during the dev but not anymore... remove if not needed

        @param attr_type (str): the attribute type (string, text, password, bool, button, list)
        @param node_type (str): keyword for filtering:
                                    @ALL@ search everywhere
                                    @GENERAL@ only search in general type
                                    @INDIVIDUAL@ only search in individual type
        @return: dict{tuple: node}: a dict {key, value} where:
            - key is a couple (attribute category, attribute name)
            - value is a node
        """
        ret = {}
        for type_node in self.dom.documentElement.childNodes:
            if (((node_type == "@ALL@" or node_type == "@GENERAL@") and type_node.nodeName == C.GENERAL) or
                ((node_type == "@ALL@" or node_type == "@INDIVIDUAL@") and type_node.nodeName == C.INDIVIDUAL)):
                for cat_node in type_node.getElementsByTagName('category'):
                    cat = cat_node.getAttribute('name')
                    params = cat_node.getElementsByTagName("param")
                    for param in params:
                        if param.getAttribute("type") == attr_type:
                            ret[(cat, param.getAttribute("name"))] = param
        return ret

    def checkSecurityLimit(self, node, security_limit):
        """Check the given node against the given security limit.
        The value NO_SECURITY_LIMIT (-1) means that everything is allowed.
        @return: True if this node can be accessed with the given security limit.
        """
        if security_limit < 0:
            return True
        if node.hasAttribute("security"):
            if int(node.getAttribute("security")) <= security_limit:
                return True
        return False

    def checkApp(self, node, app):
        """Check the given node against the given app.
        @param node: parameter node
        @param app: name of the frontend requesting the parameters, or '' to get all parameters
        @return: True if this node concerns the given app.
        """
        if not app or not node.hasAttribute("app"):
            return True
        return node.getAttribute("app") == app
