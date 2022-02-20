#!/bin/bash

# Current code directory
PWD=$(cd $(dirname $0); pwd)
cd $PWD 1> /dev/null 2>&1

# Asign a task name 
TASKNAME=task1_lifeng

# Upload your program if worker machine does not have them.
PY27='lifeng/tools/python2.7.tar.gz'

# Hadoop input and output
HADOOP_INPUT_DIR=/user/lifeng/data1/part-*
HADOOP_OUTPUT_DIR=/user/lifeng/results/task1

echo $HADOOP_INPUT_DIR
echo $HADOOP_OUTPUT_DIR

$HADOOP_HOME fs -rmr $HADOOP_OUTPUT_DIR

hadoop -jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
    -jobconf mapred.job.name=$TASKNAME \
    -jobconf mapred.job.priority=NORMAL \
    -jobconf mapred.map.tasks=500 \
    -jobconf mapred.reduce.tasks=500 \
    -jobconf mapred.job.map.capacity=500 \
    -jobconf mapred.job.reduce.capacity=500 \
    -jobconf stream.num.map.output.key.fields=2 \
    -jobconf mapred.text.key.partitioner.options=-k1,1 \
    -jobconf stream.memory.limit=1000 \
    -file $PWD/mapper.sh \
    -output ${HADOOP_OUTPUT_DIR} \
    -input ${HADOOP_INPUT_DIR} \
    -mapper "sh mapper.sh" \
    -reducer "cat" \
    -cacheArchive ${PY27}#py27 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner


if [ $? -ne 0 ]; then
    echo 'error'
    exit 1
fi
$HADOOP_HOME fs -touchz ${HADOOP_OUTPUT_DIR}/done

exit 0


