rm(list = ls())
source("~/Dropbox/arctic-browning/analysis/lib.R")

set.seed(2017)

maximumFunction <- function(dat) {
  res <- pmax(dat[,1], dat[,2], dat[,3], dat[,4], dat[,5], dat[,6])
  return(res)
}

dat <- buildNormalData(1000, 60, 5, 1, c(1,1,1,1,1,1))
Y <- maximumFunction(dat)
synthetic <- cbind(dat, Y)
heatmap(as.matrix(synthetic), Rowv = NA, Colv = NA)
write.csv(synthetic, "~/design_matrices/maximum.csv", row.names = FALSE)