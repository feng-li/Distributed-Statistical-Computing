#!/usr/bin/python

import sys
import re


def textParse(bigString):
    listOfTokens = re.split(r'\W*', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]

for line in sys.stdin:
    wordList = textParse(line)
    print(str(wordList).strip('[]')
