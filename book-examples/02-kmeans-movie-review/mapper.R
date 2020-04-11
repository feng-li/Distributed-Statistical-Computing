#! /usr/bin/env Rscript

input <- file("stdin","r")

A<-c()
B<-c()

while(length(currentLine <- readLines(input,n=1,warn=FALSE))>0)
{
    fields <- unlist(strsplit(currentLine,","))
    a=as.double(fields[1])
    b=as.double(fields[2])
    A=c(A,a)
    B=c(B,b)
}
mydata <- data.frame(A,B)

scale01=function(x){
    ncol=dim(x)[2]
    nrow=dim(x)[1]
    new=matrix(0,nrow,ncol)
    for(i in 1:ncol)
    {max=max(x[,i])
        min=min(x[,i])
        for(j in 1:nrow)
        {new[j,i]=(x[j,i]-min)/(max-min)}
    }
    new
}

datanorm=scale01(mydata)
print(datanorm,stdout())
close(input)
