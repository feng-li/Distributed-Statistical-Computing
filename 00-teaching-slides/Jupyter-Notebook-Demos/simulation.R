#! /usr/bin/Rscript

n = 100000
p = 10
x = matrix(rnorm(n*p), n, p)
e = rnorm(n)
beta = c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10) #生成beta系数分别为1~10
y = x%*%beta+0.3*e
mydata = cbind(x, y)
dim(mydata)
write.table(mydata, "linear_random.csv", sep = "," , row.names = FALSE,  col.names = FALSE)
colnames(mydata) = c("x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", "x10", "y")
mydata = data.frame(mydata)
myfit  =  lm(y~x1+x2+x3+x4+x5+x6+x7+x8+x9+x10, mydata)
myfit$coefficients
