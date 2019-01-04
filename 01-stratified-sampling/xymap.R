#! /usr/bin/env Rscript
input <- file("stdin", "r")
library(sampling)
a <- runif(1000, 1, 10)
b <- rnorm(2000, 2.5, 5)
c <- rexp(1500, 1/2)
t <- c(c(a, b), c)
tmean <- mean(t)

## 简单随机抽样 ##
sitime <- srswor(450, 4500)
siindfun <- function(k){
      if(sitime[k] != 0){
              tmp <- rep(t[k], sitime[k])
      } else {tmp = 0}
}
siind <- unlist(lapply(1:length(sitime), FUN = siindfun))
sampsi <- siind[which(siind != 0)]
simean <- mean(sampsi)

## 分层随机抽样 ##
sitime <- srswor(100, 1000)
siindfun <- function(k){
    if(sitime[k] != 0){
        tmp <- rep(a[k], sitime[k])
    } else {tmp = 0}
}
siind <- unlist(lapply(1:length(sitime), FUN = siindfun))
sampsi <- siind[which(siind != 0)]
amean <-mean(sampsi)

sitime <- srswor(200, 2000)
siindfun <- function(k){
    if(sitime[k] != 0){
        tmp <- rep(b[k], sitime[k])
    } else {tmp = 0}
}
siind <- unlist(lapply(1:length(sitime), FUN = siindfun))
sampsi <- siind[which(siind != 0)]
bmean <-mean(sampsi)


sitime <- srswor(150, 1500)
siindfun <- function(k){
    if(sitime[k] != 0){
        tmp <- rep(c[k], sitime[k])
    } else {tmp = 0}
}
siind <- unlist(lapply(1:length(sitime), FUN = siindfun))
sampsi <- siind[which(siind != 0)]
cmean <-mean(sampsi)


mean <-c(c(amean,bmean),cmean)
for(i in 1:3){
    cat(mean[i],"\n")
}
close(input)
