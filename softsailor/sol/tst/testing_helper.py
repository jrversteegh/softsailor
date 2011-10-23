#!/usr/bin/env python

import os
import sys

module_path = os.path.dirname(os.path.realpath(__file__)) + '/..'
sys.path.append(module_path)
module_path = os.path.dirname(os.path.realpath(__file__)) + '/../..'
sys.path.append(module_path)
module_path = os.path.dirname(os.path.realpath(__file__)) + '/../../..'
sys.path.append(module_path)

offline = os.system('ping -c 1 -w 1 google.com >/dev/null 2>&1')
