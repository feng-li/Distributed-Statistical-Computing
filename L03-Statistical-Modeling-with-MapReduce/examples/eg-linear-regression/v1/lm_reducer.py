#!/usr/bin/anaconda2/bin/python
# -*- coding: utf-8 -*-
"""
linear regression reducer


"""

import sys 
import numpy as np

def read_input(file):
    for line in file:
        yield line.strip()
input = read_input(sys.stdin) 

def forsumup(datairow):
    datairow = datairow.split("\t")
    datairow = np.array(datairow,float)
    return datairow

vecsumup = np.array(map(forsumup,input))
sumup = np.sum(vecsumup,axis = 0)

p = int((-1+np.sqrt(1+4.0*len(sumup)))/2.0)
XY = np.mat(sumup[:p]).T
XX = np.mat(sumup[p:].reshape(p,p)).I #ni
beta = XX*XY
print beta
