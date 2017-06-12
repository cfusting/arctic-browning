rm(list = ls())
source("~/Dropbox/arctic-browning/analysis/lib.R")

linearCombination <- function(dat) {
  res <- dat[,1] + dat[,2] + dat[,3] + dat[,4] + dat[,5] + dat[,6]
  return(res)
}

dat <- buildNormalData(1000, 60, 3, 5, c(1,2,3,4,5,6))
Y <- linearCombination(dat)
synthetic <- cbind(dat, Y)
heatmap(as.matrix(synthetic), Rowv = NA, Colv = NA)
write.csv(synthetic, "~/design_matrices/linear_combination.csv", row.names = FALSE)