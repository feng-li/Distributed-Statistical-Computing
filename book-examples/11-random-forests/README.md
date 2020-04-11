# 实例分析：随机森林的并行实现


## 准备知识

* 随机森林
* Mahout
* Spark

## 研究背景

切伦科夫望远镜的目标是接收伽玛射线,其光子能量是可见光的亿亿倍。本 文主要收集由 MC 生成的模
拟大气切伦科夫望远镜接收的高能伽玛射线粒子的 大量数据,通过其属性指标判断其属于
gamma(sighal)事件,还是 hadron (background)事件;是一个二分类问题。



## 数据来源


数据来自 UCI 的大气切伦科夫望远镜项目的
[数据](http://archive.ics.uci.edu/ml/machine-learning-databases/magic/magic04.data)。数据
集共有 19020 个样本观测值,11 个变量。在服务器上,使用下面的 linux 命令直接下载数据。其中
URL_address_of_data 为上面的网址。

	$ wget -t inf URL_address_of_data




## 建立模型

基于分类问题的机器学习算法主要包括逻辑回归、朴素贝叶斯、决策树、神 经网络、隐马尔科夫,以及
建立在决策树之上的推广算法——随机森林,Boosting, Bagging 等等。决策树是一种简单易解释的模型,
在实际中运用非常广泛,但是 它自身存在很多缺点;随机森林是决策树的一种推广:它是一个包含多个决
策树的分类器,并且输出的类别是由个别树输出的类别的众数而定。随机森林提高了 决策树的准确率,
速度快,且易于进行并行计算。本文中对训练数据建立随机森林模型,并在测试集上计算误判率比较模型
的 优劣。


### 基于Mahout的实现
#### 划分训练集、测试集

在下载好的数据文件路径下,调用 mahout 实现训练集、测试集的划分(70% 为训练集、30%为测试集)。
具体命令如下:


	$ mahout splitDataset -i magic04.data -o splitdata -t 0.7 -p 0.3

划分后的训练集与测试集分别位于 splitdata 路径下的 trainingData 与 testData 中。这里需要注
意的是,直接调用 mahout 命令需要提前设置环境变量,否则, 需要用/home/dmc/mahout/bin/mahout 代
替 mahout.


#### 数据上传至 HDFS

首先在 Hadoop 文件系统中创建一个文件夹 pkuzcy 用于进行本次实验。之后上传的数据集以及建模结
果都存放在这里。


	$ hadoop fs –mkdir pkuzcy

注意,这里直接调用 hadoop 命令的前提是设置好环境变量 (/home/dmc/hadoop/bin/路径下的 hadoop)
如果没有设置,需要用 /home/dmc/hadoop/bin/hadoop 代替 hadoop. 上传文件至 HDFS:这样就把训练
集与测试集分别上传至文件系统中的 pkuzcy 路径下,可以用 下面的命令查看:


	$ hadoop fs –ls pkuzcy


#### 生成数据集描述

下载的数据集文本文件只有数据,没有相关数据的描述,在用 mahout 建立 随机森林模型之前,先对其构
建描述信息。

	$ hadoop jar $MAHOUT_HOME/mahout-examples-0.10.1-job.jar \
      org.apache.mahout.classifier.df.tools.Describe \
      -p pkuzcy/train.arff \
	  -f pkuzcy/train.info \
	  -d 10 N L

这里,$MAHOUT_HOME 代表/home/dmc/mahout.参数-p 表示输入文件,-f 表示输出文件;在 hadoop 平台
上调用 mahout,输入输出均为 HDFS 文件系统中 的数据。-d 表示要描述的数据集的变量信息,其后的
字符串“10 N L”表示从左到 右依次是 10 个数值型变量,最后的“L”表示要分类的变量。这里还可以输
入“C” 表示分类型变量(本例中没有分类型)。成功执行后,文件系统中 pkuzcy 路径下会出现
train.info 的文件。使用 cat 命 令查看该路径下所有的 info 文件。


	$ hadoop fs -cat pkuzcy/*.info


#### 训练模型

在训练集上建立随机森林模型,具体命令如下:

	$ hadoop jar $MAHOUT_HOME/mahout-examples-0.10.1-job.jar \
      org.apache.mahout.classifier.df.mapreduce.BuildForest \
		 -Dmapred.max.split.size=147739 \
         -d pkuzcy/train.arff \
		 -ds pkuzcy/train.info \
		 -sl 5 –p -t 100 -o magicForest
这里的 Dmapred.max.split.size 参数表示 hadoop 分布式计算每部分数据的最 大规模,默认为原始数据的十分之一,这里使用 147739 即为原始训练集的 1/10. 参数-sl 表示每棵树的使用随机的 5 个变量来构建;参数-p 表示分布式计算;参 数-t 表示子树的数量,这里取 100 棵;参数-o 表示建立好的模型存放在 magicForest 路径下。


	$ hadoop jar $MAHOUT_HOME/mahout-examples-0.10.1-job.jar \
      org.apache.mahout.classifier.df.mapreduce.TestForest \
        -i pkuzcy/test.arff \
		-ds pkuzcy/train.info \
		-m magicForest \
		-a -mr -o prediction

这里测试集的描述使用的是同训练集一样的描述信息。参数-m 表示使用的 模型,即为上面建立的模型
magicForest;参数-a 表示计算混淆矩阵;参数-mr 表示采用分布式计算;参数-o 表示预测结果存放在
prediction 路径下。输出的信息也有很多,包括文件系统读入、写出的数据量,map 的个数、计 算时间,混
淆矩阵,正确、错误判断分类的比率等等。混淆矩阵显示正确分类 4959 个样本,准确率为 87.77%;错分
了 691 个样本,错分率为 12.23%.


#### 训练误差

在原训练集上检验一下建立的模型,将输入数据文件改为 train.arff,结果输 出到 prediction-train
路径,其余参数不变。结果显示正确分类 13247 个样本,准确率为 99.08%;错分了 123 个样本,错分率
为 0.92%.比之测试集,正确率高了很多,模型可能存在过拟合现象。


####1000 棵子树的随机森林

更改子树数量参数,构建 1000 棵决策树再次建立模型,并在测试集上检验。结果显示正确分类 4974 个
样本,准确率为 88.04%;错分了 676 个样本,错分率为11.96%. 与上面 100 棵树的模型比较,准确率有
一点提高,但是子树数量的增多增加了计算的代价,运行时间反而增多。所以根据结果可知,采用 100 棵
树建立随机 森林模型已经足够。



### 基于Spark的实现

Spark 拥有多种语言的函数式编程 API,提供了除 map 和 reduce 之外更多的 运算符,这些操作是通过
一个称作弹性分布式数据集(resilient distributed datasets, RDDs)的分布式数据框架进行的。由于
RDD 可以被缓存在内存中,Spark 对迭代 应用特别有效。Spark 非常快,可以通过类似 Python REPL 的
命令行提示符交互 式访问。Spark 的核心组件之一 MLlib 是一个常用的机器学习算法库,算法被实现
为 对 RDD 的 Spark 操作。这个库包含可扩展的学习算法,比如分类、回归等需要 对大量数据集进行
迭代的操作。之前可选的大数据机器学习库 Mahout,将会转 到 Spark,并在未来实现。


#### 读入数据

打开 PySpark 的交互式终端(输入命令“pyspark”)。PySpark 将会自动使用本 地 Spark 配置创建一个
SparkContext,可以通过 sc 变量来访问它。创建第一个 RDD。

	$ data = sc.textFile(‘magic04.data’)

上述命令将下载的数据集 magic04.data 加载到一个 RDD 命名文本。 3.3.2 转化格式并划分训练集定
义一个函数将上面的数据转化为 spark 分类算法需要的 RDD 格式 (LabeledPoint)。

	from pyspark.mllib.regression import LabeledPoint
	def parsedata(line):
		newline = [a for a in line.split(',')]
		X = [float(x) for x in newline[:10]]
		Y = newline[-1]
		y = 0 if Y=='g' else 1
	    return LabeledPoint(y,X)


对 data 应用该函数。对转化后的数据 parseddata 进行训练集与测试集的划 分。

	$ parseddata = data.map(parsedata)
	## Split the data into training and test sets (70%-training)
	$ (trainingData, testData) = parseddata.randomSplit([0.7, 0.3])

#### 训练模型

依然选取 100 棵树在训练集上训练随机森林模型。设置树深为 4,选取 gini指标构建每一棵决策树。

	from pyspark.mllib.tree import RandomForest
	$ model = RandomForest.trainClassifier(trainingData, \
		numClasses=2, categoricalFeaturesInfo={},numTrees=100,\
		featureSubsetStrategy="auto",impurity='gini', maxDepth=4)
#### 检验模型

在测试集上应用上面建立的模型来分类,并与测试集的标准交过作比较,计算误判率,以此来检验模型的
优劣。

	$ predictions = model.predict(testData.map(lambda x:
        \ x.features))
	labelsAndPredictions = testData.map(lambda lp: lp.label
        \ ).zip(predictions)
	cetestErr = labelsAndPredictions.filter(lambda (v, p):
        \ v != p).count() / float(testData.count())
	print('Test Error = ' + str(testErr))

如果要查看每个子树的具体情况,可以用下面的命令输出:


	$ print(model.toDebugString())

还可以加载 matplotlib 包绘制图像。 计算得出在测试集上的误判率为 17.11%。


## 结论

基于 Mahout 的随机森林实现,100 棵树的模型误判率为 12.23%,1000 棵树 的误判率为 11.96%;子树
的增加使模型准确率略有提升,同时付出了时间的代 价。鉴于两个模型的准确率相差不大,但是计算时
间有较大差别,实际中采用适 当的树即可训练出比较满意的模型。

基于 Spark 的随机森林实现,100 棵树的模型误判率为 17.11%,与基于 Mahout 实现的模型误判率有出
入。这是因为随机森林模型本身就有一定的随机性;另外,本次实验为了测试 Mahout 与 Spark 语句,用
于建立模型的训练集与 测试集是分别划分的,这对于模型的结果也有很大影响。此外,需要注意的
是,Spark 运行的时间明显比在 hadoop 之上 Mahout 实现 的运行时间短很多,这体现了 Spark 的优势。

（感谢北京大学张楚妍提供素材和案例。）
