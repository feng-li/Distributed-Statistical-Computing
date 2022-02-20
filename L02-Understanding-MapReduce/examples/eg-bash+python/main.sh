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
       -D mapred.job.name=TASKNAME \
       -D mapred.job.priority=NORMAL \
       -D stream.memory.limit=1000 \
       -D mapred.map.tasks=10 \
       -D mapred.reduce.tasks=7 \
       -D mapred.job.map.capacity=100 \
       -D mapred.job.map.capacity=100 \
       -input ${HADOOP_INPUT_DIR} \
       -output ${HADOOP_OUTPUT_DIR} \
       -mapper "$PWD/mapper.sh" \
       -file "$PWD/mapper.sh"
# -cacheArchive ${PY27}#py27 \
# -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner

# following are others generic command, if use ,please put them above streaming Options
# -D mapred.compress.map.output=True # if output of map is compressed
# -D mapred.map.output.comression.codec=org.apache.hadoop.io.compress.GzipCodec # compress mode
# -D mapred.output.compress=True # if output of reduce is compressed
# -D mapred.output.compression.codec=org.apache.hadoop.io.compress.GzipCodec # compress mode
# -D stream.map.output.field.separator=. # default \t
# -D stream.num.map.output.key.fields=4 # default the part before the first \t serves as the key
# -D stream.reduce.output.field.separator=.
# -D stream.num.reduce.output.key.fields=4
# -D map.output.key.field.separator=. # Sets the delimiter inside the Key in the Map output
# -D mapreduce.partition.keypartitioner.options=-k1,2 # equal -D num.key.fields.for.partition=2

hadoop fs -cat ${HADOOP_OUTPUT_DIR}/*

exit 0;
