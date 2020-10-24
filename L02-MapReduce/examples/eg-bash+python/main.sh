#! /bin/bash

PWD=$(cd $(dirname $0); pwd)
cd $PWD 1> /dev/null 2>&1

TASKNAME=hadoop_task_fli

# hadoop client
HADOOP_INPUT_DIR=/fli/data/part-*
HADOOP_OUTPUT_DIR=/fli/results/task
HADOOP_VERSION=3.1.3

echo $HADOOP_HOME
echo $HADOOP_INPUT_DIR
echo $HADOOP_OUTPUT_DIR

hadoop fs -rm -r $HADOOP_OUTPUT_DIR

hadoop jar  ${HADOOP_HOME}/share/hadoop/tools/lib/hadoop-streaming-${HADOOP_VERSION}.jar \
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
    -reducer "python3 reducer.py" \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner

hadoop fs -cat ${HADOOP_OUTPUT_DIR}/*

exit 0;
