#! /usr/bin/env python
from itertools import combinations
import sys
import numpy as np
import pandas as pd

A=[]
B=[]

for line in sys.stdin:
    fields = line.strip().split(',')
    a = float(fields[0])
    b = float(fields[1])
    A.append(a)
    B.append(b)
    for i in range(1,len(A)):
	A[i] = (A[i] - min(A))/(max(A)-min(A))
    for j in range(1,len(B)):
	B[j] = (B[j] -min(B))/(max(B)-min(B))

A = np.array(A)
B = np.array(B)
data = np.column_stack((A , B))
print(data)
sys.stdin.close()
