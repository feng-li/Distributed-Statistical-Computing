#! /usr/bin/sh

TASKNAME=stocks_mean

hadoop fs -rm -r ./output/
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
    -jobconf mapred.job.name=$TASKNAME \
    -input /user/lifeng/data/stocks.txt \
    -output ./output  \
    -file "stock_day_avg.R"  \
    -mapper "/usr/bin/cat" \
    -reducer "Rscript stock_day_avg.R" \
    -numReduceTasks 1

hadoop fs -cat ./output/*
