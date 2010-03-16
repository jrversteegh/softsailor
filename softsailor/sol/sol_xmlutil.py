
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
    conn = HTTPConnection(host)
    conn.request("GET", file)
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
