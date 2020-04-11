#! /usr/bin/env python3
# line_count.py
import sys
count = 0
data = []
for line in sys.stdin:
    count += 1
    data.append(line)    
print(count) # print goes to sys.stdout
# print(data)
