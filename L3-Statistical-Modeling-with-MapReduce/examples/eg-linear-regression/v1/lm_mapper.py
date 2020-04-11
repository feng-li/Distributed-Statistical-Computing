#!/usr/bin/anaconda2/bin/python
# -*- coding: utf-8 -*-
"""
linear regression mapper


"""

import sys
import numpy as np

def read_input(file): 
    for line in file:
        yield line.strip()
        #rstrip()去除字符串右边的空格 
input = read_input(sys.stdin)#依次读取每行的数据 

#an example
#datairow = '1,2,3,4,5,6'
#b =  ['1,2,3,4,5,6', '2,3,4,5,6,7']
#map(lm_row,b)

def lm_row(datairow):
    datairow = ["1"]+datairow.split(",") #add beta0
    datairow = np.array(datairow,float)
    y = datairow[len(datairow)-1]
    x =  datairow[:(len(datairow)-1)]
    xy = x*y
    xx = np.matrix(x).T*np.matrix(x)
    return xy,xx

res = map(lm_row,input) #contain xx xy

p = 0
for r in res:
    xy_tmp,xx_tmp = r
    if p==0:
        p = len(xy_tmp)
        xx = np.diag(np.zeros(p))
        xy = np.zeros(p)
    xx += xx_tmp
    xy += xy_tmp
  
xy = list(xy)
xx = xx.reshape(1,p**2)
xx = list(xx[0])
data = xy + xx
#print len(data)
print("\t".join(str(i) for i in data))

