#coding: gbk
"""
# @file   : mapper.py
# @author : Feng Li 
# @date   : 2016/07/15
# @brief  :
"""

# input  :
#       
# output :
#       


import ast
import sys
from gtburl import *


def img2cs2url(img):
    try:
        cs = ast.literal_eval(img)[0]["cs"]
        url = gen_url_from_csid(cs)
    except:
        url = '-'
    return url



def run():
    for line in sys.stdin:
        cols = line.split('\t')
        query = cols[3]
        cmatch = cols[9]
        if cmatch != '367':
            continue
        ovl_exp = cols[55].strip()
        if  '3106-1' in ovl_exp:
            cols = [query, img2cs2url(cols[53]), cols[12], 1, cols[1]]
            cols = [str(x) for x in cols]
            print '\t'.join(cols)
    return 0


if __name__ == '__main__':
    exit(run())
