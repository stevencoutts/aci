# ACI general functions to import
#
# Steven Coutts - stevec@couttsnet.com - 4 November 2018

from acitoolkit.acitoolkit import *

def login (username, password, url):
    # Login to APIC and push the config
    session = Session(url, username, password)
    session.login()
    return session

def createTenant (tenantName):
    tenant = Tenant(tenantName)
    return tenant

def createAppProfile (AppName, tenant):
    app = AppProfile(AppName, tenant)
    return app

def createEPG (epgName, app):
    epg = EPG(epgName, app)
    return epg

def createVRF (vrfName, tenant):
    context = Context(vrfName, tenant)
    return context

def createBD (BDName, tenant):
    bd = BridgeDomain(BDName, tenant)
    return bd

def createSubnet (subnetName, subnetIP, bd):
    subnet = Subnet(subnetName, bd)
    subnet.set_addr(subnetIP)
    return subnet

def createContract (ContractName, tenant):
    contract = Contract(ContractName, tenant)
    return contract

def createFilter (FilterName, tenant, dFromPort, dToPort):
    filter = FilterEntry(FilterName, tenant, "false", "req", dFromPort, dToPort)
    return filter