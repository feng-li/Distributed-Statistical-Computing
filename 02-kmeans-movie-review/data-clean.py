#! /usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
from numpy import *
import pandas as pd
from pandas import *
import sys
from itertools import islice


df = open('kmeans.csv','r',encoding = 'utf-8')
lines = df.readlines()

rate = []
number = []

for line in lines:
part=line.split(',')
c1 =part[0]
rate.append(c1)
c2=part[1][1:-5]
number.append(c2)

rate = rate[1:]
number = number[1:]

for j in range(0,len(rate)):
rate[j] = float(rate[j])

for a in range(0,len(number)):
number[a] = int(number[a])

data = [rate] +[number]
data = transpose(np.array(data))
data = DataFrame(data, columns = ['rate', 'number'])

data.to_csv('clean.txt',index=False)
