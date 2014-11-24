#!/usr/bin/env python3

import urllib
import urllib.request
import hashlib
import glob
import string
import random
import itertools


host = 'vvor.virtualregatta.com'
service = '/core/Service/ServiceCaller.php?service='
user = '333458'
key = 'EC335D9E-9B78-4AE6-B21B-261DBA9EE288'

def id_generator(size=20, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def request(serv, req, xtra=''):
    qry = ''
    chk = serv
    for k, v in req:
        qry += '&%s=%s' % (k, v)
        chk += '%s' % v
    chk += xtra
    chk = hashlib.sha1(chk.encode('latin-1')).hexdigest()
    print(chk)
    url = 'http://%s%s%s%s&checksum=%s' % (host, service, serv, qry, chk)
    print(url)
    return urllib.request.urlopen(url).read()


class VR(object):
    pass

velems = ['dz7',   # PlayerManager
          'ez4d',  # _-Zx 
          '4',     # GetUserWrapper 
          '4s',    # WindManager(2) 
          'fifç',  # initAfterLoad
          '50',    # ZoomSelector.init
          '50',    # ZoomSelector.init (called twice)
         ]

if __name__ == '__main__':
    login = ('AuthLoginXml', 
             (
              ('id_user', user), 
              ('pass', key), 
             ),
             'vr2010',
            )
    data = request(*login)
    print(data)
    getuser = ('GetUser',
            (
             ('id_user', user),
             ('lang', 'EN'),
             ('light', '1'),
             ('auto', '1'),
             ('clientVersion', '5.2.26'),
            ),
           )
    data = request(*getuser, xtra=key)
    print(data)
    rnd = id_generator()
    update = ('Update',
              (
               ('id_user', user),
               ('cap', '115'),
               ('voile', '64'),
               ('r', rnd),
              ),
             )
    x = ''.join(velems)
    x = x.encode('latin-1')
    x = hashlib.sha1(x).hexdigest()
    x = key + x
    data = request(*update, xtra=x)
    print(data)
