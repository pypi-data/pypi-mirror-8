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


class JID(unicode):
    """This class help manage JID (Node@Domaine/Resource)"""

    def __new__(cls, jid):
        self = unicode.__new__(cls, cls.__normalize(jid))
        self.__parse()
        return self

    @classmethod
    def __normalize(cls, jid):
        """Naive normalization before instantiating and parsing the JID"""
        if not jid:
            return jid
        tokens = jid.split('/')
        tokens[0] = tokens[0].lower()  # force node and domain to lower-case
        return '/'.join(tokens)

    def __parse(self):
        """Find node domain and resource"""
        node_end = self.find('@')
        if node_end < 0:
            node_end = 0
        domain_end = self.find('/')
        if domain_end < 1:
            domain_end = len(self)
        self.node = self[:node_end]
        self.domain = self[(node_end + 1) if node_end else 0:domain_end]
        self.resource = self[domain_end + 1:]
        if not node_end:
            self.bare = self
        else:
            self.bare = self.node + '@' + self.domain

    def is_valid(self):
        """
        @return: True if the JID is XMPP compliant
        """
        # TODO: implement real check, according to the RFC http://tools.ietf.org/html/rfc6122
        return self.domain != ""
