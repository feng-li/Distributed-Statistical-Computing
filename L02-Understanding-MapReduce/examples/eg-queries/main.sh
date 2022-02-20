#!/bin/bash

PWD=$(cd $(dirname $0); pwd)
cd $PWD 1> /dev/null 2>&1

TASKNAME=task4_fli
# python location on hadoop
PY27='/fli/tools/python2.7.tar.gz'
# hadoop client
HADOOP_HOME=/home/users/fli/hadoop/bin/hadoop
HADOOP_INPUT_DIR1=/fli/data/part-*
HADOOP_OUTPUT_DIR=/fli/results/task2

echo $HADOOP_HOME
echo $HADOOP_INPUT_DIR
echo $HADOOP_OUTPUT_DIR

$HADOOP_HOME fs -rmr $HADOOP_OUTPUT_DIR

$HADOOP_HOME streaming \
    -jobconf mapred.job.name=$TASKNAME \
    -jobconf mapred.job.priority=NORMAL \
    -jobconf mapred.map.tasks=500 \
    -jobconf mapred.reduce.tasks=10 \
    -jobconf mapred.job.map.capacity=500 \
    -jobconf mapred.job.reduce.capacity=500 \
    -jobconf stream.num.map.output.key.fields=1 \
    -jobconf num.key.fields.for.partition=1 \
    -jobconf stream.memory.limit=1000 \
    -file $PWD/mapper.py  $PWD/reducer.py $PWD/queries92w \
    -output ${HADOOP_OUTPUT_DIR} \
    -input ${HADOOP_INPUT_DIR1}  \
    -mapper "python mapper.py" \
    -reducer "python reducer.py" \
    -cacheArchive ${PY27}#py27

if [ $? -ne 0 ]; then
    echo 'error'
    exit 1
fi
$HADOOP_HOME fs -touchz ${HADOOP_OUTPUT_DIR}/done

exit 0


