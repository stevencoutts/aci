import requests
import json
import acifunctions.py

def get_cookies(apic):
    username = 'admin'
    password = 'ciscopsdt'
    url = apic + '/api/aaaLogin.json'
    auth = dict(aaaUser=dict(attributes=dict(name=username, pwd=password)))
    authenticate = requests.post(url, data=json.dumps(auth), verify=False)
    return authenticate.cookies

def add_tenant(tenant, apic,cookies):
    jsondata = {"fvTenant":{"attributes":{"dn":"uni/tn-Softcat","name":"Softcat","rn":"tn-Softcat","status":"created"},"children":[]}}
    result = requests.post('{0}://{1}/api/node/mo/uni/tn-Softcat.json'.format(protocol, host), cookies=cookies, data=json.dumps(jsondata), verify=False)
    print result.status_code
    print result.text

def add_vrf(apic,cookies):
    jsondata = {"fvCtx":{"attributes":{"dn":"uni/tn-Softcat/ctx-Internal","name":"Internal","rn":"ctx-Internal","status":"created"},"children":[]}}
    result = requests.post('{0}://{1}/api/node/mo/uni/tn-Softcat/ctx-Internal.json'.format(protocol, host), cookies=cookies, data=json.dumps(jsondata), verify=False)
    print result.status_code
    print result.text

def get_tenants(apic, cookies):
    uri = '/api/class/fvTenant.json'
    url = apic + uri
    req = requests.get(url, cookies=cookies, verify=False)
    response = req.text
    return response

if __name__ == "__main__":
    protocol = 'https'
    host = 'sandboxapicdc.cisco.com'
    apic = '{0}://{1}'.format(protocol, host)
    cookies = get_cookies(apic)
    add_tenant("Softcat",apic,cookies)
    add_vrf(apic,cookies)
    rsp = get_tenants(apic,cookies)
    rsp_dict = json.loads(rsp)
    tenants = rsp_dict['imdata']

for tenant in tenants:
      print tenant['fvTenant']['attributes']['name']