# 实例分析：基于判别分析的气象因素对雾霾的影响


## 准备知识

* 判别分析
* R
* Hadoop Streaming

## 研究背景

众所周知，雾霾指数（AQI）由二氧化硫、二氧化氮、PM10、PM2.5、一氧化碳和臭氧这六项污染物计算
所得，然而我们生活中经常熟知的气象因素，比如平均气温、平均水汽压、平均相对湿度、平均风速和
日照时数，是否会对雾霾有影响呢？那么简单的基于这些因素通过距离判别法对是否雾霾进行分析预测
是否可行呢？本文会通过Hadoop对此进行简单探究。


## 研究思路

本案例基于北京市2013年10月到2015年6月的日气象数据对是否雾霾进行判别分析。数据的自变量来自
于中国气象数据网的中国地面国际交换站气候资料日值数据集（站点为北京站），主要有平均气温、平
均水汽压、平均相对湿度、平均风速和日照时数。数据的因变量是根据AQI指数得出的是否雾霾指标
rank(0、1变量)。研究思路是，将所有的样本分成训练样本集（所有样本去掉最后三十天样本）和测试
样本集（最后三十天样本），对训练样本集进行Hadoop下的判别分析建模，最后用测试样本集对模型进
行测试，计算错判率，分析结果。


## 建立判别分析模型

距离判别的重点是求得每个类别中各个变量的均值作为类中心，然后基于每个类别中各个变量的均值和
方差求得观测数据点到各类别中心得马氏距离，根据距离的远近进行判别。对于训练样本集中每类的各
个变量的均值和方差的计算我们用mapper和reducer进行分布式计算。下面我们以0类的第一个变量
trainx10为例进行展示。


首先用R将trainx10数据提出保存为trainx10.txt。然后我们用mapper和reducer计算均值。

    trainx10<-matrix((subset(pdata[,1],pdata[,6]==0)))
    write.table(trainx10,file="d:/trainx10.txt",sep=",",row.names=F,col.names=F)


Mapper是每一块中所有数据的均值，reducer为由mapper传递到reducer中所有数据的均值。经检验与数
据真实的均值一致。


最后我们根据上一步中得到的均值，再写一个mapper和reducer,这次mapper为每一块中每个数据与均值
的差的平方的和，reducer为由mapper传递到reducer中所有数据的和除以n-1。最后所得值就是方差，
经验证与数据真实的方差一致。


0类的其他变量的均值方差与x10类似，1类的所有变量的均值方差与0类的计算类似。最后分别计算测试
样本数据与0类和1类的马氏距离，离哪类比较近就判为哪一类，可以得到测试样本的预测判别变量
prerank。



### Mapper函数

计算0类中的x1（airtemperature）变量均值的mapper如下所示，它是每一块中所有数据的均值。计算0类中的x1（airtemperature）变量方差的mapper函数与之类似。


```
#! /usr/bin/env Rscript
options(warn=-1)
sink("/dev/null")
input<-file("stdin","r")
while(length(currentLine<-readLines(input, n=1, warn=FALSE)) > 0)	{
    fields<-unlist(strsplit(currentLine, ","))
    data<-sum(as.numeric(fields))
    sink()
    cat(data,"\n", sep="\t")
    sink("/dev/null")
    }
close(input)
```


### Reducer函数

计算0类中的x1（airtemperature）变量均值的reducer如下所示，它为由mapper传递到reducer中所有数据的均值。计算0类中的x1（airtemperature）变量方差的reducer与之类似。

```
#! /usr/bin/env Rscript
options(warn=-1)
sink("/dev/null")
input<-file("stdin","r")
data<-0
while(length(currentLine<-readLines(input, n=1, warn=FALSE)) > 0)	{
    fields<-unlist(strsplit(currentLine, "\t"))
    data<-data+as.numeric(fields)
}

x10bar<-data/305
sink()
cat(x10bar,"\n",sep="\t")
sink("/dev/null")

close(input)
```


## 结论


由本文的研究可知平均气温、平均水汽压、平均相对湿度、平均风速和日照时数对雾霾有影响。简单的
基于这些因素通过距离判别法对是否雾霾进行分析预测的错判率为0.3，可以用此方法进行预测。
