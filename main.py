#!/usr/bin/env python

# ACI main/test script
#
# Steven Coutts - stevec@couttsnet.com - 4 November 2018
#
# 13-July-2019 - Minor updates, add subnet to the BD, changed names of stuff
#                Add a subnet to the BD

import acifunctions as aci
from acitoolkit.acitoolkit import *

tenantName = 'Softcat'
appName = 'sfctAppNginx'
epgName = 'sfctEpgWeb'
bridgeDomainName = 'sfctBdWeb'
vrfName = 'sfctVrfWeb'
subnetName = "sfctSubnet10.100.100.0-24"
subnetIP = "10.100.100.1/24"

session = aci.login('admin', 'ciscopsdt', 'https://sandboxapicdc.cisco.com')
# Create the Tenant
tenant = aci.createTenant(tenantName)
# Create the Application Profile
app = aci.createAppProfile(appName, tenant)
# Create the EPG
epg = aci.createEPG(epgName, app)
# Create a VRF and BridgeDomain
vrf = aci.createVRF(vrfName, tenant)
bd = aci.createBD(bridgeDomainName, tenant)
# Add the vrf to the bridgedomain
bd.add_context(vrf)
# Add a subnet to the bridge domain
subnet = aci.createSubnet(subnetName, subnetIP, bd)
bd.add_subnet(subnet)
# Place the EPG in the BD
epg.add_bd(bd)

resp = tenant.push_to_apic(session)
if not resp.ok:
  print('%% Error: Could not push configuration to APIC')
  print(resp.text)

# Print what was sent
print 'Pushed the following JSON to the APIC'
print 'URL:', tenant.get_url()
print 'JSON:', tenant.get_json()


