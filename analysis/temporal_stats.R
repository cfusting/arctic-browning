rm(list = ls())
setwd("~/Dropbox/arctic-browning/analysis/data")
ndvi <- read.csv("ndvi_temporal_stats.csv")
ndvi$mean <- ndvi$mean * .0001

library(ggplot2)
ggplot(ndvi[1:13,], aes(x = year, y = mean)) + 
  geom_line(size = 3) +
  geom_point(size = 3) +
  labs(title = "Mean EVI over the NAR ", y = "NDVI", x = "Year")
