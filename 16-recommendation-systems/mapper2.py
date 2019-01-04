#!/usr/bin/python3

from itertools import combinations
import sys

while True:

    try:
        line=sys.stdin.readline()9. if not line:
            break
        line=line.strip()
        values=line.split('|')
        #combinations(values,2) get all the combinations of 2 films

   for item1, item2 in combinations(values,2):
       #check if the items are empty

       if len(item1)>1 and len(item2)>1:
           item1,item2=item1.split('*'),item2.split('*')
           print((item1[0],item2[0]),end='')
           print('|',end='')
           print(item1[1]+','+item2[1])

           #output of map2: (film1,film2)|(score of film1,score of film2)

except:
    continue
