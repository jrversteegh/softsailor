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
from xml.dom.minidom import parseString, Node 
from xml.parsers.expat import ExpatError
from zlib import decompress

import os

class BadToken(Exception):
    pass

def read_sol_document(handle, cache_file=None):
    data = handle.read()
    if data.find('Bad token') >= 0:
        raise BadToken('Bad token while fetching boat from sailonline')
    if cache_file:
        with open(cache_file, 'w') as f:
            f.write(data)
    if data.startswith('x'):
        data = decompress(data)
    dom = parseString(data)
    return dom

def fetch_sol_document_from_url(url, cached=False):
    cache_file = None
    if cached:
        sol_dir = os.path.expanduser('~') + '/.softsailor/sol'
        if not os.path.exists(sol_dir):
            os.makedirs(sol_dir)
        cache_file = sol_dir + '/' + url.replace('/', '_')
        if os.path.exists(cache_file):
            url = cache_file
            cache_file = None
    handle = urlopen(url)
    try:
        return read_sol_document(handle, cache_file)
    except BadToken as bt:
        raise BadToken(str(bt) + '. Url: %s' % url)

def fetch_sol_document(host, uri):
    conn = HTTPConnection(host, timeout=4)
    conn.request("GET", uri)
    conn.sock.settimeout(4)
    resp = conn.getresponse()
    try:
        return read_sol_document(resp)
    except BadToken as bt:
        raise BadToken(str(bt) + '. Host: %s, Uri: %s' % (host, uri))

def get_element(parent, name):
    children = parent.getElementsByTagName(name)
    try:
        return children[0]
    except IndexError:
        return None

def get_first_element(parent):
    for child in parent.childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            return child

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
