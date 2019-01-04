#!/bin/bash

PWD=$(cd $(dirname $0); pwd)
cd $PWD 1> /dev/null 2>&1

TASKNAME=task3_fli
# python location on hadoop
PY27='/fli/tools/python2.7.tar.gz'
# hadoop client
HADOOP_HOME=/home/users/fli/hadoop/bin/hadoop
HADOOP_INPUT_DIR1=/fli/data/part-*
HADOOP_OUTPUT_DIR=/fli/results/task2

echo $HADOOP_HOME
echo $HADOOP_INPUT_DIR
echo $HADOOP_OUTPUT_DIR

$HADOOP_HOME/bin/hadoop fs -rmr $HADOOP_OUTPUT_DIR

$HADOOP_HOME/bin/hadoop streaming \
    -jobconf mapred.job.name=$TASKNAME \
    -jobconf mapred.job.priority=NORMAL \
    -jobconf mapred.map.tasks=100 \
    -jobconf mapred.reduce.tasks=10 \
    -jobconf mapred.job.map.capacity=100 \
    -jobconf mapred.job.reduce.capacity=100 \
    -jobconf stream.num.map.output.key.fields=1 \
    -jobconf mapred.text.key.partitioner.options=-k1,1 \
    -jobconf stream.memory.limit=1000 \
    -file $PWD/mapper.sh  $PWD/reducer.py $PWD/t \
    -output ${HADOOP_OUTPUT_DIR} \
    -input ${HADOOP_INPUT_DIR1} \
    -mapper "sh mapper.sh" \
    -reducer "python reducer.py" \
    -cacheArchive ${PY27}#py27 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner


if [ $? -ne 0 ]; then
    echo 'error'
    exit 1
fi
$HADOOP_HOME fs -touchz ${HADOOP_OUTPUT_DIR}/done

exit 0


