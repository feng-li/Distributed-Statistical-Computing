#! /usr/bin/env python

import re
import sys
from numpy import *
from pandas import *
import string

lines = sys.stdin.readlines()

dataMat = []
for i  in range(0,len(lines)):
       fields = lines[ i ].strip(' \n')
       curfields = re.findall(r"\d+\.?\d*", fields)
       fltfields = map(float, curfields)
       dataMat.append(fltfields)

dataMat = array(dataMat)

def distEclud(vecA, vecB):
       return sqrt(sum(power(vecA - vecB, 2)))


def randCent(dataSet, k):
      n = shape(dataSet)[1]
      centroids = mat(np.zeros((k,n)))
      for j  in range(n):
           minJ = min(dataSet[:, j])
           rangeJ = float(max(dataSet[:,j]) - minJ)
           centroids[:,j] = minJ + rangeJ * random.rand(k, 1)
      return centroids

def kMeans(dataSet, k, distMeas=distEclud,createCent=randCent):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2)))
    centroids = createCent(dataSet,k)
    clusterChanged = True
    while clusterChanged:
	  clusterChanged = False
          for i in range(m):
              minDist = inf; minIndex = -1
              for j in range(k):
                  distJI = distMeas(centroids[j,:],dataSet[i,:])
		  if distJI < minDist:
		     minDist = distJI; minIndex = j
	      if clusterAssment[i,0] != minIndex: clusterChanged = True
	      clusterAssment[i,:] = minIndex,minDist**2
          print centroids
          for cent in range(k):
	      ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]
              centroids[cent,:] = mean(ptsInClust,axis=0)
	  return centroids,clusterAssment

myCentroids, clusterAssing = kMeans(dataMat,4)
print(myCentroids,clusterAssing)
