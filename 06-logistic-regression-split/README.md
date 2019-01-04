# 实例分析：基于MapReduce的Logistics回归


## 准备知识

* Logistics回归
* R和Python
* Hadoop Streaming

## 研究思路

Logit模型(Logistic model)，是最早的离散选择模型。Logit模型的求解速度快、应用方便，可以对预
测的结果进行比较和检验，在社会学、生物统计学、临床、数量心理学、计量经济学、市场营销等统计
实证分析中广为应用。本文以R软件中的Orange Juice数据为研究对象，通过描述性分析对消费者橙汁
品牌选择的偏好进行初步分析，继而分别建立了Logit回归模型，对消费数据进行拟合分析。最后在
MapReduce实践部分，展示了完整的从数据获取到Map函数、Reduce函数以及输出结果的过程。在服务器
上使用MapRuducer的方法， 对Logistics回归进行并行计算操作。Map函数的具体流程如下：


1. 首先将数据分成k个不同的块。

2. 对每一块的数据进行logistic回归估计出自变量的系数；Reduce函数则对每一块的自变量系数进行
平均，作为最终的结果。

可以证明，当数据量n和每一个子块中的数据量m足够大的情况下，用这种MapReduce方法计算出来的系
数估计与真实值具有一致性。


## 数据准备

本研究所用样本数据均来自R软件ISLR包中的OJ数据，样本中包含1070个消费者购买Citrus Hill 牌或
Minute Maid牌橙汁的行为数据。1070个样本数据的18个变量包含Purchase、Store7、StoreID和STORE4
个分类变量，和其余的14个数值变量，用于以下研究分析。

## 建立Logit回归模型

将购买（Purchase）作为本文的因变量，将购买CH”定义为0，“购买MM”定义为1，选取CH售价（PriceCH），MM售价（PriceMM），CH折扣（DiscCH），MM折扣（DiscMM），CH特殊指标（SpecialCH），MM特殊指标（SpecialMM），CH忠诚度（LoyalCH）几个指标作为自变量建立Logit回归模型。MapReduce中首先将数据打乱，随后分成不同的3块，以下分别给出3块回归的结果和最后Reduce后的结果，并和利用全部数据整体进行对比。


### Mapper部分


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


### Reducer部分


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


### 实践结论

观察Logit全模型的估计结果，可以发现CH标价（PriceCH）、MM标价（PriceMM）、MM折扣（DiscMM）、
CH品牌忠诚度（LoyalCH）、MM折扣比例（PctDiscMM）对Purchase有显著的影响。一定程度上对
Purchase有解释作用，而其他变量对因变量解释性并不显著。通过对比MapReduce的结果和利用全部数
据同时建模的结果可以发现，MapReduce的结果精确度还是比较高的，为了避免是一次实验造成的随机
性结果，又重复多次进行计算，发现大多数变量的系数依然较为只有“CH特殊指标（SpecialCH）“这一
个变量的系数有可能出现符号相反的结果，考虑到其系数本身就接近于0，同时并不显著，所以不能改
变我们对最终结果比较精确的判断。在对三个子块进行建模得到的系数进行比较后，发现不同子块之间
的个别变量的系数差别还是比较大的，例如“CH价格（PriceCH）”三次得到结果分别是6.28，1.44和
4.39，这可能与数据的分布有关系，但是不影响最终Reduce的效果。

（感谢中央财经大学朱述政提供素材和案例。）
