rm(list = ls())
setwd("~/Dropbox/browning/results")
PIXELS <- 10690908
evi <- read.csv("evistats.csv", na.strings = "--") 
evi$mean <- evi$mean* .0001
evi$date <- as.Date(substring(evi$key, 2), "%Y%j")
evi$year <- format(evi$date, "%Y")
evi.ag <- aggregate(mean ~ year, evi,
                    FUN = sum)
evi$doy<- format(evi$date, "%j")

ndvi <- read.csv("ndvistats.csv", na.strings = "--") 
ndvi$mean <- ndvi$mean * .0001
ndvi$date <- as.Date(substring(ndvi$key, 2), "%Y%j")
ndvi$year <- format(ndvi$date, "%Y")
ndvi$weight <- ndvi$pixels / PIXELS
ndvi.ag <- aggregate(mean ~ year, ndvi,
                    FUN = sum)
ndvi$doy <- as.numeric(format(ndvi$date, "%j"))
ndvi.sum <- subset(ndvi, doy >= 162 & doy <= 255)
ndvi.sum.ag <- aggregate(mean ~ year, ndvi.sum,
                    FUN = mean)

library(ggplot2)
ggplot(evi, aes(x = date, y = mean, group = 1, color = std)) + 
  geom_line(size = 3) +
  labs(title = "Mean EVI over the NAR ", y = "EVI", x = "Date") +
  scale_color_gradient(low = "green", high = "red")

ggplot(ndvi, aes(x = date, y = mean, group = 1)) + 
  geom_line(color = "blue") +
  labs(title = "Mean NDVI over the NAR", y = "NDVI", x = "Date")

ggplot(evi.ag, aes(x = year, y = mean, group = 1)) +
  geom_line(size = 2, color = "green") +
  geom_point(size = 3) +
  labs(title = "Mean EVI over the NAR - Yearly Sum", x = "Year", y = "EVI")

ggplot(ndvi.ag, aes(x = year, y = mean, group = 1)) +
  geom_line(size = 2, color = "blue") +
  geom_point(size = 3) +
  labs(title = "Mean NDVI over the NAR - Yearly Sum", 
       x = "Year", y = "NDVI")

ggplot(ndvi.sum.ag[1:13,], aes(x = year, y = mean, group = 1)) +
  geom_line(size = 2, color = "red") +
  geom_point(size = 3) +
  labs(title = "Mean NDVI over the NAR - Summer Mean", 
       x = "Year", y = "NDVI")
