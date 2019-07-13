#!/usr/bin/env python

# ACI main/test script
#
# Steven Coutts - stevec@couttsnet.com - 4 November 2018
#
# 13-July-2019 - Minor updates, add subnet to the BD, changed names of stuff

import acifunctions as aci
from acitoolkit.acitoolkit import *

tenantName = 'Softcat'
appName = 'sfct-nginx'
epgName = 'sfct-web'
bridgeDomainName = 'sfct-web-bd'
vrfName = 'sfct-web-vrf'

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


# Place the EPG in the BD
epg.add_bd(bd)

resp = tenant.push_to_apic(session)
if resp.ok:
    print 'Success'

# Print what was sent
print 'Pushed the following JSON to the APIC'
print 'URL:', tenant.get_url()
print 'JSON:', tenant.get_json()


