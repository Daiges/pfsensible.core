# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Frederic Bor <frederic.bor@wanadoo.fr>
# Copyright: (c) 2026, Jonathan Daigle <Jonathan.Daigle@kaisev.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.pfsensible.core.plugins.module_utils.module_base import PFSenseModuleBase

DYNDNS_ARGUMENT_SPEC = dict(
    state=dict(default='present', choices=['present', 'absent']),
    enable=dict(default=True, type='bool'),
    # TODO: This list is way too long
    type=dict(required=True, choices=['all-inkl', 'azure', 'azurev6', 'citynetwork', 'cloudflare', 'cloudflare-v6', 'cloudns', 'custom', 'custom-v6', 'desec', 'desec-v6', 'digitalocean', 'digitalocean-v6', 'dnsexit', 'dnsimple', 'dnsimple-v6', 'dnsmadeeasy', 'dnsomatic', 'domeneshop', 'domeneshop-v6', 'dreamhost', 'dreamhost-v6', 'duiadns', 'duiadns-v6', 'dyfi', 'dyndns', 'dyndns-custom', 'dyndns-static', 'dyns', 'dynv6', 'dynv6-v6', 'easydns', 'easydns-v6', 'eurodns', 'freedns', 'freedns-v6', 'freedns2', 'freedns2-v6', 'glesys', 'gandi-livedns', 'gandi-livedns-v6', 'godaddy', 'godaddy-v6', 'googledomains', 'gratisdns', 'he-net', 'he-net-v6', 'he-net-tunnelbroker', 'hover', 'linode', 'linode-v6', 'loopia', 'luadns', 'luadns-v6', 'mythicbeasts', 'mythicbeasts-v6', 'name.com', 'name.com-v6', 'namecheap', 'nicru', 'nicru-v6', 'noip', 'noip-v6', 'noip-free', 'noip-free-v6', 'onecom', 'onecom-v6', 'ods', 'opendns', 'ovh-dynhost', 'route53', 'route53-v6', 'selfhost', 'spdyn', 'spdyn-v6', 'strato', 'yandex', 'yandex-v6', 'zoneedit', 'porkbun', 'porkbun-v6']),
    interface=dict(required=True, type='str'),
    check_ip_mode=dict(required=False, choices=['default', 'always', 'never']),
    host=dict(required=True, type='str'),
    domainname=dict(required=True, type='str'),
    proxied=dict(default=False,type='bool'),
    mx=dict(required=False, type='str'),
    wildcard=dict(required=False, type='bool'),
    verboselog=dict(required=False, type='bool'),
    username=dict(required=False, type='str'),
    password=dict(required=False, type='str'),
    descr=dict(required=True, type='str'),
    requestif=dict(required=True, type='str'),
    zoneid=dict(required=False, type='str'),
    ttl=dict(required=False, type='int'),
    maxcacheage=dict(required=False, type='int'),
    updateurl=dict(required=False, type='str'),
    resultmatch=dict(required=False, type='str'),
    id=dict(required=False, type='int'),
)

class PFSenseDyndnsModule(PFSenseModuleBase):
    """ module managing pfsense dyndns (ddns) entries """

    @staticmethod
    def get_argument_spec():
        """ return argument spec """
        return DYNDNS_ARGUMENT_SPEC

    ##############################
    # init
    #
    def __init__(self, module, pfsense=None):
        super(PFSenseDyndnsModule, self).__init__(module, pfsense)
        self.name = "pfsense_dyndns"
        self.root_elt = self.pfsense.get_element('dyndnses')
        self.obj = dict()

        if self.root_elt is None:
            self.root_elt = self.pfsense.new_element('dyndnses')
            self.pfsense.root.append(self.root_elt)

    ##############################
    # params processing
    #
    # TODO: Do I even need this function
    def _expand_alias(self, networks):
        """ return real addresses of alias """
        ret = list()

        while len(networks) > 0:
            alias = networks.pop()
            if self.pfsense.is_ipv4_network(alias, strict=False):
                ret.append(alias)
            else:
                alias_elt = self.pfsense.find_alias(alias, aliastype='host')
                if alias_elt is None:
                    alias_elt = self.pfsense.find_alias(alias, aliastype='network')
                networks += alias_elt.find('address').text.split(' ')

        return ret

    def _params_to_obj(self):
        """ return a dict from module params """
        params = self.params

        obj = dict()
        self.obj = obj

        obj['descr'] = params['descr']
        target_elt = self._find_target()
        if params['state'] == 'present':
            self._get_ansible_param(obj, 'state')
            self._get_ansible_param_bool(obj, 'enable')
            self._get_ansible_param(obj, 'type')
            self._get_ansible_param(obj, 'interface')
            self._get_ansible_param(obj, 'check_ip_mode')
            self._get_ansible_param(obj, 'host')
            self._get_ansible_param(obj, 'domainname')
            self._get_ansible_param(obj, 'mx')
            self._get_ansible_param_bool(obj, 'wildcard')
            self._get_ansible_param_bool(obj, 'verboselog')
            self._get_ansible_param(obj, 'username')
            self._get_ansible_param(obj, 'password')
            self._get_ansible_param(obj, 'descr')
            self._get_ansible_param(obj, 'requestif')
            self._get_ansible_param(obj, 'zoneid')
            self._get_ansible_param(obj, 'ttl')
            self._get_ansible_param(obj, 'maxcacheage')
            self._get_ansible_param(obj, 'updateurl')
            self._get_ansible_param(obj, 'resultmatch')
            self._get_ansible_param(obj, 'id')

        return obj

    # TODO: All of this
    def _validate_params(self):
        """ do some extra checks on input parameters """

    ##############################
    # XML processing
    #
    def _create_target(self):
        """ create the XML target_elt """
        return self.pfsense.new_element('dyndns')

    def _find_target(self):
        """ find the XML target_elt """
        for dyndns_elt in self.root_elt:
            # TODO: Null handling for the host property
            # TODO: How should we be identifying these? By description? By ID? I don't want the user to have to enter in either parameter unless necessary
            # I think this may be the best option for now
            if dyndns_elt.find('domainname').text == self.obj['domainname'] & dyndns_elt.find('host').text == self.obj['host']:
                return dyndns_elt
        return None

    @staticmethod
    def _get_params_to_remove():
        """ returns the list of params to remove if they are not set """
        return ['check_ip_mode', 'wildcard', 'verboselog', 'zoneid']

    ##############################
    # run
    #
    def _update(self):
        """ make the target pfsense reload """
        return self.pfsense.phpshell('''
send_event("service reload dyndnsall");
''')

    ##############################
    # Logging
    #
    def _get_obj_name(self):
        """ return obj's name """
        return "'{0}'".format(self.obj['descr'])

    # TODO: This whole thing
    def _log_fields(self, before=None):
        """ generate pseudo-CLI command fields parameters to create an obj """
        values = ''
        if before is None:
            values += self.format_cli_field(self.obj, 'host')
            values += self.format_cli_field(self.obj, 'domainname')
            values += self.format_cli_field(self.params, 'enable', fvalue=self.fvalue_bool, default=True)
        else:
            values += self.format_updated_cli_field(self.obj, before, 'host', add_comma=(values))
            values += self.format_updated_cli_field(self.obj, before, 'domainname', add_comma=(values))
            values += self.format_updated_cli_field(self.obj, before, 'enable', fvalue=self.fvalue_bool, default=True, add_comma=(values))

        return values
