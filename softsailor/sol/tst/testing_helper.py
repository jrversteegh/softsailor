#!/usr/bin/env python

import os
import sys
import logging

module_path = os.path.dirname(os.path.realpath(__file__)) + '/..'
sys.path.insert(0, module_path)
module_path = os.path.dirname(os.path.realpath(__file__)) + '/../..'
sys.path.insert(0, module_path)
module_path = os.path.dirname(os.path.realpath(__file__)) + '/../../..'
sys.path.insert(0, module_path)

offline = os.system('ping -c 1 -w 1 google.com >/dev/null 2>&1')

def setup_log(logname):
    try:
        os.remove(logname)
    except:
        pass
    logging.basicConfig(filename=logname + '.log', 
                        level=logging.DEBUG,
                        filemode='w', 
                        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
