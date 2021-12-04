#! /usr/bin/env python3
import pyspark
from pyspark.mllib.linalg.distributed import RowMatrix
import numpy as np

conf = pyspark.SparkConf().setAppName("Compute the inverse of X'X with Spark RDD")  # “yarn”
sc = pyspark.SparkContext(conf=conf)

x = [[1, 20, 3], [40, 5, 6], [7, 8, 90], [10, 110, 12], [13, 14, 150]]
rows = sc.parallelize(x)
X = RowMatrix(rows)
XTX = X.computeGramianMatrix()
XTX_np = XTX.toArray()
XTX_inv = np.linalg.inv(XTX_np)
print(XTX_inv)
