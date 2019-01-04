#! /usr/bin/env Rscript
input = file("stdin", "r")
i = 0
coefficients = rep(0,5)
pvalue = rep(0,5)
mean = 0
while(length(mapresult <- readLines(input, n = 1, warn = F)) > 0)
{
    i = i+1
    fields = strsplit(mapresult, ' ')
    if (i%%3 == 1) {
        coefficients = coefficients + as.numeric(fields[[1]]) # 对 1、4、7、10 行的系数求和
    }
    else if (i%%3 == 2) {
        pvalue = pvalue + as.numeric(fields[[1]])
                                        # 对 2、5、8、11 行的 p 值求和
    }
    else if (i%%3 == 0) {
        mean = mean + as.numeric(fields[[1]])
                                        # 对 3、6、9、12 行的误差求和
    }
}
coefficients = coefficients/(i/3)
pvalue = pvalue/(i/3)
mean = mean/(i/3)
cat('coefficients =', coefficients, '\n')
cat('pvalue =', pvalue, '\n')
cat('RME =', mean, '\n')
close(input)
