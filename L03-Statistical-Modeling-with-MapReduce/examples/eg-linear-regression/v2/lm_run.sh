#!/bin/bash

PWD=$(cd $(dirname $0); pwd)
cd $PWD 1> /dev/null 2>&1

# hadoop client
STREAMING_DIR=/usr/lib/hadoop-current/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar 
HADOOP_INPUT_DIR=/user/student/linear_random.csv
HADOOP_OUTPUT_DIR=/user/student/output

echo $PWD
echo $HADOOP_INPUT_DIR
echo $HADOOP_OUTPUT_DIR

hadoop fs -rmr $HADOOP_OUTPUT_DIR

hadoop jar $STREAMING_DIR \
    -jobconf mapred.map.tasks=4 \
    -jobconf mapred.reduce.tasks=1 \
    -file  $PWD/lm_mapper.py $PWD/lm_reducer.py \
    -output ${HADOOP_OUTPUT_DIR} \
    -input ${HADOOP_INPUT_DIR} \
    -mapper "lm_mapper.py" \
    -reducer "lm_reducer.py" \

