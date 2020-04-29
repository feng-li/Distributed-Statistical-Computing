#! /usr/bin/python3

import sys
import numpy as np

def read_input(file):
    for line in file:
         yield line.strip()
          
input = read_input(sys.stdin)
length=0
for line in input:
    field = line.split("\t")
    if length == 0:
        length = len(field)
        data = np.array([0.0 for i in range(length)])
    data += np.array(field,dtype = float)
                                        
xy = np.mat(data[:10])
xy = xy.T
xx= data[10:]
xx = xx.reshape(10,10)
xx = np.mat(xx)
xx = xx.I
result = xx*xy
print(result)

