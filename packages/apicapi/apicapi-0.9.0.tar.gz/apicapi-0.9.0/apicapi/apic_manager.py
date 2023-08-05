# Copyright (c) 2014 Cisco Systems Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# @author: Arvind Somya (asomya@cisco.com), Cisco Systems Inc.
# @author: Ivar Lazzaro (ivar-lazzaro), Cisco Systems Inc.

from apicapi import apic_mapper
from apicapi import apic_client
from apicapi import exceptions as cexc
import uuid

CONTEXT_ENFORCED = '1'
CONTEXT_UNENFORCED = '2'
CONTEXT_SHARED = 'shared'
DN_KEY = 'dn'
PORT_DN_PATH = 'topology/pod-1/paths-%s/pathep-[eth%s/%s]'
NODE_DN_PATH = 'topology/pod-1/node-%s'
POD_POLICY_GROUP_DN_PATH = 'uni/fabric/funcprof/podpgrp-%s'
CP_PATH_DN = 'uni/tn-%s/brc-%s'
SCOPE_GLOBAL = 'global'
SCOPE_TENANT = 'tenant'
TENANT_COMMON = 'common'
NAMING_STRATEGY_UUID = 'use_uuid'
NAMING_STRATEGY_NAMES = 'use_name'

# L3 External constants
EXT_NODE = 'os-lnode'
EXT_INTERFACE = 'os-linterface'
EXT_EPG = 'os-external_epg'

# Contract constants
CP_SUBJ = 'os-subject'
CP_FILTER = 'os-filter'
CP_ENTRY = 'os-entry'
CP_INTERFACE = 'os-interface'

LOG = None


