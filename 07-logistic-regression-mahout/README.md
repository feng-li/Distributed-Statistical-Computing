# 实例分析：Mahout 机器学习研究红酒质量影响因素


## 准备知识

* Logistics回归和随机森林分类算法
* Mahout和R
* Hadoop Streaming

## 研究背景

本案例主要使用 Hadoop 和 Mahout 的机器学习算法对实际数据完成分类问题的学 习. 为了实践机器
学习算法,使用 UCI 机器学习库的红酒质量数据集,学习的内容为根据红酒的一些属性判断红酒质量水
平. 在这里使用了的分类方法为 Logistic 回归、随机森林. 从 Logistic 回归得到的结果发现酒精浓
度、密度、糖分量等和红酒质量是正相关的,氯化 钠含量、柠檬酸含量、挥发性酸含量等和红酒质量是
负相关的. 通过随机森林的学习,我 们依据红酒属性得到对红酒质量的判断可以达到很高的准确性.

## 数据准备

###数据信息

本次报告分析的数据集是来自UCI机器学习库的红酒质量数据集(网
址:http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/). 该数据集包含
1599 个样本,13 个变量,其中 1 个变量为样本序号、11 个变量为红酒一些属性的数值描 述、1 个变
量为该红酒样本的质量评分.

### 数据预处理

从 UCI 机器学习库直接下载得到的数据集 winequality-red.csv 是分号分割格式的数据, 且没有变量
名信息,参考它提供的文件 winequality.names,使用 R 读入数据,并添加变量 名信息. 为了比较不同
机器学习的算法,首先,使用分层随机抽样的方式(根据因变量quality 分层),取数据集的 70% 为训练集,剩
下的 30% 作为测试集. 拆分后,训练集 共有 1120 个样本,测试集共有 479 个样本,分别保存为文件
train_redwine.csv 和 test_redwine.由于Logistic回归要求的因变量为二分类变量,而这里因变量
quality可以有3、4、5、 6、7、8 共 6 种取值,分别代表红酒的质量从低到高. 这里粗略地将响应变
量 quality 分为 两类,其中品质评分 3、4、5 的归为一类,用 0 表示,表示红酒品质一般;品质评分 6、
7、8 的归为一类,用 1 表示,表示红酒品质较好.

## 使用 Mahout 计算 Logistic 回归

Logistic 回归常是一种有效的分类问题学习方法,并且模型可解释性较好. 然而它的求 解算法是迭代的,在 Hadoop 分布式计算中的 MapReduce 一般要求算法是可以拆分并行
进行的,也就是要求算法不是迭代的. 所以要分布式计算 Logistic 回归的解,简单的对 Logistic 回归求解的迭代算法拆分成 Map 和 Reduce 两个部分是不合理的.所以要在 Hadoop 上使用 MapReduce 计算 Logistic 回归的解,一般定义 Mapper 函数 和 Reducer 函数为:

1. Mapper:将n个样本的数据集拆分成k个子集,分别在k个子集上使用随机梯度下降(Stochastic
   Gradient Descent,简称 SGD)算法计算 Logistic 回归的解.

2. Reducer:计算Mapper中得到的k个Logistic回归解的均值作为Logistic回归的解.

在数学上可以证明,当样本数 n 趋于无穷时,以上得到的 Logistic 回归解有相合性, 且该估计量的分
布是渐进正态的. 并且实际计算中,单个程序中 Logistic 回归解的求解使 用的SGD算法的计算速度是
很快的. 所以以上提出的MapReduce算法计算Logistic解可以 做到维持估计准确性的同时提高计算速度.


### Logistic 回归模型训练

因为在这个问题中我们使用的数据集样本量仅 1000 多,所以为了计算的准确性,仅使用单机模式计算模
型的解. 在 Linux 系统下的 Mahout 下计算 Logistic 的解的代码如下。




	$ mahout trainlogistic --input train_redwine.csv \
      --output ./logit_model \
      --target quality --categories 2 \
      --predictors fixed.acidity volatile.acidity citric.acid \
      residual.sugar chlorides free.sulfur.dioxide total.sulfur.dioxide \
      density pH sulphates alcohol --types numeric \
      --features 20 --passes 100


以上代码在存放数据集train_redwine.csv和test_redwine.csv的目录下运行. 其中使用的选项包括:

- `trainlogistic`代表计算Logistic回归的模型解

- `--input`选择输入的数据集为train_redwine.csv

- `--output`代表将结果输出到当前目录下的文件logit_model中

- `--target`说明
因变量为quality,并告知Mahout系统它的类型为2分类的分类变量

- `--predictors`说明自变量为紧接
着的11个变量,并告知Mahout它们都是数值型变量

- `--features`说明建模型时使用的的内部特征向量
大小

- -`-passes`说明在学习模型的时候输入数据需要重检查的次数

输出结显示对红酒品质有正影响的变量包括酒精浓度、柠檬酸 含量、密度、非挥发性酸含量、游离二
氧化硫含量、酸碱度、残余糖分量、硫酸钾含量; 对红酒品质有负影响的变量包括氯化钠含量、柠檬酸
含量、总二氧化硫含量、挥发性酸含量. 事实上,Logistic 回归得到的结果对各属性对品质影响的解释
与显示是相符的.


### Logistic 回归模型测试

通过以上得到的 Logistic 模型对测试集做模型检测的代码如下。


	$ mahout runlogistic --input test_redwine.csv \
	  --model ./logit_model --auc --confusion

