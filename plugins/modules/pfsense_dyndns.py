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
    description: The interface to monitor for IP address changes
    default: wan
    type: str
  check_ip_mode:
    description: Set to always to use a Check IP service to find the firewall's pubic IP address. When set to "Default" the service will only be used if the interface has a private address
    choices: [ "default", "always", "never" ]
    default: present
    type: str
  host:
    description: The host part of the address to update. See NetGate documentation or your firewall's dyndns config page for detailed usage.
    required: false
    type: str
  domainname:
    description: The domain name part of the address to update. See NetGate documentation or your firewall's dyndns config page for detailed usage.
    required: false
    type: str
  proxied:
    description: Enable Cloudflare VirtualDNS proxy. Only applies when the type is cloudflare or cloudflare-v6
    default: false
    type: bool
  mx:
    description: MX (mail) records to create for the host. Not supported by all providers.
    type: str
  wildcard:
    description: When enabled the created DNS entry will use a wildcard, meaning all host queries for that domain will be directed to the dynamic IP address.
    default: false
    type: bool
  verboselog:
    description: Enable verbose logging for this entry
    default: false
    type: bool
  username:
    description: The username for authentication to upstream provider. See NetGate documentation or your firewall's dyndns config page for detailed usage.
    type: str
  password:
    description: The password for authentication to upstream provider. See NetGate documentation or your firewall's dyndns config page for detailed usage.
    type: str
  descr:
    description: The description of the dyndns entry
    required: true
    type: str
  requestif:
    description: The interface to send the request to the provider from. This is usually the same as the interface
    default: wan
    type: str
  zoneid:
    description: The DNS Zone or Record ID to update. Only applies to Azure, DNSimple, and Route53. See NetGate documentation or your firewall's dyndns config page for detailed usage.
    type: str
  ttl:
    description: The TTL for the created DNS record
    type: int
  maxcacheage:
    description: The maximum number of days to wait before forcing an update to the DNS record, even if no IP address change is detected.
    type: it
  updateurl:
    description: For Type custom only. The provider URL to make POST requests to. Use %IP% to include the new IP address in the URL
    type: str
  resultmatch:
    description: |
      The pattern used to verify that the result from the provider is successful. If left blank the returned result will not be checked.
      Use %IP% as a placeholder for the new IP address
      This should only be used with Type custom
      This field should be identical to what the DDNS Provider will return if the update succeeds, leave it blank to disable checking of returned results.
      To include the new IP in the request, put %IP% in its place. Separate multiple possible values with a |. Use \\| if the provider includes a | in the result
      Tabs, newlines, and carriage returns are trimmed from the beginning and end of the result before the comparison is run.
    type: str
  curl_ipresolve_v4:
    description: Force IPv4 for DNS resolution
    type: bool
    default: false
  curl_ssl_verifypeer:
    description: Verify the SSL/TLS certificate of the remote service
    default: false
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
RETURN = """
commands:
    description: the set of commands that would be pushed to the remote device (if pfSense had a CLI)
    returned: always
    type: list
    sample: ["create dyndns 'Test Entry', host='foo', domainname='example.com'", "delete dyndns 'Test Entry', host='foo', domainname='example.com'"]
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
