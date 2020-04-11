# 实例分析：术后病人安置方案的决策树模型


## 准备知识

* 决策树模型
* Python和Spark



## 数据介绍


### 数据来源


本文研究数据是由 UC Irvine Machine Learning Repository,即加州大学欧文分校机器学习库提供的
1993 年某医院关于病人手术后体征表现的数据集
(http://archive.ics.uci.edu/ml/datasets/Post-Operative+Patient)。该数据集的主要分类任务是
决定术后恢复区的病人是否应当被转移到特护病房、普通病房,或者直接出院回家。由于体温降低是衡
量术后恢复状况的一个重要指标,因此本数据集中的病人体征指标主要考察病人手术后的体温水平。

###数据预处理

原始数据集包含 90 个观测,9 个变量,其中有 1 个因变量,8 个自变量。由于原始数据集中因变量一列
中包含 3 个缺失数据,因此删去这 3 个观测,最终得到含 87 个观测、9 个变量的有效数据。为了方便
后续建模过程的运算,我们依次将分类变量的字符串值分别转化成数值型,如将“低”、“中”、“高”分别记
为“1”、“2”、“3”。

## 建立模型

### 数据读入

由于 Spark 中用于建立决策树的数据集必须为 LabeledPoint 格式,因此我们在读入 csv 格式的数据
之后,必须对现有数据集进行格式转换。LabeledPoint 是 Spark 中独有的一种标签数据集格式,数据结
构分为 label 和features 两部分。具体结构为,label index1:value1 index2:value2 ...,其中
label 为标签数据,index1,index2 为特征值序号,value1,value2 为特征值。

在 pyspark 中,我们可以用 pyspark.mllib.regression 模块中的“LabeledPoint”函数对读入的数据集
中的每一行进行格式转换,生成模型可识别的数据格式。具体代码如下:

	from __future__ import print_function
	from pyspark import SparkContext
	from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
	from pyspark.mllib.regression import LabeledPoint
	####定义格式转化函数 datatrans###
	def datatrans(d):
		t = [m for m in d.split(',')]
		y = float(t[0])-1
		x = [float(t) for t in t[1:]]
		return LabeledPoint(y,x)
	####对读入的数据集 mydata 的每一行进行格式转化###
	mydata = sc.textFile("/home/pku15/wei_sy/finalHWdata.csv")
	data = mydata.map(datatrans)


### 建立决策树

将已转化成 LabeledPoint 格式的数据集 data 分成 3:1 的两份,一份为训练集(75%),一份为测试集
(25%)。利用训练集的数据进行建模,选用 Gini 不纯度作为节点纯度的度量。具体代码如下:

	(trainingData, testData) = data.randomSplit([0.75, 0.25]) ###生成训练集和测试集
	Model = DecisionTree.trainClassifier(trainingData, numClasses=3,\
    categoricalFeaturesInfo={}, impurity='gini', maxDepth=5, maxBins=32)

### 在测试集上预测

基于训练集中建立好的决策树模型,用 predict 函数对预测集进行预测。得到预测集上的错分率 Test
Error = 39.29%,具体代码如下:


	predictions = model.predict(testData.map(lambda x: x.features))
	######计算错分率######
	labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
	testErr = labelsAndPredictions.filter(lambda (v, p): v != p).coun\
			  t()/ float(testData.count())
	print('Test Error = ' + str(testErr))
	print('Learned classification tree model: ' + model.toDebugString())

（感谢北京大学魏诗韵提供素材和案例。）
