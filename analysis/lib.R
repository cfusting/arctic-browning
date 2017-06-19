getDataFrame <- function(experiment.name, directory) {
  files <- list.files(directory, pattern = paste("^afsc_po_", experiment.name, "_\\d+.log", sep=""),
                      full.names = TRUE)
  for(file in files) {
    cat("Matched file:", file, "\n")
  }
  pattern <- "afsc_po_.+_\\d+.log"
  seeds <- unlist(lapply(files, function(x) { 
    m <- regexpr(pattern, x) 
    seed <- regmatches(x, m)
    return(regmatches(seed, regexpr("\\d+", seed)))
  }))
  dats <- lapply(files, read.csv)
  dats.labeled <- lapply(1:length(dats), function(i) {
    dats[[i]]$seed <- rep(seeds[i], nrow(dats[[i]])) 
    dats[[i]]$generation <- 1:nrow(dats[[i]])
    return(dats[[i]])
  })
  df <- do.call("rbind", dats.labeled)
  return(df)
}

calcAvg <- function(dat) {
  return(aggregate(dat, by=list(gen = dat$generation), FUN = mean))
}

zeroOne <- function(x) {
  return((x - min(x)) / diff(range(x)))
}

computeTarget <- function(dat) {
  res <- .2 * dat[,1] + 
    .1 * (dat[,2] * dat[,3]) + 
    .23 * dat[,4]^2 + 
    .2 * pmin(dat[,5], dat[,6], dat[,7], dat[,8]) +
    .1 * dat[,9] + 
    .1 * dat[,10]^3 #+
    #.05 * zeroOne(rnorm(nrow(dat)))
  return(res)
}

computeSimpleTarget <- function(dat) {
  res <- dat[,1] + dat[,2] + dat[,3] + dat[,4] + dat[,5] + dat[,6]
  return(res)
}

computeMediumTarget <- function(dat) {
  res <- dat[,1] + dat[,2] + dat[,3] + dat[,4] + dat[,5] + dat[,6]
  return(res)
}

buildNormalData <- function(n, mean, stdev, multiplier, values) {
  dat <- data.frame(
    X0 = rnorm(n, mean = mean + values[1] * multiplier, sd = stdev),
    X1 = rnorm(n, mean = mean + values[2] * multiplier, sd = stdev),
    X2 = rnorm(n, mean = mean + values[3] * multiplier, sd = stdev),
    X3 = rnorm(n, mean = mean + values[4] * multiplier, sd = stdev),
    X4 = rnorm(n, mean = mean + values[5] * multiplier, sd = stdev),
    X5 = rnorm(n, mean = mean + values[6] * multiplier, sd = stdev)
  )
  return(dat)
}