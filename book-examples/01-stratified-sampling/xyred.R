#! /usr/bin/env Rscript
input <- file("stdin","r")
smean <- NULL
while(length(currentline <- readLines(input, n=1, warn=F))>0){
            data <- unlist(strsplit(currentline," "))
            ncol <- length(data)
            smean <- rbind(smean, as.double(data[1:ncol]))
}

print(str <- mean(2/9*smean[1]+4/9*smean[2]+1/3*smean[3]))
close(input)
