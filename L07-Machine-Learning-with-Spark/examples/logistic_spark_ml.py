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

# from dlsa.models import simulate_logistic

import numpy as np
import pandas as pd
import time
import sys


def simulate_logistic(sample_size, p, partition_method, partition_num):
    '''Simulate data based on logistic model

    '''
    ## Simulate Data
    n = sample_size
    p1 = int(p * 0.4)

    # partition_method = "systematic"
    # partition_num = 200

    ## TRUE beta
    beta = np.zeros(p).reshape(p, 1)
    beta[:p1] = 1

    ## Simulate features
    features = np.random.rand(n, p) - 0.5
    prob = 1 / (1 + np.exp(-features.dot(beta)))

    ## Simulate label
    label = np.zeros(n).reshape(n, 1)
    partition_id = np.zeros(n).reshape(n, 1)
    for i in range(n):
        # TODO: REMOVE loop
        label[i] = np.random.binomial(n=1,p=prob[i], size=1)

        if partition_method == "systematic":
            partition_id[i] = i % partition_num
        else:
            raise Exception("No such partition method implemented!")

        data_np = np.concatenate((partition_id, label, features), 1)
        data_pdf = pd.DataFrame(data_np, columns=["partition_id"] + ["label"] + ["x" + str(x) for x in range(p)])

    return data_pdf


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
