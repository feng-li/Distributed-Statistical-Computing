#! /usr/bin/env Rscript
input = file("stdin", "r")
poi = readLines(input, warn = F)
poi = matrix(as.numeric(unlist(strsplit(poi, ","))), ncol = 5, byrow = T)
poi = data.frame(poi)
n = dim(poi)[1]
set.seed(1)
sam = sample(n)
poi = poi[sam, ]
write.csv(poi, "poisson2.csv")
close(input)
