#coding: gbk
"""
# @file   : mapper.py
# @author : Feng Li
# @date   : 2016/07/15
# @brief  :
"""

import sys


queries = {}
f = open('queries92w', 'r')
for line in f:
    query = line.strip()
    queries[query] = 1


def run():
    for line in sys.stdin:
        cols = line.split('\t')
        if len(cols) < 51:
            continue
        cmatch = cols[9]
        if cmatch != '346':
            continue
        price = cols[2]
        query = cols[3]
        if query in queries:
            cols = [query,  price]
            cols = [str(x) for x in cols]
            print '\t'.join(cols)
    return 0


if __name__ == '__main__':
    exit(run())
