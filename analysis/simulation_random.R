rm(list = ls())
source("~/Dropbox/arctic-browning/analysis/lib.R")

set.seed(2017)

simulation <- function(dat) {
  res <- apply(dat[,1:20], 1, sum) + 
    apply(dat[,13:25], 1, max)
  return(res)
}

dat <- buildNormalMatrix()
dat <- scale(dat)
Y <- simulation(dat)
synthetic <- cbind(dat, Y)
heatmap(as.matrix(synthetic), Rowv = NA, Colv = NA)
write.csv(synthetic, "~/design_matrices/simulation_random.csv", row.names = FALSE)