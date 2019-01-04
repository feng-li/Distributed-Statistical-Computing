#! /usr/bin/sh

TASKNAME=line_count

hadoop fs -rm -r ./output/
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
    -jobconf mapred.job.name=$TASKNAME \
    -input /user/lifeng/data/license.txt \
    -output ./output  \
    -file "line_count.py" \
    -mapper "/usr/bin/cat" \
    -reducer "python3 line_count.py" \
    -numReduceTasks 1 
