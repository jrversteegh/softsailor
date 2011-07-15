"""
Sol xml util module

Contains xml interfacing with sol server
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2011, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

from httplib import HTTPConnection
from urllib import urlopen
from xml.dom.minidom import parseString, getDOMImplementation

class BadToken(Exception):
    pass

def read_sol_document(handle):
    data = handle.read()
    if data.find('Bad token') >= 0:
        raise BadToken('Bad token while fetching boat from sailonline')
    dom = parseString(data)
    return dom

def fetch_sol_document_from_url(url):
    handle = urlopen(url)
    return read_sol_document(handle)

def fetch_sol_document(host, file):
    conn = HTTPConnection(host, timeout=4)
    conn.request("GET", file)
    conn.sock.settimeout(4)
    resp = conn.getresponse()
    return read_sol_document(resp)

def get_element(parent, name):
    children = parent.getElementsByTagName(name)
    return children[0]

def get_elements(parent, name):
    children = parent.getElementsByTagName(name)
    return children

def get_child_text_value(parent, name):
    return get_element(parent, name).childNodes[0].nodeValue

def get_child_float_value(parent, name):
    return float(get_child_text_value(parent, name))
