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
from xml.parsers.expat import ExpatError
from zlib import decompress

class BadToken(Exception):
    pass

def read_sol_document(handle):
    data = handle.read()
    if data.find('Bad token') >= 0:
        raise BadToken('Bad token while fetching boat from sailonline')
    if data.startswith('x'):
        data = decompress(data)
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
    try:
        return children[0]
    except IndexError:
        return None

def get_elements(parent, name):
    children = parent.getElementsByTagName(name)
    return children

def get_child_text_value(parent, name):
    elem = get_element(parent, name)
    if elem is not None:
        child = elem.childNodes[0]
        if child is not None:
            return child.nodeValue
    return ''

def get_child_float_value(parent, name):
    return float(get_child_text_value(parent, name))
