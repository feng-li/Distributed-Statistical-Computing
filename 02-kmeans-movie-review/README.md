# 实例分析：2015年上映电影的聚类分析


## 准备知识

* K均值聚类算法
* R 和 Python
* Hadoop Streaming

## 数据准备

本次Hadoop实例是利用K均值聚类算法对豆瓣网上2015年上映的电影进行一次聚类分析，主要利用豆瓣
网上各个电影的评分和各个电影的评价人数这两个标准，对2015年所有上映的电影进行分类。数据的爬
取、清理使用Python语言，而K均值聚类模型建立的Map和Reduce，本实例同时采用了R和Python两种语言
进行编写。


* 爬取数据：通过firefox网站访问豆瓣网，找到关于2015年中国内地票房年度总排行，点击后利用开
  发者中的查看器，查看网页脚本，找到需要提取信息所对应的脚本内容。启动新的爬虫项目，编写好
  items和spiders，爬取相应信息。并将爬取下来的信息另存到新的文件。

* 将爬取的信息利用Python语言进行清洗，去除掉评论人数过少导致评分缺失的数据，对数字以外的字
  符进行删除，并将新数据转化为数值型。

* 分别利用R和Python语言实现对2015年内地进上映电影进行K均值聚类，将实现过程分别写入Mapper和
Reducer。

## 建立K均值聚类模型


初始的数据集较为杂乱，我们需要重新对数据进行清洗和整合，按行提取数据后首先删除数据中的除数
字外的信息。并将数据格式转化为数值型。

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


Hadoop的MapReduce技术，Mapper主要用于实现读取数据完输入数据并完成数据分割后开始运行。每个
分割后的切片数据都会以键值对数据进行输出。


	#! /usr/bin/env Rscript
	
	input <- file("stdin","r")
	
	A<-c()
	B<-c()
	
	while(length(currentLine <- readLines(input,n=1,warn=FALSE))>0)
	{
	    fields <- unlist(strsplit(currentLine,","))
	    a=as.double(fields[1])
	    b=as.double(fields[2])
	    A=c(A,a)
	    B=c(B,b)
	}
	mydata <- data.frame(A,B)
	
	scale01=function(x){
	    ncol=dim(x)[2]
	    nrow=dim(x)[1]
	    new=matrix(0,nrow,ncol)
	    for(i in 1:ncol)
	    {max=max(x[,i])
	        min=min(x[,i])
	        for(j in 1:nrow)
	        {new[j,i]=(x[j,i]-min)/(max-min)}
	    }
	    new
	}
	
	datanorm=scale01(mydata)
	print(datanorm,stdout())
	close(input)




而Reducer在接收Map阶段的输出数据，该数据以键为基础进行分组。Reducer用于对数据进行聚集，接
受Map的数据后产生键值，以作为每个分组的数值。从K均值聚类的流程来看，我们需要对数据进行标准
化处理，将处理后的数据变为0-1之间分布的数值。然后再建立模型。

在R版本的Reducer中引入R包e1071，利用cmeans函数分析数据，将其进行K均值聚类分析。将聚类数目
设置为4，迭代数目设为20次。

	
	#! /usr/bin/env Rscript
	
	input <- file("stdin","r")
	A<-c()
	B<-c()
	while(length(currentLine<-readLines(input,n=1,warn=FALSE))>0)
	{
	    fields=unlist(strsplit(currentLine," "))
	    a=as.double(fields[2])
	    b=as.double(fields[3])
	    A=c(A,a)
	    B=c(B,b)
	}
	
	mydata=data.frame(A,B)
	mydata=na.omit(mydata)
	data=as.matrix(mydata)
	
	library(e1071)
	results=cmeans(data,centers=4,iter.max=20,verbose=TRUE,method="cmeans",m=2)
	print(results)
	
	close(input)



在Python版本Reducer的该函数为给定数据集构建一个包含K个随机质心的集合，随机质心必须要在整个
数据集的边界内，这可以通过找到数据集每一维的最小和最大值来完成。然后随机生成0到1之间的随机
数，并通过取值范围和最小值，以便确保随机点在数据的边界之内：



	def randCent(dataSet, k):
	      n = shape(dataSet)[1]
	      centroids = mat(np.zeros((k,n)))
	      for j  in range(n):
	           minJ = min(dataSet[:, j])
	           rangeJ = float(max(dataSet[:,j]) - minJ)
	           centroids[:,j] = minJ + rangeJ * random.rand(k, 1)
	      return centroids


最后定义K均值算法的函数。一开始确定数据集中数据点的总数，然后创建一个矩阵来储存每个点的簇分配结果。簇分类结果有两列。一列记录簇的索引值，第二列储存误差。这里的误差指的是当前点到簇质心的距离。按照此种方式，反复迭代，知道所有数据点的簇分配结果不会改变为止。


	def kMeans(dataSet, k, distMeas=distEclud,createCent=randCent):
	    m = shape(dataSet)[0]
	    clusterAssment = mat(zeros((m,2)))
	    centroids = createCent(dataSet,k)
	    clusterChanged = True
	    while clusterChanged:
		  clusterChanged = False
	          for i in range(m):
	              minDist = inf; minIndex = -1
	              for j in range(k):
	                  distJI = distMeas(centroids[j,:],dataSet[i,:])
			  if distJI < minDist:
			     minDist = distJI; minIndex = j
		      if clusterAssment[i,0] != minIndex: clusterChanged = True
		      clusterAssment[i,:] = minIndex,minDist**2
	          print centroids
	          for cent in range(k):
		      ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]
	              centroids[cent,:] = mean(ptsInClust,axis=0)
		  return centroids,clusterAssment


（感谢中国人民大学陈晞提供素材和案例。）
