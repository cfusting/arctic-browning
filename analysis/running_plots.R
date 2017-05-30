rm(list=ls())
# setwd("~/Dropbox/arctic-browning/analysis/")
DATA_DIR <- "~/symbolic_results"

getDataFrame <- function(experiment.name) {
  files <- list.files(DATA_DIR, pattern = paste("^afsc_po_", experiment.name, "_\\d+.log", sep=""),
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

penguin <- getDataFrame("penguin") 
blue.penguin <- getDataFrame("blue_penguin")
ferret <- getDataFrame("ferret") 

library(ggplot2)
XMAX <- max(penguin$generation, ferret$generation, blue.penguin$generation)

ggplot(ferret, aes(generation, min_fitness, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = "Ferret Experiment", subtitle = "Without Temporal Range Operation") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(.4, 1) + xlim(0, XMAX)

ggplot(penguin, aes(generation, min_fitness, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = "Penguin Experiment", subtitle = "With Temporal Range Operation") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(.4, 1) + xlim(0, XMAX)

ggplot(blue.penguin, aes(generation, min_fitness, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = "Blue Penguin Experiment", subtitle = "With Temporal Range Operation") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(.4, 1) + xlim(0, XMAX)

ggplot(ferret, aes(generation, avg_fitness, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = "Ferret Experiment", subtitle = "Without Temporal Range Operation") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(.4, 1) + xlim(0, XMAX)

ggplot(penguin, aes(generation, avg_fitness, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = "Penguin Experiment", subtitle = "With Temporal Range Operation") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(.4, 1) + xlim(0, XMAX)

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
