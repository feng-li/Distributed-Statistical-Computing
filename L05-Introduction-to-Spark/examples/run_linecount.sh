#! /bin/sh

PYSPARK_PYTHON=python3 spark-submit \
	      --master yarn \
              --conf spark.ui.enabled=false \
	      linecount.py

exit 0;
