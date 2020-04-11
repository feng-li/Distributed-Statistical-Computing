#! /usr/bin/env python
import re
import feedparser
import random
import sys
from numpy import *



docList=[]
fullText =[]


def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec

def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(array(trainCategory).astype(float))/float(numTrainDocs)
    p0Num = ones(numWords); p1Num = ones(numWords)     
    p0Denom = 2.0; p1Denom = 2.0                        
    for i in range(numTrainDocs):
        if trainClasses[i] == '1':
            p1Num += trainMat[i]
            p1Denom += sum(trainMat[i])
        else:
            p0Num += trainMat[i]
            p0Denom += sum(trainMat[i])
    p1Vect = log(p1Num/p1Denom)        
    p0Vect = log(p0Num/p0Denom)          
    return p0Vect,p1Vect,pAbusive

def textParse(bigString):
    listOfTokens = re.split(r'\W*', bigString)
    return [tok.lower() for tok in listOfTokens]

def createVocabList(dataSet):
    vocabSet = set([])  
    for document in dataSet:
        vocabSet = vocabSet | set(document) 
    return list(vocabSet)

def calcMostFreq(vocabList,fullText):
    import operator
    freqDict = {}
    for token in vocabList:
        freqDict[token]=fullText.count(token)
    sortedFreq = sorted(freqDict.iteritems(), key=operator.itemgetter(1), reverse=True) 
    return sortedFreq[:30]

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)    
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else: 
        return 0

    
for line in sys.stdin:
    wordList = textParse(line)[1:-1]
    docList.append(wordList)
    fullText.extend(wordList)
    
vocabList = createVocabList(docList)

classList = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
             0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

top30Words = calcMostFreq(vocabList,fullText)

for pairW in top30Words:
   if pairW[0] in vocabList:
      vocabList.remove(pairW[0])
      
trainingSet = range(2*25)

testSet=[]

for i in range(10):
   randIndex = int(random.uniform(0,len(trainingSet)))
   testSet.append(trainingSet[randIndex])
   del(trainingSet[randIndex])
   
trainMat=[]

trainClasses = []

for docIndex in trainingSet:
   trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
   trainClasses.append(classList[docIndex])
p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
errorCount = 0

 
for docIndex in testSet:        
   wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
   if classifyNB(array(wordVector),p0V,p1V,pSpam) != float(classList[docIndex]):
      errorCount += 1
print 'the error rate is: ',float(errorCount)/len(testSet)
