# 实例分析：基于MapReduce的朴素贝叶斯模型


## 准备知识

* 朴素贝叶斯模型
* MapReduce
* Python

## 模型介绍

本案例使用朴素贝叶斯模型对文本进行分类。对于给定的一个文本，观察文档中出现的词，把每个词的
出现或者不出现作为一个特征。朴素贝叶斯模型假定：每个单词是否出现相互独立；每个特征同等重要。
在这个假定下，朴素贝叶斯模型的计算过程如下：

计算每个类别中的文档数目。对每篇训练文档： 对每个类别： 如果词条出现在文档中→增
加该词条的计数值 增加所有词条的计数值 对每个类别： 对每个词条： 将该词条的数目除以
总词条数目得到条件概率 返回每个类别的条件概率

## 数据来源

本案例所用的数据是来自craigslist网站的RSS源数据，从美国的纽约市和旧金山市分别选取25条广告，
通过分析这些人发布的信息来比较这两个城市的人们在用词上是否不同。即通过对文本建模分析，测试
一个文档可能出自哪个城市。

## 建立模型

### 获取数据

这一步骤的目的是从craigslist网站上获取RSS源数据，并将待分析的文本数据提取出来，保存到文件
中。首先使用feedparser库获取RSS源数据，提取craigslist网站上两个城市的信息，分别保存为ny和
sf。每个城市数据中，entries部分的summary对应的文本是本案例的分析对象，将其写入文件try.txt
中。代码如下：

	#! /usr/bin/python
	import feedparser

	sf=feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
	ny=feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
	f = open('try1.txt','w')
	for i in range(len(sf['entries'])):
        wordList = ny['entries'][i]['summary']
        f.write(wordList.replace('\n','')  +'\n')
        wordList = sf['entries'][i]['summary']
        f.write(wordList.replace('\n','')  +'\n')
	f.close()


### Mapper

这一步骤的目的是将try.txt文件中的原始数据读入，作分词处理，然后将处理后的数据映射到不同节
	点，以便作reduce处理。首先将数据按标准流读入，然后分词并标记类别，最后输出整理结果。代
	码如下。


    #!/usr/bin/python

	import sys
	import re


	def textParse(bigString):
	    listOfTokens = re.split(r'\W*', bigString)
	    return [tok.lower() for tok in listOfTokens if len(tok) > 2]

	for line in sys.stdin:
	    wordList = textParse(line)
	    print(str(wordList).strip('[]')



### Reducer

这一步骤的目的是读入mapper处理后的标准输出，建立模型，进行分类，计算误判率。模型建立过程如
下：

1. 解析读入的数据流，将处理后的文本加入指定的list。
2. 去掉出现次数最高的30个词（这些词在各条文本中使用频率高，对分类意义不大）
3. 随机构造训练集。
4. 对测试集分类。

代码如下。

	#! /usr/bin/env python
	import re
	import feedparser
	import random
	import sys
	from numpy import *



	docList=[]
	fullText =[]


	def bagOfWords2VecMN(vocabList, inputSet):
	    returnVec = [0]*len(vocabList)
	    for word in inputSet:
	        if word in vocabList:
	            returnVec[vocabList.index(word)] += 1
	    return returnVec

	def trainNB0(trainMatrix,trainCategory):
	    numTrainDocs = len(trainMatrix)
	    numWords = len(trainMatrix[0])
	    pAbusive = sum(array(trainCategory).astype(float))/float(numTrainDocs)
	    p0Num = ones(numWords); p1Num = ones(numWords)
	    p0Denom = 2.0; p1Denom = 2.0
	    for i in range(numTrainDocs):
	        if trainClasses[i] == '1':
	            p1Num += trainMat[i]
	            p1Denom += sum(trainMat[i])
	        else:
	            p0Num += trainMat[i]
	            p0Denom += sum(trainMat[i])
	    p1Vect = log(p1Num/p1Denom)
	    p0Vect = log(p0Num/p0Denom)
	    return p0Vect,p1Vect,pAbusive

	def textParse(bigString):
	    listOfTokens = re.split(r'\W*', bigString)
	    return [tok.lower() for tok in listOfTokens]

	def createVocabList(dataSet):
	    vocabSet = set([])
	    for document in dataSet:
	        vocabSet = vocabSet | set(document)
	    return list(vocabSet)

	def calcMostFreq(vocabList,fullText):
	    import operator
	    freqDict = {}
	    for token in vocabList:
	        freqDict[token]=fullText.count(token)
	    sortedFreq = sorted(freqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
	    return sortedFreq[:30]

	def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
	    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
	    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
	    if p1 > p0:
	        return 1
	    else:
	        return 0


	for line in sys.stdin:
	    wordList = textParse(line)[1:-1]
	    docList.append(wordList)
	    fullText.extend(wordList)

	vocabList = createVocabList(docList)

	classList = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
	             0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

	top30Words = calcMostFreq(vocabList,fullText)

	for pairW in top30Words:
	   if pairW[0] in vocabList:
	      vocabList.remove(pairW[0])

	trainingSet = range(2*25)

	testSet=[]

	for i in range(10):
	   randIndex = int(random.uniform(0,len(trainingSet)))
	   testSet.append(trainingSet[randIndex])
	   del(trainingSet[randIndex])

	trainMat=[]

	trainClasses = []

	for docIndex in trainingSet:
	   trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
	   trainClasses.append(classList[docIndex])
	p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
	errorCount = 0


	for docIndex in testSet:
	   wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
	   if classifyNB(array(wordVector),p0V,p1V,pSpam) != float(classList[docIndex]):
	      errorCount += 1
	print 'the error rate is: ',float(errorCount)/len(testSet)



## 结论

本案例利用朴素贝叶斯模型对文本进行分类，并利用hadoop实现了朴素贝叶斯模型的分布式计算，通过
mapper将得到的文本清洗并分布到不同节点进行计算，通过reducer将整理后的整齐数据建模，得到最
终的分类结果。这个模型可以扩展到其它文本分类中，也可以扩展为多分类的模型。

总体而言，利用hadoop做MapReduce，需要注意以下几点：

- map脚本的标准输入与标准输出；

- reduce脚本的标准输入。

- 路径问题。在hadoop中指明路径非常重要。首先要明确hadoop的安装路径，如果在安装路径下执行命
令，则直接执行bin/hadoop命令即可，否则需要在前面添加绝对路经以指明路径。其次，要找到
streaming所在路径，并指明。第三，指明mapper和reducer的脚本存放路径，这两个脚本的存放路径为
本地。第四，指明输入文件input的存放路径，这个文件需要放在服务器的文件夹中。


- 查看执行结果。执行结果均被保存在名为part-00000的文件中，并存放于-output所指定的路径下。


（感谢中国人民大学赵哲汇提供素材和案例。）
