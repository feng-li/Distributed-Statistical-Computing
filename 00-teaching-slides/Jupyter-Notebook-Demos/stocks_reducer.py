#! /usr/bin/env python3

import sys
from operator import itemgetter 
wordcount = {}

for line in sys.stdin:
    word,count = line.split(' ')
    count = int(count)
    wordcount[word] = wordcount.get(word,0) + count

sorted_wordcount = sorted(wordcount.items(), key=itemgetter(0))

for word, count in sorted_wordcount:
    print ('%s\t%s'% (word,count))
