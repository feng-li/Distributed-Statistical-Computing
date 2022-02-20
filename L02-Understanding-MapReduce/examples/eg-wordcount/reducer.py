#! /usr/bin/env python3

import sys

line_count = 0
word_count = 0

for line in sys.stdin:
    word= line.split(' ')
    line_count += 1
    word_count += len(word)

print ('%s\t%s'% (line_count, word_count))
