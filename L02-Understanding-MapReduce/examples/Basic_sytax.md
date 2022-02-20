## https://hadoop.apache.org/docs/current/hadoop-streaming/HadoopStreaming.html

hadoop jar /opt/apps/ecm/service/hadoop/2.7.2-1.3.1/package/hadoop-2.7.2-1.3.1/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar -input /user/lifeng/license.txt  -output /user/lifeng/output -mapper "/usr/bin/cat" -reducer "/usr/bin/wc" 

