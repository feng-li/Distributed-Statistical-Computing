#! /usr/bin/env python3

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import findspark
findspark.init("/usr/lib/spark-current")

import pyspark
spark = pyspark.sql.SparkSession.builder.appName(
    "Spark Native Logistic Regression App").getOrCreate()
spark.sparkContext.setLogLevel("WARN") # "DEBUG", "ERROR"

from pyspark.ml.classification import LogisticRegression
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler

from dlsa.models import simulate_logistic

import numpy as np
import pandas as pd
import time
import sys

tic0 = time.perf_counter()
##----------------------------------------------------------------------------------------
## Logistic Regression with SGD
##----------------------------------------------------------------------------------------
sample_size = 5000
p = 50
partition_method = "systematic"
partition_num = 20

data_pdf = simulate_logistic(sample_size, p, partition_method, partition_num)
data_sdf = spark.createDataFrame(data_pdf)

memsize = sys.getsizeof(data_pdf)

assembler = VectorAssembler(inputCols=["x" + str(x) for x in range(p)],
                            outputCol="features")

tic = time.perf_counter()
parsedData = assembler.transform(data_sdf)
time_parallelize = time.perf_counter() - tic

tic = time.perf_counter()
# Model configuration
lr = LogisticRegression(maxIter=100, regParam=0.3, elasticNetParam=0.8)

# Fit the model
lrModel = lr.fit(parsedData)
time_clusterrun = time.perf_counter() - tic

# Model fitted
print(lrModel.intercept)
print(lrModel.coefficients)

time_wallclock = time.perf_counter() - tic0

out = [
    sample_size, p, memsize, time_parallelize, time_clusterrun, time_wallclock
]
print(", ".join(format(x, "10.4f") for x in out))
