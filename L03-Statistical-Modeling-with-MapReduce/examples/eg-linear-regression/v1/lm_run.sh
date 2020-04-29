#! /bin/sh

#cd /home/lifeng/lectures/L3-Statistical-Modeling-with-MapReduce/examples/eg-linear-regression

chmod +x lm_reducer.py
chmod +x lm_mapper.py

#python lm_mapper.py < ranMat.csv | python lm_reducer.py

hadoop fs -rm /user/lifeng/lab3out

#hadoop fs -copyFromLocal ranMat.csv /user/lifeng/

hadoop jar /usr/lib/hadoop-current/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
        -input /user/lifeng/ranMat.csv \
        -output /user/lifeng/lab3out  \
        -file lm_mapper.py   \
        -mapper "lm_mapper.py" \
        -file lm_reducer.py  \
        -reducer "lm_reducer.py" \ 
        -numReduceTasks 1 \

hadoop fs -cat /user/lifeng/lab3out/part-*

#hadoop fs -copyToLocal /user/lifeng/lab3out .
#Rscript ./lm_confirm.R

