#!/usr/bin/env python

import pstats

p = pstats.Stats('prof.txt')

p.strip_dirs()
p.sort_stats(-1)
p.sort_stats('cumulative')
p.print_stats()
