#! /usr/bin/python
import feedparser

sf=feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
ny=feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
f = open('try1.txt','w')
for i in range(len(sf['entries'])):
        wordList = ny['entries'][i]['summary']
        f.write(wordList.replace('\n','')  +'\n')
        wordList = sf['entries'][i]['summary']
        f.write(wordList.replace('\n','')  +'\n')
f.close()
