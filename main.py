#!/usr/bin/env python

# ACI main/test script
#
# Steven Coutts - stevec@couttsnet.com - 4 November 2018

import acifunctions as aci
from acitoolkit.acitoolkit import *

tenantName = 'forfusion-test'
appName = 'forfusion-app'
epgName = 'forfusion-epg'
bridgeDomainName = 'forfusion-bd'
vrfName = 'forfusion-vrf'

session = aci.login('admin', 'ciscopsdt', 'https://sandboxapicdc.cisco.com')
# Create the Tenant
tenant = aci.createTenant(tenantName)
# Create the Application Profile
app = aci.createAppProfile(appName, tenant)
# Create the EPG
epg = aci.createEPG(epgName, app)
# Create a Context and BridgeDomain
vrf = aci.createVRF(vrfName, tenant)
bd = aci.createBD(bridgeDomainName, tenant)



bd.add_context(vrf)
# Place the EPG in the BD
epg.add_bd(bd)

resp = tenant.push_to_apic(session)
if resp.ok:
    print 'Success'

# Print what was sent
print 'Pushed the following JSON to the APIC'
print 'URL:', tenant.get_url()
print 'JSON:', tenant.get_json()


