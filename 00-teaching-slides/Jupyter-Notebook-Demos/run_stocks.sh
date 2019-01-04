#! /usr/bin/sh

TASKNAME=stocks

hadoop fs -rm -r ./output/
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
    -jobconf mapred.job.name=$TASKNAME \
    -input /user/lifeng/data/stocks.txt \
    -output ./output  \
    -file "stocks_mapper.py" "stocks_reducer.py"  \
    -mapper "python3 stocks_mapper.py" \
    -reducer "python3 stocks_reducer.py" \
    -numReduceTasks 3

hadoop fs -cat ./output/*
