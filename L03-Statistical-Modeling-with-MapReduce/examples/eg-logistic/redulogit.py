# -*- coding: utf-8 -*-
"""
Created on Wed Jan 06 15:05:41 2016

@author: ZHU
"""
import sys
import pandas as pd
#读取数据
f = sys.stdin
fields = f.read()
#整理数据
fields = fields.split(',')#每一块数据的结果是按“，”分割的，重新用“，”划分成列表
data = [field.split('\n') for field in fields]#每一块中自变量的系数
for i in range(len(data)):
    while '' in data[i]:#去除列表中的空格
        data[i].remove('')
data = pd.DataFrame(data)#重新整理成数据框
data.columns=['PriceCH','PriceMM','DiscCH','DiscMM','SpecialCH','SpecialMM','Lo\
yalCH','Intercept']
data = data.astype(float)#将数据框中的元素类型转化为float
print data
print data.mean()

