# 实例分析：通过Word Count了解Spark工作流程


## 准备知识

* Spark


## 基本步骤

编写Spark应用与Hadoop类似。将需要的代码写入一个惰性求值的driver program中，通过一个action，
driver program被分发到集群上，由各个RDD分区上的worker来执行。然后结果会被发送回driver
program进行聚合或编译。本质上，驱动程序创建一个或多个RDD，调用操作来转换RDD，然后调用动作
处理被转换后的RDD。


这些步骤大体如下：

* 定义一个或多个RDD，可以通过获取存储在磁盘上的数据（HDFS，HBase，Local Disk），并行化内存
  中的某些集合，转换（transform）一个已存在的RDD，或者，缓存或保存。

* 通过传递一个闭包（函数）给RDD上的每个元素来调用RDD上的操作。Spark提供了除了Map和Reduce的
  80多种高级操作。

* 使用结果RDD的动作（action）（如count、collect、save等）。动作将会启动集群上的计算。

* 当Spark在一个worker上运行闭包时，闭包中用到的所有变量都会被拷贝到节点上，但是由闭包的局
  部作用域来维护。Spark提供了两种类型的共享变量，这些变量可以按照限定的方式被所有worker访
  问。广播变量会被分发给所有worker，但是是只读的。累加器这种变量，worker可以使用关联操作来
  “加”，通常用作计数器。


下面我们来简略描述下Spark的执行。

本质上，Spark应用作为独立的进程运行，由驱动程序中的SparkContext协调。这个context将会连接到
一些集群管理者（如YARN），这些管理者分配系统资源。集群上的每个worker由执行者（executor）管
理，执行者反过来由SparkContext管理。执行者管理计算、存储，还有每台机器上的缓存。


重点要记住的是应用代码由驱动程序发送给执行者，执行者指定context和要运行的任务。执行者与驱
动程序通信进行数据分享或者交互。驱动程序是Spark作业的主要参与者，因此需要与集群处于相同的
网络。这与Hadoop代码不同，Hadoop中你可以在任意位置提交作业给JobTracker，JobTracker处理集群
上的执行。

## Word Count 演示


为了演示”word count”的功能，我们在计算机路径下存储了一部小说《福尔摩斯全集》。


首先，在命令行中输入以下命令：

    pyspark

PySpark将会自动使用本地Spark配置创建一个SparkContext。你可以通过sc变量来访问它。

下面我们来创建第一个RDD

    >>>text = sc.textFile("SherlockHolmes.txt")
    >>> print text



由于我们访问的是本地的数据文件，所以没有必要使用addFile函数。textFile方法将数据文件加载到
一个RDD命名文本。使用print命令查看RDD，可以发现这是一个MapPartitionsRDD。注意，文件路径是
相对于当前工作目录的一个相对路径，在上一段命令中我们没有输入文件的路径是因为我们是在数据文
件所在的目录下打开pyspark的。我们转换下这个RDD，来进行分布式计算的“hello world”：

    >>> from operator import add
    >>>def acf(text):
    	   return text.split()
    >>> words = text.flatMap(acf)
    >>> print words


我们首先引入了add这个函数，作为加法的闭包来使用。首先我们要做的是把文本拆分为单词。我们创
建了一个tokenize函数，参数是文本片段，返回根据空格拆分的单词列表。然后我们通过给flatMap操
作符传递tokenize闭包对textRDD进行变换创建了一个wordsRDD。words是个PythonRDD，但是执行本应
该立即进行。显然，我们还没有把整个数据集拆分为单词列表。


如果你曾使用MapReduce做过Hadoop版的“字数统计”，你应该知道下一步是将每个单词映射到一个键值
对，其中键是单词，值是1，然后使用reducer计算每个键的1总数。


首先，我们定义一个mapper

    >>>def chag(x):
        return (x,1)
    >>> wc = words.map(chag)
    >>> print wc.toDebugString()


这行代码将会把lambda映射到每个单词。因此，每个x都是一个单词，每个单词都会被匿名闭包转换为
元组(word, 1)。为了查看转换关系，我们使用toDebugString方法来查看RDD是怎么被转换的。


接下来可以使用reduceByKey动作进行字数统计，然后把统计结果写到磁盘。

    >>> counts = wc.reduceByKey(add)
    >>> counts.saveAsTextFile("wc_result")


一旦我们最终调用了saveAsTextFile动作，这个分布式作业就开始执行了，在作业“跨集群地”（或者你
本机的很多进程）运行时，你应该可以看到很多INFO语句。如果退出解释器，你可以看到当前工作目录
下有个“wc_result”目录。


每个part文件都代表你本机上的进程计算得到的被保持到磁盘上的最终RDD。如果对一个part文件进行
head命令，你可以看到字数统计元组。注意这些键没有像Hadoop一样被排序（因为Hadoop中Map和
Reduce任务中有个必要的打乱和排序阶段）。但是，能保证每个单词在所有文件中只出现一次，因为我
们使用了reduceByKey操作符。
