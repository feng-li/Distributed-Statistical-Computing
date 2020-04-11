
1 试验流程:
  首先在/user/lifeng/下建立了lifenghive数据库，并在该数
  据库中利用stocks.csv数据建立了stocks表，并创建了3个查询hql语句利用hive进行相
  关查询，查询结果被保存文件夹中。

2 hive分布式查询文档
  creatdb.hql：
  利用hql文档在/user/lifeng/下建立了lifenghive数据库。

  creattb.hql：
  在lifenghive该数据库中利用stocks.csv数据建立了stocks表。

  select：
  利用所建立的lifenghive数据库进行三个查询，如下解释：
  select1:查询苹果公司在各个交易所的平均收，开盘价格，平均最高，低价格。
  select2:查看每个公司在纳斯达克交易所的平均收盘，开盘价格和成交总量。
  select3：查询每个公司在开盘价和收盘价都高于2.6美元的时间中的，平均收盘，开盘
          价格，和交易总量，并按交易总量进行排序。
 
  result:
  result1，result2，result3中分别对应存放着以上select1,2,3查询的结果。

3 分布式查询计算结果
  最终输出的结果在result1，result2，result3  路径下