class APICManager(object):
    """Class to manage APIC translations and workflow.

    This class manages translation from Neutron objects to APIC
    managed objects and contains workflows to implement these
    translations.
    """
    def __init__(self, db, log, network_config, apic_config,
                 keyclient=None, keystone_authtoken=None,
                 apic_system_id='openstack'):
        self.db = db
        self.apic_config = apic_config
        self.vlan_ranges = network_config.get('vlan_ranges')
        self.switch_dict = network_config.get('switch_dict', {})
        self.vpc_dict = network_config.get('vpc_dict', {})
        self.ext_net_dict = network_config.get('external_network_dict', {})
        self.apic_system_id = apic_system_id
        global LOG
        LOG = log.getLogger(__name__)

        # Connect to the APIC
        self.apic = apic_client.RestClient(
            log,
            self.apic_system_id,
            self.apic_config.apic_hosts,
            self.apic_config.apic_username,
            self.apic_config.apic_password,
            self.apic_config.apic_use_ssl
        )

        name_mapping = self.apic_config.apic_name_mapping
        self._apic_mapper = apic_mapper.APICNameMapper(
            self.db, log, keyclient, keystone_authtoken,
            name_mapping)
        self.phys_domain_dn = None
        self.entity_profile_dn = None
        self.apic_system_id = apic_system_id
        self.app_profile_name = self.apic_mapper.app_profile(
            None, self.apic_config.apic_app_profile_name)

        self.function_profile = self.apic_config.apic_function_profile
        self.lacp_profile = self.apic_config.apic_lacp_profile

    @property
    def apic_mapper(self):
        return self._apic_mapper

    def ensure_infra_created_on_apic(self):
        """Ensure the infrastructure is setup.

        First create all common entities, and then
        Loop over the switch dictionary from the config and
        setup profiles for switches, modules and ports
        """
        # Create VLAN namespace
        vlan_ns_name = self.apic_config.apic_vlan_ns_name
        vlan_range = self.vlan_ranges[0]
        (vlan_min, vlan_max) = vlan_range.split(':')[-2:]
        vlan_ns_dn = self.ensure_vlan_ns_created_on_apic(
            vlan_ns_name, vlan_min, vlan_max)

        # Create domain
        phys_name = self.apic_config.apic_domain_name
        self.ensure_phys_domain_created_on_apic(phys_name, vlan_ns_dn)

        # Create entity profile
        ent_name = self.apic_config.apic_entity_profile
        self.ensure_entity_profile_created_on_apic(ent_name)

        # Create lacp profile
        lacp_name = self.lacp_profile
        self.ensure_lacp_profile_created_on_apic(lacp_name)

        # Create function profile
        func_name = self.function_profile
        self.ensure_function_profile_created_on_apic(func_name)

        # first make sure that all existing switches in DB are in apic
        for switch in self.db.get_switches():
            self.ensure_infra_created_for_switch(switch[0])

        # now create add any new switches in config to apic and DB
        for switch in self.switch_dict:
            for module_port in self.switch_dict[switch]:
                module, port = module_port.split('/')
                hosts = self.switch_dict[switch][module_port]
                for host in hosts:
                    self.add_hostlink(host, 'static', None, switch, module,
                                      port)

    def ensure_context_enforced(self, owner=TENANT_COMMON,
                                ctx_id=CONTEXT_SHARED, transaction=None):
        """Set the specified tenant's context to enforced."""
        with self.apic.transaction(transaction) as trs:
            self.apic.fvCtx.create(
                owner, ctx_id, pcEnfPref=CONTEXT_ENFORCED, transaction=trs)

    def ensure_context_deleted(self, owner=TENANT_COMMON,
                               ctx_id=CONTEXT_SHARED,
                               transaction=None):
        self.apic.fvCtx.delete(owner, ctx_id, transaction=transaction)

    def ensure_entity_profile_created_on_apic(self, name, transaction=None):
        """Create the infrastructure entity profile."""
        with self.apic.transaction(transaction) as trs:
            self.apic.infraAttEntityP.create(name, transaction=trs)
            # Attach phys domain to entity profile
            self.apic.infraRsDomP.create(name, self.phys_domain_dn,
                                         transaction=trs)
        self.entity_profile_dn = self.apic.infraAttEntityP.dn(name)

    def ensure_function_profile_created_on_apic(self, name, transaction=None):
        """Create the infrastructure function profile."""
        with self.apic.transaction(transaction) as trs:
            self.apic.infraAccPortGrp.create(name, transaction=trs)
            # Attach entity profile to function profile
            self.apic.infraRsAttEntP.create(name,
                                            tDn=self.entity_profile_dn,
                                            transaction=trs)

    def ensure_lacp_profile_created_on_apic(self, name, transaction=None):
        """Create the lacp profile."""
        with self.apic.transaction(transaction) as trs:
            self.apic.lacpLagPol.create(name, mode='active', transaction=trs)

    def ensure_infra_created_for_switch(self, switch, transaction=None):
        # Create a node and profile for this switch
        with self.apic.transaction(transaction) as trs:
            self.ensure_node_profile_created_for_switch(switch,
                                                        transaction=trs)
            ppname = self.ensure_port_profile_created_for_switch(
                switch, transaction=trs)

            # Setup each module and port range
            for module in self.db.get_modules_for_switch(switch):
                # Add this module and ports to the profile
                module = module[0]
                ports = [p[0] for p in
                         self.db.get_ports_for_switch_module(switch, module)]
                ports.sort()
                for port in ports:
                    pbname = '%s-%s' % (port, port)
                    hname = 'hports-%s-%s' % (module, pbname)
                    self.apic.infraHPortS.create(ppname, hname, 'range',
                                                 transaction=trs)
                    fpdn = self.get_function_profile(switch, module, port,
                                                     transaction=trs)
                    self.apic.infraRsAccBaseGrp.create(ppname, hname, 'range',
                                                       tDn=fpdn,
                                                       transaction=trs)
                    self.apic.infraPortBlk.create(ppname, hname, 'range',
                                                  pbname, fromCard=module,
                                                  toCard=module,
                                                  fromPort=str(port),
                                                  toPort=str(port),
                                                  transaction=trs)

    def get_function_profile(self, switch, module, port, transaction=None):
        fpdn = self.apic.infraAccPortGrp.dn(self.function_profile)
        with self.apic.transaction(transaction) as trs:
            if switch in self.vpc_dict:
                link1 = switch, module, port
                link2 = None

                host = self.db.get_hostlinks_for_switchport(
                    switch, module, port)[0][0]
                links = self.db.get_switch_and_port_for_host(host)
                for link in links:
                    switch2, module2, port2 = link
                    if switch2 == self.vpc_dict[switch]:
                        link2 = switch2, module2, port2
                        break
                if link2 is not None:
                    fpdn = self.ensure_vpc_profile_created(link1, link2,
                                                           transaction=trs)
        return fpdn

    def ensure_vpc_profile_created(self, link1, link2, transaction=None):
        sw1, mod1, port1 = link1
        sw2, mod2, port2 = link2
        bname = 'bundle-%s-%s-%s-and-%s-%s-%s' % (
            sw1, mod1, port1, sw2, mod1, port2)

        bundle = self.apic.infraAccBndlGrp.get(bname)
        if bundle:
            dn = self.apic.infraAccBndlGrp.dn(bname)
        else:
            with self.apic.transaction(transaction) as trs:
                self.apic.infraAccBndlGrp.create(bname, lagT='node',
                                                 transaction=trs)
                dn = self.apic.infraAccBndlGrp.dn(bname)
                ep = self.entity_profile_dn
                self.apic.infraRsAttEntP.create(bname, tDn=ep,
                                                transaction=trs)
                lp = self.lacp_profile
                self.apic.infraRsLacpPol.create(bname,
                                                tnLacpLagPolName=lp,
                                                transaction=trs)
        return dn

    def ensure_node_profile_created_for_switch(self, switch_id,
                                               transaction=None):
        """Creates a switch node profile.

        Create a node profile for a switch and add a switch
        to the leaf node selector
        """
        # Create Node profile
        with self.apic.transaction(transaction) as trs:
            self.apic.infraNodeP.create(switch_id, transaction=trs)
            # Create leaf selector
            lswitch_id = 'leaf'
            self.apic.infraLeafS.create(switch_id, lswitch_id, 'range',
                                        transaction=trs)
            # Add leaf nodes to the selector
            name = 'node'
            self.apic.infraNodeBlk.create(switch_id, lswitch_id, 'range',
                                          name, from_=switch_id,
                                          to_=switch_id, transaction=trs)

    def ensure_port_profile_created_for_switch(self, switch, transaction=None):
        """Check and create infra port profiles for a node."""

        # Generate id port profile
        ppname = 'pprofile-%s' % switch

        # Create port profile for this switch
        with self.apic.transaction(transaction) as trs:
            self.apic.infraAccPortP.create(ppname, transaction=trs)
            # Add port profile to node profile
            ppdn = self.apic.infraAccPortP.dn(ppname)
            self.apic.infraRsAccPortP.create(switch, ppdn, transaction=trs)
        return ppname

    def ensure_phys_domain_created_on_apic(self, phys_name, vlan_ns_dn=None,
                                           vxlan_ns_dn=None, transaction=None):
        """Create physical domain.

        Creates the physical domain on the APIC and adds a VLAN or VXLAN
        namespace to that physical domain.
        """
        with self.apic.transaction(transaction) as trs:
            self.apic.physDomP.create(phys_name, transaction=trs)
            if vlan_ns_dn:
                self.apic.infraRsVlanNs.create(phys_name,
                                               tDn=vlan_ns_dn, transaction=trs)
        self.phys_domain_dn = self.apic.physDomP.dn(phys_name)

    def ensure_vlan_ns_created_on_apic(self, name, vlan_min, vlan_max,
                                       transaction=None):
        """Creates a static VLAN namespace with the given vlan range."""
        with self.apic.transaction(transaction) as trs:
            ns_args = name, 'static'
            self.apic.fvnsVlanInstP.create(*ns_args, transaction=trs)
            vlan_min = 'vlan-' + vlan_min
            vlan_max = 'vlan-' + vlan_max
            ns_blk_args = name, 'static', vlan_min, vlan_max
            ns_kw_args = {
                'name': 'encap',
                'from': vlan_min,
                'to': vlan_max
            }
            self.apic.fvnsEncapBlk__vlan.create(*ns_blk_args,
                                                transaction=trs,
                                                **ns_kw_args)
        return self.apic.fvnsVlanInstP.dn(*ns_args)

    def ensure_bgp_pod_policy_created_on_apic(self, bgp_pol_name='default',
                                              asn='1', pp_group_name='default',
                                              p_selector_name='default',
                                              transaction=None):
        """Set the route reflector for the fabric if missing."""
        with self.apic.transaction(transaction) as trs:
            self.apic.bgpInstPol.create(bgp_pol_name, transaction=trs)
            if not self.apic.bgpRRP.get_subtree(bgp_pol_name):
                for node in self.apic.fabricNode.list_all(role='spine'):
                    self.apic.bgpRRNodePEp.create(bgp_pol_name, node['id'],
                                                  transaction=trs)

            self.apic.bgpAsP.create(bgp_pol_name, asn=asn, transaction=trs)

            self.apic.fabricPodPGrp.create(pp_group_name, transaction=trs)
            reference = self.apic.fabricRsPodPGrpBGPRRP.get(pp_group_name)
            if not reference or not reference['tnBgpInstPolName']:
                self.apic.fabricRsPodPGrpBGPRRP.update(
                    pp_group_name,
                    tnBgpInstPolName=self.apic.bgpInstPol.name(bgp_pol_name),
                    transaction=trs)

            self.apic.fabricPodS__ALL.create(p_selector_name, type='ALL',
                                             transaction=trs)
            self.apic.fabricRsPodPGrp.create(
                p_selector_name, tDn=POD_POLICY_GROUP_DN_PATH % pp_group_name,
                transaction=trs)

    def ensure_bd_created_on_apic(self, tenant_id, bd_id,
                                  ctx_owner=TENANT_COMMON,
                                  ctx_name=CONTEXT_SHARED,
                                  transaction=None):
        """Creates a Bridge Domain on the APIC."""
        self.ensure_context_enforced(ctx_owner, ctx_name)
        with self.apic.transaction(transaction) as trs:
            self.apic.fvBD.create(tenant_id, bd_id, transaction=trs)
            # Add default context to the BD
            self.apic.fvRsCtx.create(
                tenant_id, bd_id,
                tnFvCtxName=self.apic.fvCtx.name(ctx_name),
                transaction=trs)

    def delete_bd_on_apic(self, tenant_id, bd_id, transaction=None):
        """Deletes a Bridge Domain from the APIC."""
        with self.apic.transaction(transaction) as trs:
            self.apic.fvBD.delete(tenant_id, bd_id, transaction=trs)

    def ensure_subnet_created_on_apic(self, tenant_id, bd_id, gw_ip,
                                      transaction=None):
        """Creates a subnet on the APIC

        The gateway ip (gw_ip) should be specified as a CIDR
        e.g. 10.0.0.1/24
        """
        with self.apic.transaction(transaction) as trs:
            self.apic.fvSubnet.create(tenant_id, bd_id, gw_ip, transaction=trs)

    def ensure_subnet_deleted_on_apic(self, tenant_id, bd_id, gw_ip,
                                      transaction=None):
        with self.apic.transaction(transaction) as trs:
            self.apic.fvSubnet.delete(tenant_id, bd_id, gw_ip, transaction=trs)

    def ensure_epg_created(self, tenant_id, network_id,
                           bd_name=None, transaction=None):
        """Creates an End Point Group on the APIC.

        Create a new EPG on the APIC for the network spcified. This information
        is also tracked in the local DB and associate the bridge domain for the
        network with the EPG created.
        """
        # Check if an EPG is already present for this network
        # Create a new EPG on the APIC
        epg_uid = network_id
        with self.apic.transaction(transaction) as trs:
            self.apic.fvAEPg.create(tenant_id, self.app_profile_name, epg_uid,
                                    transaction=trs)

            # Add bd to EPG
            bd_name = bd_name or network_id
            self.apic.fvBD.create(tenant_id, bd_name, transaction=trs)

            # create fvRsBd
            self.apic.fvRsBd.create(tenant_id, self.app_profile_name, epg_uid,
                                    tnFvBDName=self.apic.fvBD.name(bd_name),
                                    transaction=trs)

            # Add EPG to physical domain
            self.apic.fvRsDomAtt.create(
                tenant_id, self.app_profile_name, epg_uid, self.phys_domain_dn,
                transaction=trs)
        return epg_uid

    def delete_epg_for_network(self, tenant_id, network_id, transaction=None):
        """Deletes the EPG from the APIC and removes it from the DB."""
        # Delete this epg
        with self.apic.transaction(transaction) as trs:
            self.apic.fvAEPg.delete(tenant_id, self.app_profile_name,
                                    network_id, transaction=trs)

    def create_tenant_filter(self, tenant_id, fuuid, transaction=None):
        """Creates a tenant filter and a generic entry under it."""
        with self.apic.transaction(transaction) as trs:
            # Create a new tenant filter
            self.apic.vzFilter.create(tenant_id, fuuid, transaction=trs)
            # Create a new entry
            self.apic.vzEntry.create(tenant_id, fuuid,
                                     CP_ENTRY, transaction=trs)

    def set_contract_for_epg(self, tenant_id, epg_id,
                             contract_id, provider=False, transaction=None):
        """Set the contract for an EPG.

        By default EPGs are consumers of a contract.
        Set provider flag to True for the EPG to act as a provider.
        """
        with self.apic.transaction(transaction) as trs:
            if provider:
                self.apic.fvRsProv.create(
                    tenant_id, self.app_profile_name, epg_id, contract_id,
                    transaction=trs)
            else:
                self.apic.fvRsCons.create(
                    tenant_id, self.app_profile_name, epg_id, contract_id,
                    transaction=trs)

    def delete_contract_for_epg(self, tenant_id, epg_id,
                                contract_id, provider=False, transaction=None):
        """Delete the contract for an End Point Group.

        Check if the EPG was a provider and attempt to grab another contract
        consumer from the DB and set that as the new contract provider.
        """
        with self.apic.transaction(transaction) as trs:
            if provider:
                self.apic.fvRsProv.delete(
                    tenant_id, self.app_profile_name, epg_id, contract_id,
                    transaction=trs)
            else:
                self.apic.fvRsCons.delete(
                    tenant_id, self.app_profile_name, epg_id, contract_id,
                    transaction=trs)

    def get_router_contract(self, router_id, owner=TENANT_COMMON,
                            suuid=CP_SUBJ, iuuid=CP_INTERFACE,
                            fuuid=CP_FILTER, transaction=None):
        """Creates a tenant contract for router.

        Create a tenant contract if one doesn't exist. Also create a
        subject, filter and entry and set the filters to allow all
        protocol traffic on all ports
        """
        cuuid = 'contract-%s' % router_id.uid
        with self.apic.transaction(transaction) as trs:
            # Create contract
            scope = SCOPE_GLOBAL if owner == TENANT_COMMON else SCOPE_TENANT
            self.apic.vzBrCP.create(owner, cuuid, scope=scope)
            # Create subject
            self.apic.vzSubj.create(owner, cuuid, suuid, transaction=trs)
            # Create filter and entry
            self.create_tenant_filter(owner, fuuid, transaction=trs)
            # Create contract interface
            self.apic.vzCPIf.create(owner, iuuid, transaction=trs)
            self.apic.vzRsIf.create(owner, iuuid,
                                    tDn=CP_PATH_DN % (owner, cuuid),
                                    transaction=trs)
        self.db.update_contract_for_router(owner, router_id.uid)
        return cuuid

    def delete_router_contract(self, router_id, transaction=None):
        """Delete the contract related to a given Router."""
        contract = self.db.get_contract_for_router(router_id.uid)
        if contract:
            with self.apic.transaction(transaction) as trs:
                self.apic.vzBrCP.delete(contract.tenant_id,
                                        'contract-%s' % router_id.uid,
                                        transaction=trs)
            self.db.delete_contract_for_router(router_id.uid)

    def ensure_path_created_for_port(self, tenant_id, network_id,
                                     host_id, encap, transaction=None):
        """Create path attribute for an End Point Group."""
        with self.apic.transaction(transaction) as trs:
            eid = self.ensure_epg_created(tenant_id, network_id,
                                          transaction=trs)

            # Get attached switch and port for this host
            host_config = self.db.get_switch_and_port_for_host(host_id)
            if not host_config or not host_config.count():
                raise cexc.ApicHostNotConfigured(host=host_id)

            for switch, module, port in host_config:
                self.ensure_path_binding_for_port(
                    tenant_id, eid, encap, switch, module, port,
                    transaction=trs)

    def ensure_path_binding_for_port(self, tenant_id, epg_id, encap,
                                     switch, module, port, transaction=None):
        # Verify that it exists, or create it if required
        with self.apic.transaction(transaction) as trs:
            encap = 'vlan-' + str(encap)
            pdn = PORT_DN_PATH % (switch, module, port)
            self.apic.fvRsPathAtt.create(
                tenant_id, self.app_profile_name, epg_id, pdn,
                encap=encap, mode="regular",
                instrImedcy="immediate", transaction=trs)

    def ensure_path_deleted_for_port(self, tenant_id, network_id, host_id,
                                     transaction=None):
        with self.apic.transaction(transaction) as trs:
            host_config = self.db.get_switch_and_port_for_host(host_id)
            if not host_config or not host_config.count():
                LOG.warn("The switch and port for host '%s' "
                         "are not configured" % host_id)
                return
            for switch, module, port in host_config:
                pdn = PORT_DN_PATH % (switch, module, port)
                self.apic.fvRsPathAtt.delete(tenant_id, self.app_profile_name,
                                             network_id, pdn, transaction=trs)

    def ensure_static_endpoint_created(self, tenant_id, epg_id, host_id,
                                       mac_address, ip_address, encap,
                                       transaction=None):
        with self.apic.transaction(transaction) as trs:
            # Get attached switch and port for this host
            host_config = self.db.get_switch_and_port_for_host(host_id)
            if not host_config or not host_config.count():
                raise cexc.ApicHostNotConfigured(host=host_id)

            encap = 'vlan-' + str(encap)
            self.apic.fvStCEp.create(
                tenant_id, self.app_profile_name, epg_id,
                mac_address, 'tep', encap=encap, ip=ip_address,
                transaction=trs)
            for switch, module, port in host_config:
                pdn = PORT_DN_PATH % (switch, module, port)
                self.apic.fvRsStCEpToPathEp.create(
                    tenant_id, self.app_profile_name, epg_id,
                    mac_address, 'tep', pdn, transaction=trs)

    def ensure_static_endpoint_deleted(self, tenant_id, epg_id, mac_address,
                                       transaction=None):
        self.apic.fvStCEp.delete(
            tenant_id, self.app_profile_name, epg_id,
            mac_address, 'tep', transaction=transaction)

    def add_hostlink(self, host, ifname, ifmac, switch, module, port,
                     transaction=None):
        switch2 = None
        update = False

        with self.apic.transaction(transaction) as trs:
            hostlinks = []
            for hlink in self.db.get_switch_and_port_for_host(host):
                hostlinks.append(hlink)
            if switch in self.vpc_dict:
                # with VPC, we support exactly one link for switch/host
                update = True
                switch2 = self.vpc_dict[switch]
                for link in hostlinks:
                    switch1, module1, port1 = link
                    if switch1 == switch:
                        update = False
                        break
            else:
                # no VPC, we support exactly one link from this host
                if not hostlinks:
                    update = True
                elif hostlinks[0] != (switch, module, port):
                    try:
                        self.db.delete_hostlink(
                            host,
                            self.db.get_hostlinks_for_host(host)[0]['ifname'])
                    except Exception as e:
                        LOG.exception(e)
                    update = True
            if update:
                self.db.add_hostlink(host, ifname, ifmac,
                                     switch, module, port)
                self.ensure_infra_created_for_switch(switch,
                                                     transaction=trs)
                if switch2 is not None:
                    self.ensure_infra_created_for_switch(switch2,
                                                         transaction=trs)
                self.ensure_vlans_created_for_host(host, transaction=trs)

    def ensure_vlans_created_for_host(self, host, transaction=None):
        with self.apic.transaction(transaction) as trs:
            segments = self.db.get_tenant_network_vlan_for_host(host)
            for tenant, network, encap in segments:
                tenant_id = self.db.get_apic_name(
                    tenant, apic_mapper.NAME_TYPE_TENANT)[0]
                network_id = self.db.get_apic_name(
                    network, apic_mapper.NAME_TYPE_NETWORK)[0]
                self.ensure_path_created_for_port(
                    tenant_id, network_id, host, encap, transaction=trs)

    def remove_hostlink(self, host, ifname, ifmac, switch, module, port):
        self.db.delete_hostlink(host, ifname)
        # TODO(mandeep): delete the right elements

    def create_router(self, router_id, owner=TENANT_COMMON,
                      context=CONTEXT_SHARED, transaction=None):

        with self.apic.transaction(transaction) as trs:
            self.get_router_contract(router_id, owner=owner,
                                     transaction=trs)
            self.ensure_context_enforced(owner, context, transaction=trs)

    def enable_router(self, router_id, owner=TENANT_COMMON, suuid=CP_SUBJ,
                      fuuid=CP_FILTER, transaction=None):
        cuuid = 'contract-%s' % router_id.uid
        self.apic.vzRsSubjFiltAtt.create(owner, cuuid, suuid, fuuid,
                                         transaction=transaction)

    def disable_router(self, router_id, owner=TENANT_COMMON, suuid=CP_SUBJ,
                       fuuid=CP_FILTER, transaction=None):
        cuuid = 'contract-%s' % router_id.uid
        self.apic.vzRsSubjFiltAtt.delete(owner, cuuid, suuid, fuuid,
                                         transaction=transaction)

    def add_router_interface(self, tenant_id, router_id,
                             network_id, context=CONTEXT_SHARED,
                             transaction=None):
        # Get contract and epg
        with self.apic.transaction(transaction) as trs:
            cid = 'contract-%s' % router_id.uid
            eid = self.ensure_epg_created(tenant_id, network_id,
                                          transaction=trs)

            # Ensure that the router ctx exists

            # update corresponding BD's ctx to this router ctx
            bd_id = network_id
            self.apic.fvRsCtx.create(
                tenant_id, bd_id, tnFvCtxName=self.apic.fvCtx.name(context),
                transaction=trs)
            # set the EPG to provide this contract
            self.set_contract_for_epg(tenant_id, eid, cid, True,
                                      transaction=trs)

            # set the EPG to consume this contract
            self.set_contract_for_epg(tenant_id, eid, cid, transaction=trs)

    def remove_router_interface(self, tenant_id, router_id,
                                network_id, context=CONTEXT_SHARED,
                                transaction=None):
        # Get contract and epg
        with self.apic.transaction(transaction) as trs:
            cid = 'contract-%s' % router_id.uid
            eid = self.ensure_epg_created(tenant_id, network_id,
                                          transaction=trs)

            # Delete contract for this epg
            self.delete_contract_for_epg(tenant_id, eid, cid, True,
                                         transaction=trs)
            self.delete_contract_for_epg(tenant_id, eid, cid, False,
                                         transaction=trs)

            # set the BDs' ctx to default
            bd_id = network_id
            self.apic.fvRsCtx.create(
                tenant_id, bd_id, tnFvCtxName=self.apic.fvCtx.name(context),
                transaction=trs)

    def delete_router(self, router_id, transaction=None):
        with self.apic.transaction(transaction) as trs:
            self.delete_router_contract(router_id, transaction=trs)

    def delete_external_routed_network(self, network_id, owner=TENANT_COMMON,
                                       transaction=None):
        with self.apic.transaction(transaction) as trs:
            self.apic.l3extOut.delete(owner, network_id, transaction=trs)

    def ensure_external_routed_network_created(self, network_id,
                                               owner=TENANT_COMMON,
                                               context=CONTEXT_SHARED,
                                               transaction=None):
        """Creates a L3 External context on the APIC."""
        with self.apic.transaction(transaction) as trs:
            # Link external context to the internal router ctx
            self.apic.l3extRsEctx.create(
                owner, network_id, tnFvCtxName=self.apic.fvCtx.name(context),
                transaction=trs)

    def ensure_logical_node_profile_created(self, network_id,
                                            switch, module, port, encap,
                                            address, owner=TENANT_COMMON,
                                            transaction=None):
        """Creates Logical Node Profile for External Network in APIC."""
        with self.apic.transaction(transaction) as trs:
            # TODO(ivar): default value for router id
            self.apic.l3extRsNodeL3OutAtt.create(
                owner, network_id, EXT_NODE,
                NODE_DN_PATH % switch, rtrId='1.0.0.1', transaction=trs)
            self.apic.l3extRsPathL3OutAtt.create(
                owner, network_id, EXT_NODE,
                EXT_INTERFACE, PORT_DN_PATH % (switch, module, port),
                encap=encap or 'unknown', addr=address,
                ifInstT='l3-port' if not encap else 'sub-interface',
                transaction=trs)

    def ensure_static_route_created(self, network_id, switch,
                                    next_hop, subnet='0.0.0.0/0',
                                    owner=TENANT_COMMON, transaction=None):
        """Add static route to existing External Routed Network."""
        with self.apic.transaction(transaction) as trs:
            self.apic.ipNexthopP.create(
                owner, network_id, EXT_NODE, NODE_DN_PATH % switch, subnet,
                next_hop, transaction=trs)

    def ensure_external_epg_created(self, router_id, subnet='0.0.0.0/0',
                                    owner=TENANT_COMMON, transaction=None):
        """Add EPG to existing External Routed Network."""
        with self.apic.transaction(transaction) as trs:
            self.apic.l3extSubnet.create(owner, router_id, EXT_EPG, subnet,
                                         transaction=trs)

    def ensure_external_epg_consumed_contract(self, network_id, contract_id,
                                              owner=TENANT_COMMON,
                                              transaction=None):
        with self.apic.transaction(transaction) as trs:
            self.apic.fvRsCons__Ext.create(owner, network_id, EXT_EPG,
                                           contract_id, transaction=trs)

    def ensure_external_epg_provided_contract(self, network_id, contract_id,
                                              owner=TENANT_COMMON,
                                              transaction=None):
        with self.apic.transaction(transaction) as trs:
            self.apic.fvRsProv__Ext.create(owner, network_id, EXT_EPG,
                                           contract_id, transaction=trs)

    def delete_external_epg_contract(self, router_id, network_id,
                                     transaction=None):
        contract = self.db.get_contract_for_router(router_id.uid)
        with self.apic.transaction(transaction) as trs:
            if contract:
                self.apic.fvRsCons__Ext.delete(contract.tenant_id, network_id,
                                               EXT_EPG,
                                               'contract-%s' % router_id.uid,
                                               transaction=trs)
                self.apic.fvRsProv__Ext.delete(contract.tenant_id, network_id,
                                               EXT_EPG,
                                               'contract-%s' % router_id.uid,
                                               transaction=trs)

    def ensure_external_routed_network_deleted(self, network_id,
                                               owner=TENANT_COMMON,
                                               transaction=None):
        with self.apic.transaction(transaction) as trs:
            self.apic.l3extOut.delete(owner, network_id, transaction=trs)