以上代码中使用的选项包括:

- `runlogistic`代表通过测试集检验之前得到的Logistic回归的模型解的效果

- `--input`说明使用的测试集为test_redwine.csv

- `--model`说明使用的Logistic回归模型结果文件为logit_model

- `--auc`表示输出模型的AUC得分,即ROC曲线下方的面积占比

- `--confusion`表示输出混淆矩阵


输出结果显示该模型的 AUC 得分为 0.64 > 0.5 ,说明训练的效果还可 以. 混淆矩阵显示品质为 0 的
223 个红酒样本有 148 个被判断为 0,75 个判断为 1;品质 为 1 的 256 个红酒样本有 121 个被判断
为 0,135 个被判断为 1. 从混淆矩阵显示的误判 率可以看出 Logistic 回归的模型学习结果不够令人
满意.

## 使用 Mahout 计算随机森林

随机森林是一种机器学习集成算法,它的思想基于使用多个弱分类器得到强分类器. 随机森林算法基于
决策树的算法。随机森林算法事实上建立的多个决策树是可以并行计算的。在测试结果的时候，也可以
并行计算多个个决策树的分类结果.所以要在 Hadoop 上使用 MapReduce 建立随机森林的模型,一般定
义 Mapper 函数和 Reducer 函数为:1. Mapper:在各个子节点上并行地分别抽取训练样本和输入变量,
建立决策树. 2. Reducer:整合各个子节点计算得到的多个决策树.

### 数据准备

在 Linux 系统下的 Mahout 下并行计算随机森林模型要求的输入数据集是纯数据集, 不包含变量信息,所以我们将 Logistic 回归中使用的数据集 train_redwine.csv 和 test_redwine.csv 删除首行变量名信息,并删除红酒样本序号一列,得到数据集 redwine_train.arff 和 redwine_test.arff.为了使用 Hadoop 并行计算完成 Mahout 的随机森林的计算,首先要将数据集 redwine_train.arff 和 redwine_test.arff 放入 HDFS 中,代码如下:

    $ hadoop fs –put redwine*

因为数据集 redwine_train.arff 和 redwine_test.arff 本身没有变量信息,要在随机森林 算法中学
    习,需要建立变量信息文件,可以使用 Mahout 中的 Describe 工具创建变量信息 文件,代码如下:

    $ hadoop jar $MAHOUT_HOME/mahout-examples-0.10.1-job.jar \ >
      org.apache.mahout.classifier.df.tools.Describe \
      > -p redwine_train.arff \
      > -f redwine_train.info \
      > -d 11 N L


以上代码使用 Hadoop 运行 Mahout 的方法 classifier.df.tools.Describe,其中使用的选项包 括:

- `-p`说明要生成的变量信息用于描述数据集redwine_train.arff

- `-f`说明生成的变量信息保存为文件redwine_train.info

- `-d`说明数据集中的变量信息,后面的内容意思为该数据集中的变量前11个都是数值 型,最后一个是
因变量可以通过如下语句查看生成的变量信息文件 redwine_train.info 内容:

        $ hadoop fs -cat redwine_train.info

为了训练集合变量描述两个数据集在并行计算中其他计算机的使用,需要修改它们的使用权限,代码如下:

	$ hadoop fs -chmod 751 redwine_train.arff
	$ hadoop fs -chmod 751 redwine_train.info


### 随机森林模型训练


在 Hadoop 中并行计算 Mahout 的随机森林模型代码如下:

	$ hadoop jar $MAHOUT_HOME/mahout-examples-0.10.1-job.jar \
	  > org.apache.mahout.classifier.df.mapreduce.BuildForest \
      > -d redwine_train.arff \
      > -ds redwine_train.info \
      > -o redwine_forest \
      > -sl 5 -t 100


以上代码使用 Hadoop 的 MapReduce 运行 Mahout 的机器学习算法建立随机森林,其中使 用的选项包括:

- `-d`说明使用的训练集redwine_train.arff

- `-ds`说明使用的变量描述文件redwine_train.info

- `-o`说明将计算得到的随机森林模型结果输出到目录redwine_forest下

- `-sl`说明建立每个决策树时随机选择的自变量数,在此定义为5

- `-t`说明建立的决策树数目,在此定义为100

### 随机森林模型测试

使用测试集测试如上生成的随机森林模型的效果代码如下:

	$ hadoop jar $MAHOUT_HOME/mahout-examples-0.10.1-job.jar \
	> org.apache.mahout.classifier.df.mapreduce.TestForest \
    > -i redwine_test.arff \
    > -ds redwine_train.info \
    > -m redwine_forest \
    > -o redwine_prediction \
    > -a

其中使用的选项包括

- `-i`说明使用的测试集redwine_test.arff

- `-ds`说明使用的变量描述文件redwine_train.info

- `-m`说明测试的模型来自目录redwine_forest

- `-o`说明测试输出的结果输出到目录redwine_prediction下

- `-a`要求输出混淆矩阵

得到的随机森林模型测试输出结果可以看到随机森林的正确率高达 98.33%. Logistic 模型的测试结果
的混淆矩阵,随机森林模型的准确性十分高. 虽 然随机森林的判断结果准确性更高,但是模型解释性相
较 Logistic 回归模型较差,我们没 有办法通过输出的结果说明红酒的各个属性变量在判断红酒质量方
面的贡献. （感谢北京大学张诗玉提供素材和案例。）
