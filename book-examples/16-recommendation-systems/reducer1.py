#! /usr/bin/python3
#reduce1: aggregate all the films and scores by the same user
import sys
from collections import defaultdict

#reduce process
dict=defaultdict(list)
#use defaultdict for key-value storage
while True:
    try:
        line=sys.stdin.readline()
        if not line:
            break
        user_id, item_id, rating = line.split('|')
        dict[user_id].append((item_id,float(rating)))
    except:
        continue
sys.stdin.close()
#reducer output: user_id:(film_id,rating)

 #save to local file in local model
 #use different separator for line split in next stage
 with open('ratings1.csv','w') as f:
     for k in dict.keys():
         for j in dict[k]:


f.write(str(j[0])+'*'+str(j[1])+'|')
f.write('\n')

 #standard output to HDFS
 #use different separator for line split in next stage
for k in dict.keys():
    for j in dict[k]:
        print(str(j[0])+'*'+str(j[1])+'|',end="")
    print('\n')
