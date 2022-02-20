from __future__ import division
import os
import sys



last = None
d = {}
for line in sys.stdin:
    [query, price] = line.strip().split('\t')
    now = query
    if (last is not None) and (last != now):
        res = [last, d['price']]
        print '\t'.join(str(i) for i in res)
        d = {}
        d['price'] = int(price)
    elif (last == now):
        d['price'] += int(price)
    else:
        d['price'] = int(price)
    last = now

if (last is not None):
    res = [last, d['price']]
    print '\t'.join(str(i) for i in res)
