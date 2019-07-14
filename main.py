#!/usr/bin/env python

# ACI main/test script
#
# Steven Coutts - stevec@couttsnet.com - 4 November 2018
#
# 13-July-2019 - Minor updates, add subnet to the BD, changed names of stuff
#                Add a subnet to the BD
#
#
#
import acifunctions as aci
from acitoolkit.acitoolkit import *
#
# Create tenanat and the Web EPG
#
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
appSfctAppNginx = aci.createAppProfile(appName, tenant)
# Create the EPG
epgSfctEpgWeb = aci.createEPG(epgName, appSfctAppNginx)
# Create a VRF and BridgeDomain
vrf = aci.createVRF(vrfName, tenant)
bdSfctBdWeb = aci.createBD(bridgeDomainName, tenant)
# Add the vrf to the bridgedomain
bdSfctBdWeb.add_context(vrf)
# Add a subnet to the bridge domain
subnet = aci.createSubnet(subnetName, subnetIP, bdSfctBdWeb)
bdSfctBdWeb.add_subnet(subnet)
# Place the EPG in the BD
epgSfctEpgWeb.add_bd(bdSfctBdWeb)
#
# Create and the DB EPG
#
appName = 'sfctAppMysql'
epgName = 'sfctEpgDB'
vrfName = 'sfctVrfDB'
bridgeDomainName = 'sfctBdDB'
subnetName = "sfctSubnet10.100.200.0-24"
subnetIP = "10.100.200.1/24"
# Create the Application Profile
appSfctAppMysql = aci.createAppProfile(appName, tenant)
# Create the EPG
epgSfctEpgDB = aci.createEPG(epgName, appSfctAppMysql)
# Create a VRF and BridgeDomain
vrf = aci.createVRF(vrfName, tenant)
bdSfctBdDB = aci.createBD(bridgeDomainName, tenant)
# Add the vrf to the bridgedomain
bdSfctBdDB.add_context(vrf)
# Add a subnet to the bridge domain
subnet = aci.createSubnet(subnetName, subnetIP, bdSfctBdDB)
bdSfctBdDB.add_subnet(subnet)
# Place the EPG in the BD
epgSfctEpgDB.add_bd(bdSfctBdDB)
#
#
#
epgName = 'sfctEpgWebDev'
subnetName = "sfctSubnet10.100.101.0-24"
subnetIP = "10.100.101.1/24"
# Create the EPG
epgSfctEpgWebDev = aci.createEPG(epgName, appSfctAppNginx)
# Add a subnet to the bridge domain
subnet = aci.createSubnet(subnetName, subnetIP, bdSfctBdWeb)
bdSfctBdWeb.add_subnet(subnet)
# Place the EPG in the BD
epgSfctEpgWebDev.add_bd(bdSfctBdWeb)
#
# Create a contract
#
contractName = "sfctCtrctDB"
contractSfctCtrctDB = aci.createContract(contractName, tenant)
# Create a Filter
icmp_entry = FilterEntry('icmpentry',
                         applyToFrag='no',
                         arpOpc='unspecified',
                         dFromPort='unspecified',
                         dToPort='unspecified',
                         etherT='ip',
                         prot='icmp',
                         sFromPort='unspecified',
                         sToPort='unspecified',
                         tcpRules='unspecified',
                         parent=contractSfctCtrctDB)
tcp_entry = FilterEntry('tcpentry',
                        applyToFrag='no',
                        arpOpc='unspecified',
                        dFromPort='3306',
                        dToPort='3306',
                        etherT='ip',
                        prot='tcp',
                        sFromPort='5000',
                        sToPort='5010',
                        tcpRules='unspecified',
                        parent=contractSfctCtrctDB)
#
# Provide/consume contrtact
#
epgSfctEpgDB.provide(contractSfctCtrctDB)
epgSfctEpgWeb.consume(contractSfctCtrctDB)
epgSfctEpgWebDev.consume(contractSfctCtrctDB)
#
# Push to the APIC
#
resp = tenant.push_to_apic(session)
if not resp.ok:
    print('%% Error: Could not push configuration to APIC')
    print(resp.text)
# Print what was sent
print 'Pushed the following JSON to the APIC'
print 'URL:', tenant.get_url()
print 'JSON:', tenant.get_json()


