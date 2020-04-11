from __future__ import division
import os
import sys



last = None
d = {}
for line in sys.stdin:
    [query, img, rank, show, click] = line.strip().split('\t')
    now = query + '_' + img + '_' + rank
    if (last is not None) and (last != now):
        res = [last, d[last][0], d[last][1], d[last][1]/d[last][0]]
        print '\t'.join(str(x) for x in res)
        d = {}
        d[now] = [int(show), int(click)]
    elif (last == now):
        d[now][0] += int(show)
        d[now][1] += int(click)
    else:
        d[now] = [int(show), int(click)]
    last = now

if (last is not None):
    res = [last, d[last][0], d[last][1], d[last][1]/d[last][0]]
    print '\t'.join(str(x) for x in res)
