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
    type=dict(required=True, choices=['all-inkl', 'azure', 'azurev6', 'citynetwork', 'cloudflare', 'cloudflare-v6', 'cloudns', 'custom', 'custom-v6', 'desec', 'desec-v6', 'digitalocean', 'digitalocean-v6', 'dnsexit', 'dnsimple', 'dnsimple-v6', 'dnsmadeeasy', 'dnsomatic', 'domeneshop', 'domeneshop-v6', 'dreamhost', 'dreamhost-v6', 'duiadns', 'duiadns-v6', 'dyfi', 'dyndns', 'dyndns-custom', 'dyndns-static', 'dyns', 'dynv6', 'dynv6-v6', 'easydns', 'easydns-v6', 'eurodns', 'freedns', 'freedns-v6', 'freedns2', 'freedns2-v6', 'glesys', 'gandi-livedns', 'gandi-livedns-v6', 'godaddy', 'godaddy-v6', 'googledomains', 'gratisdns', 'he-net', 'he-net-v6', 'he-net-tunnelbroker', 'hover', 'linode', 'linode-v6', 'loopia', 'luadns', 'luadns-v6', 'mythicbeasts', 'mythicbeasts-v6', 'name.com', 'name.com-v6', 'namecheap', 'nicru', 'nicru-v6', 'noip', 'noip-v6', 'noip-free', 'noip-free-v6', 'onecom', 'onecom-v6', 'ods', 'opendns', 'ovh-dynhost', 'route53', 'route53-v6', 'selfhost', 'spdyn', 'spdyn-v6', 'strato', 'yandex', 'yandex-v6', 'zoneedit', 'porkbun', 'porkbun-v6']),
    interface=dict(default='wan', type='str'),
    check_ip_mode=dict(required=False, choices=['default', 'always', 'never']),
    host=dict(required=False, type='str'),
    domainname=dict(required=False, type='str'),
    proxied=dict(default=False,type='bool'),
    mx=dict(required=False, type='str'),
    wildcard=dict(required=False, type='bool'),
    verboselog=dict(required=False, type='bool'),
    username=dict(required=False, type='str'),
    password=dict(required=False, no_log=True, type='str'),
    descr=dict(required=True, type='str'),
    requestif=dict(default='wan', type='str'),
    zoneid=dict(required=False, type='str'),
    ttl=dict(required=False, type='int'),
    maxcacheage=dict(required=False, type='int'),
    updateurl=dict(required=False, type='str'),
    resultmatch=dict(required=False, type='str'),
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

    def _params_to_obj(self):
        """ return a dict from module params """
        params = self.params

        obj = dict()
        self.obj = obj

        obj['descr'] = params['descr']
        self._get_ansible_param(obj, 'host')
        self._get_ansible_param(obj, 'domainname')
        self._get_ansible_param(obj, 'updateurl')
        if params['state'] == 'present':
            self._get_ansible_param(obj, 'state')
            self._get_ansible_param_bool(obj, 'enable')
            self._get_ansible_param(obj, 'type')
            self._get_ansible_param(obj, 'interface')
            self._get_ansible_param(obj, 'check_ip_mode')
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
            self._get_ansible_param(obj, 'resultmatch')

        return obj

    # TODO: Improve parameter validation
    def _validate_params(self):
        """ do some extra checks on input parameters """
        params = self.params
        if params['type'] == 'custom':
            if not params['updateurl']:
                self.module.fail_json(msg='updateurl is required for custom entries')
        else:
            if not params['domainname'] and not params['host']:
                self.module.fail_json(msg='domainname or host is required for non-custom entries')


    ##############################
    # XML processing
    #
    def _create_target(self):
        """ create the XML target_elt """
        id = 0
        for dyndns_elt in self.root_elt:
            entryid = int(dyndns_elt.find('id').text)
            if entryid >= id:
                id = entryid + 1

        self.obj['id'] = str(id)
        return self.pfsense.new_element('dyndns')

    def _find_target(self):
        """ find the XML target_elt """
        for dyndns_elt in self.root_elt:
            if getattr(dyndns_elt.find('domainname'), 'text', '') == self.obj.get('domainname', '') and getattr(dyndns_elt.find('host'), 'text', '') == self.obj.get('host', '') and getattr(dyndns_elt.find('updateurl'), 'text', '') == self.obj.get('updateurl', ''):
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

    def _log_fields(self, before=None):
        """ generate pseudo-CLI command fields parameters to create an obj """
        values = ''
        if before is None:
            values += self.format_cli_field(self.obj, 'host')
            values += self.format_cli_field(self.obj, 'domainname')
            values += self.format_cli_field(self.obj, 'updateurl')
            values += self.format_cli_field(self.params, 'enable', fvalue=self.fvalue_bool, default=True)
        else:
            values += self.format_updated_cli_field(self.obj, before, 'host', add_comma=(values))
            values += self.format_updated_cli_field(self.obj, before, 'domainname', add_comma=(values))
            values += self.format_updated_cli_field(self.obj, before, 'updateurl', add_comma=(values))
            values += self.format_updated_cli_field(self.obj, before, 'enable', fvalue=self.fvalue_bool, default=True, add_comma=(values))

        return values

    def _log_fields_delete(self):
        return self._log_fields()
