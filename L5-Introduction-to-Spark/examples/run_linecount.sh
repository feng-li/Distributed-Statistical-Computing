#! /bin/sh

PYSPARK_PYTHON=python3.7 spark-submit \
	      --master yarn \
	      linecount.py

exit 0;
