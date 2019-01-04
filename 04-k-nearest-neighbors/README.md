# 实例分析：MapReduce 框架下的 KNN 算法实现

## 准备知识

* KNN分类算法
* R
* Hadoop Streaming

## K最近邻算法（KNN）


k-最临近分类法是一个理论上比较成熟的机器学习算法,该方法的思路是: 如果一个样本在特征空间中
的 k 个最相似(即特征空间中最邻近)的样本中的大 多数属于某一个类别,则该样本也属于这个类别。
KNN 算法中,所选择的邻居都 是已经正确分类的对象。该方法在定类决策上只依据最邻近的一个或者几
个样本 的类别来决定待分样本所属的类别。



## 数据介绍

## 建立KNN分类模型

### Mapper函数

1. 需对所有样本点(训练集+测试集)进行归一化处理。 然后,对未知分类的数据集中的每个样本点依次
   执行以下操作。

2. 计算训练集中的点与当前点(测试集)的距离。

3. 按照距离递增排序。

4. 选取与当前距离最小的 k(取 5)个点。

5. Map 函数的输出为:测试集实际的分类及与当前距离最近的 k 个 点所属类别。


		#! /usr/bin/env Rscript
		sink("/dev/null")
		# 读取iris数据集
		input<-file("stdin","r")
		rawdata<-read.table(input)
		k=5
		# 归一化
		data<-cbind(as.data.frame(scale(rawdata[,1:4])),
                    Species=raw data[,5])
		# 随机选择其中的120条记录作为训练集,30条作为测试集
		sampleid<-sample(1:150,120)
		train <- data[sampleid,]
		test <- data[-sampleid,]
		#对测试集的每一个样本执行如下步骤
		for(i in 1:nrow(test)){
			#记录与每个训练集的距离及该样本的分类
			dis2train <- matrix(rep(0,nrow(train)*2),ncol=2)
			# 计算距离并保存训练集的分类信息
			for(j in 1:nrow(train)){
				dis2train[j,1] <- dist(rbind(test[i,1:4],train[j,1:4]),
                                       method="euclidean")
				dis2train[j,2] <- train[j,5]
			}
			#按距离从小到大排序
			sorteddis2train<-dis2train[order(dis2train[,1]),]
			sink()
			#将测试集实际的分类及与当前距离最近的k个点所属类别
			cat(test[i,5],sorteddis2train[1:k,2],"\n",sep="\t")
			sink("/dev/null")
		}
		close(input)


### Reducer 函数

1. 前 k 个点出现频率最高的类别作为当前点的预测类别。

2. Reduce 函数的输出为:测试集的实际分类及预测分类。




		#! /usr/bin/env Rscript
		sink("/dev/null")
		#读取map的输出
		input <- file("stdin","r")
		species <- read.table(input)
		for(i in 1:nrow(species)){
			#计算频率
			freq <- as.data.frame(table(species[i,2:5]))
			#将频率从大到小排列
			sortedfreq <- freq[order(-freq$Freq),]
			sink()
			#输出测试集的实际分类及预测分类
			cat(as.character(species[i,1]),
                as.character(sortedfreq[1,1] ),'\n',sep='\t')
			sink("/dev/null")
		}
		close(input)




## 实验结果


使用测试集测试 k 近邻模型的准确度,混淆矩阵如下表所示。



	             setosa versicolor virginica
	setosa         11        0         0
	versicolor      0        12        1
	virginica       0        1         5


（感谢北京大学吴雅雯提供素材和案例。）
