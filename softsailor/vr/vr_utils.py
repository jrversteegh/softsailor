"""
VR xml util module

Contains xml interfacing with VR server and generic xml utilities
"""
__author__ = "J.R. Versteegh"
__copyright__ = "Copyright 2015, J.R. Versteegh"
__contact__ = "j.r.versteegh@gmail.com"
__version__ = "0.1"
__license__ = "GPLv3, No Warranty. See 'LICENSE'"

from httplib import HTTPConnection
from urllib import urlopen
from xml.dom.minidom import parseString, Node 
from xml.parsers.expat import ExpatError
from zlib import decompress
from datetime import datetime, timedelta
from time import time
from logging import getLogger

_log = getLogger('softsailor.vr.vr_xmlutil')

import os

class BadKey(Exception):
    pass

class ConnectionFailed(Exception):
    pass

def read_vr_document(handle, cache_file=None):
    data = handle.read()
    if data.find('Bad token') >= 0:
        raise BadToken('Bad token while fetching boat from sailonline')
    if cache_file:
        _log.info('Writing to cache: %s' % cache_file)
        with open(cache_file, 'w') as f:
            f.write(data)
    if data.startswith('x'):
        data = decompress(data)
    dom = parseString(data)
    return dom

def fetch_vr_document_from_url(url, cached=False):
    cache_file = None
    if cached:
        vr_dir = os.path.expanduser('~') + '/.softsailor/vr'
        if not os.path.exists(vr_dir):
            os.makedirs(vr_dir)
        cache_file = vr_dir + '/' + url.replace('/', '_')
        if os.path.exists(cache_file):
            _log.info('Cache file exists: %s' % cache_file)
            fileage = time() - os.stat(cache_file).st_mtime
            if fileage > 86400 * 30:
                _log.info('Cache file out of date, age: %d days' % int(fileage / 86400))
            else:
                _log.info('Cache file age is: %d days' % int(fileage / 86400))
                url = cache_file
                cache_file = None
    _log.info('Reading file: %s' % url) 
    handle = urlopen(url)
    try:
        return read_vr_document(handle, cache_file)
    except BadKey as bt:
        raise BadKey(str(bt) + '. Url: %s' % url)

def fetch_vr_document(host, uri):
    _log.debug('Fetching %s from %s' % (uri, host))
    try:
        conn = HTTPConnection(host, timeout=4)
        conn.request("GET", uri)
        conn.sock.settimeout(4)
        resp = conn.getresponse()
    except Exception as e:
        raise ConnectionFailed('Connection %s/%s failed: %s' % (host, uri, str(e)))
    try:
        return read_vr_document(resp)
    except BadKey as bt:
        raise BadKey(str(bt) + '. Host: %s, Uri: %s' % (host, uri))

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
