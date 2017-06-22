rm(list = ls())
source("~/Dropbox/arctic-browning/analysis/lib.R")

set.seed(2017)

simulation <- function(dat) {
  res <- apply(dat[,1:20], 1, sum) + 
    apply(dat[,13:25], 1, max)
  return(res)
}

dat <- buildNormalMatrix()
Y <- simulation(dat)
synthetic <- cbind(dat, Y)
summary(synthetic)
write.csv(synthetic, "~/design_matrices/simulation_random.csv", row.names = FALSE)