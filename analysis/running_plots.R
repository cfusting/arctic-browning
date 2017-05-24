rm(list=ls())
setwd("~/Dropbox/arctic-browning/analysis/")
DATA_DIR <- "~/symbolic_results"

getDataFrame <- function(experiment.name) {
  files <- list.files(DATA_DIR, pattern = paste("^afsc_po_", experiment.name, sep=""),
                      full.names = TRUE)
  pattern <- "afsc_po_.+_\\d+.log"
  seeds <- unlist(lapply(files, function(x) { 
    m <- regexpr(pattern, x) 
    seed <- regmatches(x, m)
    return(regmatches(seed, regexpr("\\d+", seed)))
  }))
  dats <- lapply(files, read.csv)
  dats.labeled <- lapply(1:length(dats), function(i) {
    dats[[i]]$seed <- rep(seeds[i], nrow(dats[[i]])) 
    return(dats[[i]])
  })
  df <- do.call("rbind", dats.labeled)
  return(df)
}

penguin <- getDataFrame("penguin") 
ferret <- getDataFrame("ferret") 

library(ggplot2)

ggplot(ferret, aes(cpu_time, min_fitness, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = "Ferret Experiment", subtitle = "Without Temporal Range Operation") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(.4, 1)

ggplot(penguin, aes(cpu_time, min_fitness, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = "Penguin Experiment", subtitle = "With Temporal Range Operation") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(.4, 1)

ggplot(ferret, aes(cpu_time, avg_size, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = "Ferret Experiment", subtitle = "Without Temporal Range Operation") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(0, 80)

ggplot(penguin, aes(cpu_time, avg_size, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = "Penguin Experiment", subtitle = "With Temporal Range Operation") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(0, 80)

ggplot(penguin, aes(avg_size, min_fitness, colour = seed)) + geom_point(show.legend = FALSE) +
  labs(title = "Penguin Experiment", subtitle = "With Temporal Range Operation") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5))

penguin.agg <- aggregate(penguin, by = list(penguin$seed), FUN = min)
penguin.stuck.seeds <- as.numeric(subset(penguin.agg, penguin.agg$min_fitness >= .57)$seed)
penguin.stuck <- subset(penguin, seed %in% penguin.stuck.seeds)

ggplot(penguin.stuck, aes(cpu_time, avg_size, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = "Penguin Experiment", 
       subtitle = "Runs where min fitness is greater than or equal to .57") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5))
