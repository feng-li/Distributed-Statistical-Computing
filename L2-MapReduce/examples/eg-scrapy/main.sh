#!/bin/bash

PWD=$(cd $(dirname $0); pwd)
cd $PWD 1> /dev/null 2>&1

TASKNAME=task2_fli
# python location on hadoop
PY27='/fli/tools/python2.7.tar.gz'
# hadoop client
HADOOP_HOME=/home/users/fli/hadoop/bin/hadoop
HADOOP_INPUT_DIR1=/fli/data1/part-*
HADOOP_INPUT_DIR2=/fli/data2/part-*
HADOOP_OUTPUT_DIR=/fli/results/task2

echo $HADOOP_HOME
echo $HADOOP_INPUT_DIR
echo $HADOOP_OUTPUT_DIR

$HADOOP_HOME fs -rmr $HADOOP_OUTPUT_DIR

$HADOOP_HOME streaming \
    -jobconf mapred.job.name=$TASKNAME \
    -jobconf mapred.job.priority=HIGH \
    -jobconf mapred.map.tasks=500 \
    -jobconf mapred.reduce.tasks=500 \
    -jobconf mapred.job.map.capacity=500 \
    -jobconf mapred.job.reduce.capacity=500 \
    -jobconf stream.num.map.output.key.fields=3 \
    -jobconf num.key.fields.for.partition=1 \
    -jobconf stream.memory.limit=1000 \
    -file $PWD/mapper.py $PWD/reducer.py $PWD/gtburl.py $PWD/argparse.py \
    -output ${HADOOP_OUTPUT_DIR} \
    -input ${HADOOP_INPUT_DIR1} \
    -input ${HADOOP_INPUT_DIR2} \
    -mapper "python mapper.py" \
    -reducer "python reducer.py" \
    -cacheArchive ${PY27}#py27

if [ $? -ne 0 ]; then
    echo 'error'
    exit 1
fi
$HADOOP_HOME fs -touchz ${HADOOP_OUTPUT_DIR}/done

exit 0


