#! /usr/bin/env Rscript

input <- file("stdin","r")
A<-c()
B<-c()
while(length(currentLine<-readLines(input,n=1,warn=FALSE))>0)
{
    fields=unlist(strsplit(currentLine," "))
    a=as.double(fields[2])
    b=as.double(fields[3])
    A=c(A,a)
    B=c(B,b)
}

mydata=data.frame(A,B)
mydata=na.omit(mydata)
data=as.matrix(mydata)

library(e1071)
results=cmeans(data,centers=4,iter.max=20,verbose=TRUE,method="cmeans",m=2)
print(results)

close(input)
