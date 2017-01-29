rm(list = ls())
setwd("~/Dropbox/arctic-browning/analysis/data")
ndvi_t <- read.csv("ndvi_temporal_stats.csv")
ndvi_t$mean <- ndvi_t$mean * .0001
ndvi_t$year <- as.Date(as.character(ndvi_t$year), "%Y")

library(ggplot2)
ggplot(ndvi_t, aes(x = year, y = mean)) + 
  geom_line(size = 3, color="black") +
  geom_point(size = 3, color="red") +
  labs(title = "Mean NDVI over the NAR - Summer - Time -> Space", 
       y = "NDVI", x = "Year") +
  scale_x_date(date_breaks = "1 year", date_labels = "%Y") + 
  scale_y_continuous(limits = c(.64,.71))
