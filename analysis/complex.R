rm(list = ls())
source("~/Dropbox/arctic-browning/analysis/lib.R")


simulation <- function(dat) {
  res <- apply(dat[,1:20], 1, sum) + 
    apply(dat[,13:25], 1, max) +
    dat[,53]^3 +
    apply(dat[,30:47], 1, min) +
    exp(dat[,59])
  return(res)
}

dat <- matrix(rnorm(100000*60, mean = 60, sd = 15), ncol=60)

Y <- simulation(dat)
synthetic <- cbind(dat, Y)
heatmap(as.matrix(synthetic), Rowv = NA, Colv = NA)
write.csv(synthetic, "~/design_matrices/complex.csv", row.names = FALSE)