#! /usr/bin/env Rscript
input = file("stdin", "r")
test = readLines(input, n=1, warn=F)
p = length((unlist(strsplit(test, ","))))
                                        # 求出数据中的变量个数 p
while(length(data <- readLines(input, n = 200, warn = F)) > 0)
                                        # 每 200 行数据为一个分块
{
    a = data.frame(matrix(as.numeric(unlist(strsplit(data, ","))), ncol = p, byrow = T))
    names(a) = c("NUM", "Y", "X1", "X2", "X3", "X4")
    glm = glm(Y~X1+X2+X3+X4, family = poisson(), data = a)
    coefficients = glm$coefficients # 回归系数
    pvalue = summary(glm)$coefficients[, 4] # p 值
    pred = predict(glm, a)
    lam = exp(pred)
    RME = abs(a$Y - lam) / (1+lam)
    mean = mean(RME)
                                        # 相对预测误差
    cat(coefficients, '\n')
    cat(pvalue, '\n')
    cat(mean, '\n')
}
close(input)
