# -*- coding: utf-8 -*-
"""
Created on Tue Jan 05 18:50:39 2016

@author: ZHU
"""

#! usr/bin/env python
import sys
import pandas as pd
from statsmodels.api import *
import numpy as np
Purchase = []
WeekofPurchase = []
StoreID = []
PriceCH = []
PriceMM = []
DiscCH = []
DiscMM = []
SpecialCH = []
SpecialMM = []
LoyalCH = []
Store7 = []
PctDiscMM =[]
PctDiscMM = []
Store = []

#打开文件
f = sys.stdin
#f=open('orangejuice.csv','r')
#读取数据
for line in f.readlines():
    vrb = line.split(',')
    Purchase.append(vrb[1])
    WeekofPurchase.append(float(vrb[2]))
    StoreID.append(float(vrb[3]))
    PriceCH.append(float(vrb[4]))
    PriceMM.append(float(vrb[5]))
    DiscCH.append(float(vrb[6]))
    DiscMM.append(float(vrb[7]))
    SpecialCH.append(float(vrb[8]))
    SpecialMM.append(float(vrb[9]))
    LoyalCH.append(float(vrb[10]))
    Store7.append(vrb[14])
    PctDiscMM.append(float(vrb[15]))
    PctDiscMM.append(float(vrb[16]))
    Store.append(float(vrb[18]))

f.close

#因变量选择PUrchase中的MM，如果是MM则取1否则为0
MM = pd.get_dummies(Purchase)#将分类型变量转化为0，1
MM = MM[MM.columns[1]]#选择MM为真的一列

#选取自变量
xdata = pd.DataFrame([PriceCH,PriceMM,DiscCH,DiscMM,SpecialCH,SpecialMM,LoyalCH])
xdata=xdata.T                      
xdata.columns=['PriceCH','PriceMM','DiscCH','DiscMM','SpecialCH','SpecialMM','LoyalCH']
xdata['intercept']=1.0

#打乱顺序
shuffle = np.random.permutation(1069)
MM = MM[shuffle]
xdata = xdata.ix[shuffle]

l = len(MM)
n=3#划分不同的几块，这里令n=3
step = l/n

#对前n-1块进行计算
for i in range(n-1):
    #print ("利用第{}行到{}行的数据进行建模。".format(step*i,step*(i+1)))
    logitmodel = Logit(MM[step*i:step*(i+1)],xdata[step*i:step*(i+1)])
    res = logitmodel.fit(disp=0)
    #print res.summary()
    for j in range(len(res.params)):
        print res.params [j]
    print ','

#对最后一块进行计算
#print ("利用第{}行到{}行的数据进行建模。".format(step*(n-1),l))
logitmodel = Logit(MM[step*(n-1):l],xdata[step*(n-1):l])
res = logitmodel.fit(disp=0)
#print res.summary()
for j in range(len(res.params)):
        print res.params [j]
