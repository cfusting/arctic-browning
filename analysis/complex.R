rm(list = ls())
source("~/Dropbox/arctic-browning/analysis/lib.R")

set.seed(2017)

simulation <- function(dat) {
  res <- apply(dat[,1:20], 1, sum) + 
    apply(dat[,13:25], 1, max) +
    dat[,53]^3 + 
    apply(dat[,50:59], 1, mean) +
    dat[,33]^2
  return(res)
}

dat <- matrix(rnorm(1000*60, mean = 60, sd = 15), ncol=60)

Y <- simulation(dat)
synthetic <- cbind(dat, Y)
write.csv(synthetic, "~/design_matrices/complex.csv", row.names = FALSE)