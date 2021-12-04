#! /bin/env pythton3.7

import pyspark
spark = pyspark.sql.SparkSession.builder.appName("My Spark App").getOrCreate()
sc = spark.sparkContext

# from pyspark import SparkConf
# from pyspark import SparkContext

# conf = SparkConf().setMaster('yarn-client').conf.setAppName('spark-yarn')
# sc = SparkContext(conf=conf)
airFile = sc.textFile("/user/lifeng/asm-LICENSE")
# airFile = sc.textFile("/data/airdelay_small.csv")
airLengths = airFile.map(lambda s: len(s)).reduce(lambda a, b: a + b)
print (airLengths)
