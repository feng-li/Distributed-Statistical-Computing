# 实例分析：基于 MapReduce 的电影推荐系统


## 准备知识

* 推荐系统
* Python
* Mapreduce

推荐系统在互联网领域有着广泛的运用,本案例实现了对大量电影评论数据的整合处理,并根据电影间的
相关程度,根据用户观影历史向用户推荐相关度较高的电影。


## 数据准备

本文所用数据来自 [GroupLens 网站](http://grouplens.org/datasets/movielens/),包含 1000 名用
户对 1700 部电影的 100000 条 评论(1998 年),为方便处理首先对数据进行了简单预处理。10 万条数
据中,每条数据由用户编号、电影名称、评分组成。


## 建立模型

针对数据特点,电 影的推荐系统设计如下:

* 对每一对电影 A 和 B,对所有评论过这两部电影的用户及评分数据进行聚集;

* 使用评分数据计算电影 A 与 B 的相关系数;

* 对所有看过某电影的用户,我们可以向其推荐与其相关系数最高的几部电影。



该推荐系统的简要 MapReduce 步骤如下。



## 把评分数据按用户进行聚集


原始数据(user|movie|rating)可视为 Key 为用户 ID,Value 为电影名和评分的 Key-Value 对,因此
Map 阶段不需要过多操作,可以直接使用 cat 函数作为 Mapper, 将 Key-Value 对传递给 Reducer。而
Reducer 则根据用户 ID,将同一用户评分过的所 有电影名和评分进行汇集。最后将同一用户的所有评
分数据储存在同一行,输出数据 共 1000 行。此处通过分行将不同用户的评分区分开来,因此用户 ID
可以在后续分析 中舍弃。

Mapper: cat 函数

Reducer:


    #! /usr/bin/python3

    import sys
    from collections import defaultdict

    #reduce process
    dict=defaultdict(list)
    while True:
        try:
            line=sys.stdin.readline()
            if not line:
                break
            user_id, item_id, rating = line.split('|')
            dict[user_id].append((item_id,float(rating)))
        except:
            continue
    sys.stdin.close()

    with open('ratings1.csv','w') as f:
         for k in dict.keys():
             for j in dict[k]:


    f.write(str(j[0])+'*'+str(j[1])+'|')
    f.write('\n')

     #standard output to HDFS
     #use different separator for line split in next stage
    for k in dict.keys():
        for j in dict[k]:
            print(str(j[0])+'*'+str(j[1])+'|',end="")
        print('\n')

其中reduce 代码中,使用了 defaultdict 类型对 Key-Value 型数据进行储存。相对于普通的字典型数
据,defaultdict 可以自动设定默认值,可以方便地储存本文的数据类 型。在读入数据时,使用了 try
函数防止错误格式的数据输入,当某一行数据格式有误时,自动从下一行继续读入。为了方便第二阶段
MapReduce 对数据进行分隔,此处 reduce 的输出使用了*和|作为分隔符。

模拟 Hadoop 模式调试:

    cat ratings.csv | sort -t $'|' -k 1,1 | ./reduce1.pyHadoop

集群运行:

    hadoop jar /home/dmc/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar \
       -D stream.map.output.field.separator=\| \
       -file /home/ruc15/chen_sicong/MR/reduce1.py \
       -input chen_sicong/ratings.csv \
       -output chen_sicong/output \
       -mapper "/bin/cat" \
       -reducer "reduce1.py"

Hadoop 集群模式下运行时,需要事先把数据文件上传至 HDFS,由于 mapper 的
输 出不是默认的逗号分隔,需要使用-D 指令进行设置。使用-file 指令将 Reducer 代码 分发到各个
节点,以解决“找不到执行程序”的错误。


## 计算每两部电影之间的皮尔逊相关系数:

第二阶段的输入数据为第一阶段的输出数据,每一行是同一用户所有评论过的电影名和评分。在 Map 阶
段,首先将同一用户对各个电影的评分拆分开来,取其中所有的两两组合进行输出。这样,Mapper 输出的
数据为每个用户同时看过的电影两两组合及其评分。即 Key:(电影 1,电影 2),Value:(电影 1 评分,电
影 2 评分)。

Reduce 阶段根据 Key:(电影 1,电影 2)进行汇总,得到所有同时看过电影 1 和电影 2 的用户的评分。
然后,根据这些评分计算电影 1 和电影 2 的皮尔逊相关系数


Reducer 的输出为每两部电影之间的皮尔逊相关系数及评分人数,评分人数可以视为相关系数的可信度,
当评分人数过少时,相关系数未必可信。最后,根据相关系数可以对用户进行简单的电影推荐:当一个用
户看过某电影时,可以向其推荐与其相关程度较高的若干其他电影。


    #!/usr/bin/python3

    from itertools import combinations
    import sys

    while True:

        try:
            line=sys.stdin.readline()9. if not line:
                break
            line=line.strip()
            values=line.split('|')
            #combinations(values,2) get all the combinations of 2 films

       for item1, item2 in combinations(values,2):
           #check if the items are empty

           if len(item1)>1 and len(item2)>1:
               item1,item2=item1.split('*'),item2.split('*')
               print((item1[0],item2[0]),end='')
               print('|',end='')
               print(item1[1]+','+item2[1])

               #output of map2: (film1,film2)|(score of film1,score of film2)

    except:
        continue


Hadoop 集群运行:

    hadoop jar /home/dmc/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar \
    -D stream.map.output.field.separator=\| \
    -file /home/ruc15/chen_sicong/MR/map2.py \
    -file /home/ruc15/chen_sicong/MR/reduce2.py \
    -input chen_sicong/ratings1.csv \
    -output chen_sicong/output \
    -mapper "map2.py" \
    -reducer "reduce2.py"


根据两次 mapreduce 计算,我们得出了任意两部电影之间的相关系数。这样,当某 一用户看过电影 A
时,我们可以对其推荐相关程度最大的几部电影。一个简单的电影 推荐系统得以实现。在使用时应该将
相关系数与评价人数结合起来进行考虑,如果评 价人数过少,即使相关系数较高,结果也未必可信。本案
例实现的基于内容过滤的推荐系统简单快速,但不能为用户发现新的感兴趣的商品,只能发现和用户已有
兴趣相似的商品。在后续的改进中,可以建立更准确有效的推荐系统。

（感谢中国人民大学陈思聪提供素材和案例。）
