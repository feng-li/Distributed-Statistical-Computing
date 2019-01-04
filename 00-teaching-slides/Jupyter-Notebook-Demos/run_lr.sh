hadoop fs -rm -r ./output

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
       -input /user/lifeng/data/linear_random.csv \
       -output ./output \
       -file "lr_mapper.py" "lr_reducer.py" \
       -mapper "python lr_mapper.py " \
       -reducer "python lr_reducer.py" \
       -numReduceTasks 1 \

hadoop fs -cat ./output/*
