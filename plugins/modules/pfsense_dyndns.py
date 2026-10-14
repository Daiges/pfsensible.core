#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Orion Poplawski <orion@nwra.com>
# Copyright: (c) 2018, Frederic Bor <frederic.bor@wanadoo.fr>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: pfsense_dyndns
version_added: TODO
author: Jonathan Daigle
short_description: Manage pfSense dyndns entries
description:
  - Manage pfSense dyndns (ddns) entries
notes:
options:
  state:
    description: State in which to leave the entry
    choices: [ "present", "absent" ]
    default: present
    type: str
  enable:
    description: Enable dynamic dns for this entry
    default: true
    type: bool
  type:
    description: The type of upstream dyndns service/provider to integrate with
    choices: ["all-inkl", "azure", "azurev6", "citynetwork", "cloudflare", "cloudflare-v6", "cloudns", "custom", "custom-v6", "desec", "desec-v6", "digitalocean", "digitalocean-v6", "dnsexit", "dnsimple", "dnsimple-v6", "dnsmadeeasy", "dnsomatic", "domeneshop", "domeneshop-v6", "dreamhost", "dreamhost-v6", "duiadns", "duiadns-v6", "dyfi", "dyndns", "dyndns-custom", "dyndns-static", "dyns", "dynv6", "dynv6-v6", "easydns", "easydns-v6", "eurodns", "freedns", "freedns-v6", "freedns2", "freedns2-v6", "glesys", "gandi-livedns", "gandi-livedns-v6", "godaddy", "godaddy-v6", "googledomains", "gratisdns", "he-net", "he-net-v6", "he-net-tunnelbroker", "hover", "linode", "linode-v6", "loopia", "luadns", "luadns-v6", "mythicbeasts", "mythicbeasts-v6", "name.com", "name.com-v6", "namecheap", "nicru", "nicru-v6", "noip", "noip-v6", "noip-free", "noip-free-v6", "onecom", "onecom-v6", "ods", "opendns", "ovh-dynhost", "route53", "route53-v6", "selfhost", "spdyn", "spdyn-v6", "strato", "yandex", "yandex-v6", "zoneedit", "porkbun", "porkbun-v6"]
    required: true
    type: str
  interface:
    description: TODO
    default: wan
    type: str
  check_ip_mode:
    description: TODO
    choices: [ "default", "always", "never" ]
    default: present
    type: str
  host:
    description: The host part of the address to update (TODO: TONS of caveats)
    required: true
    type: str
  domainname:
    description: The domain name part of the address to update (TODO: TONS of caveats)
    required: true
    type: str
  proxied:
    description: Enable Cloudflare VirtualDNS proxy. Only applies when the type is cloudflare or cloudflare-v6
    default: false
    type: bool
  mx:
    description: MX (mail) records to create for the host
    type: str
  wildcard:
    description: TODO
    default: false
    type: bool
  verboselog:
    description: Enable verbose logging for this entry
    default: false
    type: bool
  username:
    description: The username for authentication to upstream provider. TODO: TONS of caveats
    type: str
  password:
    description: The password for authentication to upstream provider. TODO: TONS of caveats
    type: str
  descr:
    description: The description of the dyndns entry
    required: true
    type: str
  requestif:
    description: TODO
    default: wan
    type: str
  zoneid:
    description: TODO
    type: str
  ttl:
    description: The TTL specified for the DNS record
    type: int
  maxcacheage:
    description: TODO
    type: it
  updateurl:
    description: TODO
    type: str
  resultmatch:
    description: TODO
    type: str
"""

EXAMPLES = """
- name: Add dynddns entry
  pfsense_dyndns:
    descr: "foo.example.com DDNS"
    type: cloudflare
    host: foo
    domainname: example.com
    password: "{{ cloudflare_api_token }}"


- name: Remove dyndns entry
  pfsense_dyndns:
    state: absent
    descr: "foo.example.com DDNS"
    type: cloudflare
    host: foo
    domainname: example.com
    password: "{{ cloudflare_api_token }}"
"""
# TODO: These examples represent what currently happens, but that is not the desired output
RETURN = """
commands:
    description: the set of commands that would be pushed to the remote device (if pfSense had a CLI)
    returned: always
    type: list
    sample: ["create dyndns 'Test Entry', host='foo', domainname='example.com'", "delete dyndns 'Test Entry'"]
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.pfsensible.core.plugins.module_utils.dyndns import PFSenseDyndnsModule, DYNDNS_ARGUMENT_SPEC 


def main():
    module = AnsibleModule(
        argument_spec=DYNDNS_ARGUMENT_SPEC,
        supports_check_mode=True)

    pfmodule = PFSenseDyndnsModule(module)
    pfmodule.run(module.params)
    pfmodule.commit_changes()


if __name__ == '__main__':
    main()
