#!/usr/bin/env python

# ACI main/test script
#
# Steven Coutts - stevec@couttsnet.com - 4 November 2018

import acifunctions as aci
from acitoolkit.acitoolkit import *

session = aci.login('admin', 'ciscopsdt', 'https://sandboxapicdc.cisco.com')

# Create the Tenant
tenant = Tenant('forfusion-test')
# Create the Application Profile
app = AppProfile('for-app', tenant)
# Create the EPG
epg = EPG('for-epg', app)
# Create a Context and BridgeDomain
context = Context('for-default-vrf', tenant)
bd = BridgeDomain('for-default-bd', tenant)
bd.add_context(context)
# Place the EPG in the BD
epg.add_bd(bd)

resp = tenant.push_to_apic(session)
if resp.ok:
    print 'Success'

# Print what was sent
print 'Pushed the following JSON to the APIC'
print 'URL:', tenant.get_url()
print 'JSON:', tenant.get_json()


