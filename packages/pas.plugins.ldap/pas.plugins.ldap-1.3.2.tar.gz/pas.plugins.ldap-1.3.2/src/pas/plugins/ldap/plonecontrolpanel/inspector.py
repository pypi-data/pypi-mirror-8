# -*- coding: utf-8 -*-
from Products.CMFCore.interfaces import ISiteRoot
from Products.Five import BrowserView
from node.ext.ldap import LDAPNode
from node.ext.ldap.interfaces import ILDAPGroupsConfig
from node.ext.ldap.interfaces import ILDAPProps
from node.ext.ldap.interfaces import ILDAPUsersConfig
from node.utils import encode
from zope.component import getUtility

import json


def safe_encode(val):
    if isinstance(val, unicode):
        return val.encode('utf-8')
    return val


class LDAPInspector(BrowserView):

    @property
    def plugin(self):
        portal = getUtility(ISiteRoot)
        aclu = portal.acl_users
        plugin = aclu.pasldap
        return plugin

    @property
    def props(self):
        return ILDAPProps(self.plugin)

    def users_children(self):
        users = ILDAPUsersConfig(self.plugin)
        return self.children(users.baseDN)

    def groups_children(self):
        groups = ILDAPGroupsConfig(self.plugin)
        return self.children(groups.baseDN)

    def node_attributes(self):
        rdn = self.request['rdn']
        base = self.request['base']
        if base == 'users':
            users = ILDAPUsersConfig(self.plugin)
            baseDN = users.baseDN
        else:
            groups = ILDAPGroupsConfig(self.plugin)
            baseDN = groups.baseDN
        root = LDAPNode(baseDN, self.props)
        node = root[rdn]
        ret = dict()
        for key, val in node.attrs.items():
            try:
                if not node.attrs.is_binary(key):
                    ret[safe_encode(key)] = safe_encode(val)
                else:
                    ret[safe_encode(key)] = \
                        '(Binary Data with {0} Bytes)'.format(len(val))
            except UnicodeDecodeError:
                ret[safe_encode(key)] = '! (UnicodeDecodeError)'
            except Exception:
                ret[safe_encode(key)] = '! (Unknown Exception)'
        return json.dumps(ret)

    def children(self, baseDN):
        node = LDAPNode(baseDN, self.props)
        ret = list()
        for key in node:
            ret.append({'rdn': key})
        return json.dumps(ret)
