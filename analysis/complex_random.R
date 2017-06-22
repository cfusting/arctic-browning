rm(list = ls())
source("~/Dropbox/arctic-browning/analysis/lib.R")

set.seed(2017)

simulation <- function(dat) {
  res <- apply(dat[,1:20], 1, sum) + 
    apply(dat[,13:25], 1, max) +
    dat[,53] + 
    apply(dat[,50:59], 1, mean) +
    dat[,33]
  return(res)
}

dat <- buildNormalMatrix()

Y <- simulation(dat)
synthetic <- cbind(dat, Y)
summary(synthetic)
write.csv(synthetic, "~/design_matrices/complex_random.csv", row.names = FALSE)