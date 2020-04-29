#! /usr/bin/python3

# -*- coding:UTF-8 -*-
import sys
import numpy as np

def read_input(file):
    for line in file:
         yield line.strip()

def matrixcount():
    input = read_input(sys.stdin)
    xy = np.array([0.0 for i in 10])
    xx = np.diag(np.zeros(10))
    for line in input:
        field = line.split(",")
        xy += np.array(field,float)[:10]*float(field[10])
        for flag in range(10):
            xx[flag] += np.array(field[:10],float)*float(field[flag])
    return xy,xx
xy,xx = matrixcount()
length = len(xx)
data= list(xx.reshape(1,length**2)[0])+list(xy)
print("\t".join(str(i) for i in data))
