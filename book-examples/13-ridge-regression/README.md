# 实例分析：利用MapReduce计算岭回归模型系数



## 准备知识

* Ridge Regression
* R
* Mapreduce


## 研究背景

本案例分析的数据来源于R软件中“ISLR”包的数据集Hitters，其包含了美国职棒大联盟1986年至1987年
间球员各方面的数据。数据的变量包括球员跑垒数、击打数、失误数、在联盟中的年数等，因变量为球
员的薪资。不难想象，这样的数据是容易存在多重共线性问题的，因此不能使用最小二乘估计系数值，
而需要用其他的估计方法。本文采用的是岭回归方法。

虽然数据集Hitters并不具有一般认为的大数据的量级，但是本次作业的重点为并行方法的实现，因此
并无大碍。

## 数据准备


在数据生成部分，进行的步骤如下。首先加载ISLR包并读取数据，其次对自变量进行标准化处理，另外
注意到数据集中分类型自变量均只有两个水平，因此将它们编码为0和1，作为虚拟变量处理。此外，为
了在最后检验模型的预测效果及筛选λ值，对数据进行70%作为训练集、30%作为测试集的划分，最后将
划分的结果保存，分别命名为train.csv和test.csv。


	#! /usr/bin/env Rscript
	#Data generation
	library(ISLR)
	data = Hitters
	data = na.omit(data)
	data$League = as.character(data$League)
	data$League[data$League == "A"] = 0
	data$League[data$League == "N"] = 1
	data$Division = as.character(data$Division)
	data$Division[data$Division == "E"] = 0
	data$Division[data$Division == "W"] = 1
	data$NewLeague = as.character(data$NewLeague)
	data$NewLeague[data$NewLeague == "A"] = 0
	data$NewLeague[data$NewLeague == "N"] = 1
	data$League = as.numeric(data$League)
	data$Division = as.numeric(data$Division)
	data$NewLeague = as.numeric(data$NewLeague)
	igno = -c(14, 15, 19, 20)
	data[, igno] = scale(data[, igno], center = T, scale = T)

	set.seed(2016)
	ind = sample(1:nrow(data), 0.3*nrow(data))
	tr = data[-ind, ]
	te = data[ind, ]
	write.csv(tr, 'train.csv', row.names = F)
	write.csv(te, 'test.csv', row.names = F)


## 建立模型

参照岭回归系数的计算公式，比较好的解决方案是先利用并行计算出维度较高、计算量较大的矩阵和，
在最后汇总时再考虑λ引起的收缩并计算出β。因此，本文用到了两个mapper和两个reducer，分别用于
计算前文所述的两个维度较高的矩阵。以计算的mapper和reducer为例，mapper的输入为、（n×p或p×n
维）矩阵，但其计算和输出的是中每一行与分别相乘的结果，而reducer则对每一个这样的结果进行按
行求和，得到p个1×p维的向量，并按照这些向量在中相应的顺序进行排序，便可以得到计算的结果。这
样子大大减少了每个步骤的计算量，能够有效的提高计算速度。

### Mapper部分

	#! /usr/bin/env Rscript
	options(warn = -1)
	sink("/dev/null")
	input = file("stdin", "r")

	read = readLines(input, warn = FALSE)
	temp = strsplit(read[-1], split = ",")
	len = length(temp)
	temp1 = as.numeric(unlist(temp))
	data = matrix(temp1, nrow = len, byrow = T)
	x = t(cbind(1, data[, -(ncol(data)-1)])) #Intercept

	for(i in 1:nrow(x))
	{
	    sink()
	    out = x[i, ] * t(x)
	    cat(out,"\n")
	    sink("/dev/null")
	}

	close(input)


### Reducer部分

	#! /usr/bin/env Rscript
	options(warn = -1)
	sink("/dev/null")

	input = file("stdin", "r")
	temp = strsplit(readLines(input), split = " ")
	len = length(temp)
	temp1 = lapply(temp, as.numeric)
	temp2 = lapply(temp1, matrix, ncol = len, byrow = F)
	temp3 = lapply(temp2, colSums)

	out = matrix(unlist(temp3), ncol = len)
	write(out, "txx.txt", ncolumns = len)
	close(input)

### 汇总部分

最后的汇总部分代码直接读取了MapReduce的输出结果，由于其维数为p×p维，这时已经可以直接对矩阵
进行计算。

在选择最佳的λ值时，使用的方法是运行简单的循环，找出测试集均方误差最小时对应的λ值即是最后的
结果。


	#! /usr/bin/env Rscript
	txx = read.table('txx.txt', sep = ' ')
	txx = as.matrix(txx)
	txy = read.table('txy.txt', sep = ' ')
	txy = as.matrix(txy, ncol = 1)
	te = read.table('test.csv', sep = ',', header = T)
	lambda = seq(0, 10000, length = 1001)
	tee = numeric()
	for(i in lambda)
	{
	  bhat = solve(txx + diag(nrow(txx)) * i, txy)
	  tey = as.matrix(cbind(1, te[, -(ncol(te) - 1)]))%*%bhat
	  tee = c(tee, mean((tey - te[, ncol(te) - 1])^2))
	}
	lambda = seq(1, lambda[which.min(tee)])
	tee = numeric()
	for(i in lambda)
	{
	  bhat = solve(txx + diag(nrow(txx)) * i, txy)
	  tey = as.matrix(cbind(1, te[, -(ncol(te) - 1)]))%*%bhat
	  tee = c(tee, mean((tey - te[, ncol(te) - 1])^2))
	}
	lambda = which.min(tee)
	print("Lambda:")
	print(lambda)
	print("MSE:")
	print(tee[lambda])
	out = solve(txx + diag(nrow(txx)) * lambda, txy)
	rownames(out) = c("Intercept", names(te)[-19])
	colnames(out) = "Coefficients"
	print(out)



（感谢中央财经大学刘利恒提供素材和案例。）
