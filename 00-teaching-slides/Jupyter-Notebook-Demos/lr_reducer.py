#! /usr/bin/python

import numpy as np
import sys
mul = []
for line in sys.stdin:
   s1 = line.lstrip('[').rstrip(']').split(']')
   n = len(s1)
   mat = []
   for i in range(0,n-2):
       s1[i] = s1[i].replace('[','')
       if i == 0:
          l = s1[i].split(',')
       else:
          l = s1[i].split(',')[1:]
       l = [float(x) for x in l]
       mat.append(l)
   mul.append(mat)
mul = np.array(mul)
summul = mul.sum(axis = 0)
sumlist = summul.tolist()
length = len(sumlist)
xx = sumlist[:length-1]
xy = sumlist[-1]
xx = np.mat(xx)
inv = xx.I
xy = np.mat(xy).T
beta = inv*xy
#print>>sys.stdout,"%r\n%r" % (xx,xy)
print >>sys.stdout,"%r" % beta.T
