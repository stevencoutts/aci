# ACI general functions to import
#
# Steven Coutts - stevec@couttsnet.com - 4 November 2018

from acitoolkit.acitoolkit import *

def login (username, password, url):
    # Login to APIC and push the config
    session = Session(url, username, password)
    session.login()
    return session

