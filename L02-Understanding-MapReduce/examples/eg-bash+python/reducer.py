#! /usr/bin/python

from __future__ import division
import os
import sys


f = open('t', 'r')
d = {}
for line in f:
    cs = line.strip()
    d[cs] = 0
f.close()


d1 = []
for line in sys.stdin:
    [cs, url, width, height] = line.strip().split('\t')
    if cs in d and cs not in d1:
        d1.append(cs)
        res = [cs, url]
        print '\t'.join(res)

