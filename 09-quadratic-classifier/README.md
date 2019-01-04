# 实例分析：用 Spark 进行二分类学习


## 准备知识

* 二分类学习
* Spark



## 数据准备

本文使用的数据来源于大数据竞赛平台 Kaggle 上的一个比赛数据,数据集由 StumbleUpon 提供,见数
据[下载地址](https://www.kaggle.com/c/stumbleupon/data?train.tsv)。由于 test.tsv 数据为测
试数据, 没有提供完整的数据,缺少我们需要预测的变量,所以我们选用的是 train.tsv 数据,该数据集
含有 7395 个网页的相关信息。

## 模型建立

### 数据预处理

我们看到数据集一共有 27 个变量,前三个变量分别为 URL 地址,该页面在 StumbleUpon 的 ID,该页
面原始的文本内容,前两个在分析时用于标记网页,可以不考虑,第三个变量由于是文本数据,为了简 单
期间,本文也不考虑文本数据。于是接下来要使用的变量为 4-27.我们对数据做如下处理。

* 将第四个变量 alchemy_category 的字符串类型转换为数值型,即用 1-14 这 14 个数字分别指代 各
  个类别;

* 将数据集中多余的双引号去掉,将缺失数据替换为 0;
* 将 label 变量转换为 Int 型。 其余的处理在具体运用具体模型时再具体说明。

### 训练逻辑回归模型

我们将预处理后的数据集除去 label 变量外进行标准化处理,然后使用 MLlib 库中的
LogisticRegressionWithSGD 函数进行逻辑回归模型的学习,迭代次数设置为 50 次。然后再使用学习
到的模型计算训练集上的预测正确率,同时计算该模型准确率-召回率(PR)曲线下的面积以及 ROC 曲 线
下的面积。以此三个结果来综合评价逻辑回归模型的性能。

### 训练 SVM 模型

类似逻辑回归模型的处理,我们将数据集进行标准化处理,然后使用 MLlib 库中的 SVMWithSGD 函数 进
行 SVM 二分类模型的学习。迭代次数设置为 50 次。然后同样计算该模型在训练集上的预测正确率,
PR 曲线和 ROC 曲线下的面积。

### 训练朴素贝叶斯模型

由于标准化处理对朴素贝叶斯模型没有太大意义,我们对原数据集不进行标准化处理,但是由于朴素贝
叶斯模型要求特数据特征矩阵中的特征值非负,因此我们在计算出数据集的特征矩阵后将小于 0 的特征
值设置为 0.然后使用 MLlib 库中的 NaiveBayes 函数进行朴素贝叶斯模型学习。然后计算该模型在训
练 集上的预测正确率,以及 PR 曲线和 ROC 曲线下的面积。


### 训练决策树模型

标准化处理对决策树同样没有太大意义,我们直接使用预处理后的数据进行分析。使用 MLlib 库中的
DecisionTree 函数进行二分类决策树学习,设置决策树的最大深度为 10.然后计算该模型在训练集上的
预测正确率,以及 PR 曲线和 ROC 曲线下的面积。


##结果分析

将各个模型的训练结果列表如下:

	模型       训练集上正确率   PR 曲线下面积    ROC 曲线下面积
	逻辑回归      66.87%         76.09%          66.81%
	SVM           66.60%         75.92%          66.53%
	朴素贝叶斯    60.96%         74.05%          60.51%
	决策树        75.84%         82.64%          75.91%

从上表可以看出,四个二分类模型中,朴素贝叶斯的学习效果最差,决策树的学习效果最好,逻辑回归 和
SVM 的学习效果基本一致。


对于上述结果而言,即是是效果最好的决策树,在训练集上的预测正确率也只有 75%,这并不是特别理 想
的结果,对于这一结果,可以改进的方向便是添加对文本数据的处理,将网页的文本描述考虑到分类 中来,这
样对于结果的预测准确性应该会有较大的提升,因为网页文本内容所承载的信息是非常多的, 在决定网
页推荐是否长久上来说也是会有比较重要的决定性作用的。


## Spark 源代码

```
// 类别+标准化
// 使用 spark-shell 运行代码:./bin/spark-shell --driver-memory 8g

// 训练集数据处理
val rawData = sc.textFile("/home/hadoop/Documents/train_new.tsv") val records = rawData.map(line => line.split("\t"))
records.first()

import org.apache.spark.mllib.regression.LabeledPoint
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.feature.StandardScaler
import org.apache.spark.mllib.evaluation.BinaryClassificationMetrics
val categories = records.map(r => r(3)).distinct.collect.zipWithIndex.toMap val numCategories = categories.size
val dataCategories = records.map{ r =>
val trimmed = r.map(_.replaceAll("\"",""))
val label = trimmed(r.size - 1).toInt
val categoryIdx = categories(r(3))
val categoryFeatures = Array.ofDim[Double](numCategories) categoryFeatures(categoryIdx) = 1.0
val otherFeatures = trimmed.slice(4, r.size -1).map(d => if (d == "?") 0.0 else d.toDouble) val features = categoryFeatures ++ otherFeatures
LabeledPoint(label, Vectors.dense(features))
}
val scalerCats = new StandardScaler(withMean = true, withStd = true).fit(dataCategories.map(lp => lp.features)) val scaledDataCats = dataCategories.map(lp => LabeledPoint(lp.label, scalerCats.transform(lp.features)))
val dataNB = records.map{r =>
val trimmed = r.map(_.replaceAll("\"",""))
val label = trimmed(r.size - 1).toInt
val categoryIdx = categories(r(3))
val categoryFeatures = Array.ofDim[Double](numCategories) categoryFeatures(categoryIdx) = 1.0
LabeledPoint(label, Vectors.dense(categoryFeatures))
}
val numData = dataCategories.count

// 训练分类模型
import org.apache.spark.mllib.classification.LogisticRegressionWithSGD import org.apache.spark.mllib.classification.SVMWithSGD
import org.apache.spark.mllib.classification.NaiveBayes
import org.apache.spark.mllib.tree.DecisionTree
import org.apache.spark.mllib.tree.configuration.Algo
import org.apache.spark.mllib.tree.impurity.Entropy
val numIterations = 50 val maxTreeDepth = 10
// logistic regression
val lrModelScaledCats = LogisticRegressionWithSGD.train(scaledDataCats, numIterations) val lrTotalCorrectScaledCats = scaledDataCats.map { point =>
if (lrModelScaledCats.predict(point.features) == point.label) 1 else 0 }.sum val lrAccuracyScaledCats = lrTotalCorrectScaledCats / numData
val lrPredictionsVsTrueCats = scaledDataCats.map{point =>
(lrModelScaledCats.predict(point.features), point.label)}
val lrMetricsScaledCats = new BinaryClassificationMetrics(lrPredictionsVsTrueCats)
val lrPrCats = lrMetricsScaledCats.areaUnderPR
val lrRocCats = lrMetricsScaledCats.areaUnderROC
println(f"${lrModelScaledCats.getClass.getSimpleName}\nAccuracy:${lrAccuracyScaledCats * 100}%2.4f%%\nArea under PR: ${lrPrCats * 100.0}%2.4f%%\nArea under ROC: ${lrRocCats * 100.0}%2.4f%%")
// SVM
val svmModelScaledCats = SVMWithSGD.train(scaledDataCats, numIterations) val svmTotalCorrectScaledCats = scaledDataCats.map { point =>
if (svmModelScaledCats.predict(point.features) == point.label) 1 else 0 }.sum val svmAccuracyScaledCats = svmTotalCorrectScaledCats / numData
val svmPredictionsVsTrueCats = scaledDataCats.map{point =>
(svmModelScaledCats.predict(point.features), point.label)}
val svmMetricsScaledCats = new BinaryClassificationMetrics(svmPredictionsVsTrueCats) val svmPrCats = svmMetricsScaledCats.areaUnderPR
val svmRocCats = svmMetricsScaledCats.areaUnderROC
println(f"${svmModelScaledCats.getClass.getSimpleName}\nAccuracy:${svmAccuracyScaledCats * 100}%2.4f% %\nArea under PR: ${svmPrCats * 100.0}%2.4f%%\nArea under ROC: ${svmRocCats * 100.0}%2.4f%%")
// Naive Bayes
val nbModelCats = NaiveBayes.train(dataNB) val nbTotalCorrectCats = dataNB.map { point =>
if (nbModelCats.predict(point.features) == point.label) 1 else 0 }.sum val nbAccuracyCats = nbTotalCorrectCats / numData
val nbPredictionsVsTrueCats = dataNB.map{point =>
(nbModelCats.predict(point.features), point.label)}
val nbMetricsCats = new BinaryClassificationMetrics(nbPredictionsVsTrueCats)
val nbPrCats = nbMetricsCats.areaUnderPR
val nbRocCats = nbMetricsCats.areaUnderROC
println(f"${nbModelCats.getClass.getSimpleName}\nAccuracy:${nbAccuracyCats * 100}%2.4f%%\nArea under PR: ${nbPrCats * 100.0}%2.4f%%\nArea under ROC: ${nbRocCats * 100.0}%2.4f%%")
// decision tree
val dtModelCats = DecisionTree.train(dataCategories, Algo.Classification, Entropy, maxTreeDepth) val dtTotalCorrectCats = dataCategories.map { point =>
val score = dtModelCats.predict(point.features) val predicted = if (score > 0.5) 1 else 0
if (predicted == point.label) 1 else 0 }.sum
val dtAccuracyCats = dtTotalCorrectCats / numData
val dtPredictionsVsTrueCats = dataCategories.map{point =>
(dtModelCats.predict(point.features), point.label)}
val dtMetricsCats = new BinaryClassificationMetrics(dtPredictionsVsTrueCats) val dtPrCats = dtMetricsCats.areaUnderPR
val dtRocCats = dtMetricsCats.areaUnderROC
println(f"${dtModelCats.getClass.getSimpleName}\nAccuracy:${dtAccuracyCats * 100}%2.4f%%\nArea under PR: $ {dtPrCats * 100.0}%2.4f%%\nArea under ROC: ${dtRocCats * 100.0}%2.4f%%")
```


（感谢北京大学刘智彬提供素材和案例。）
