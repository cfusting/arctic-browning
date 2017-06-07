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

exp1 <- getDataFrame("duck") 
exp2 <- getDataFrame("domestic_duck")
exp3 <- getDataFrame("mallard") 

library(ggplot2)
XMAX <- max(exp1$generation, exp2$generation, exp3$generation)

ggplot(exp1, aes(generation, min_fitness, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = "Control", subtitle = "Without Temporal Range Mutation") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(.4, 1) + xlim(0, XMAX)

ggplot(exp2, aes(generation, min_fitness, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = "Experiment", subtitle = "Mutate All Parametrized Nodes") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(.4, 1) + xlim(0, XMAX)

ggplot(exp3, aes(generation, min_fitness, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = "Experiment 2", subtitle = "Mutate Single Parametrized Node.") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(.4, 1) + xlim(0, XMAX)

ggplot(exp1, aes(generation, avg_size, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = "Control", subtitle = "Without Temporal Range Mutation") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(0, 80)

ggplot(exp2, aes(generation, avg_size, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = "Experiment", subtitle = "With Temporal Range Mutation") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(0, 80)

ggplot(exp2, aes(cpu_time, avg_size, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = "Blue exp1 Experiment", subtitle = "With Temporal Range Operation") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(0, 80)

ggplot(exp1, aes(avg_size, min_fitness, colour = seed)) + geom_point(show.legend = FALSE) +
  labs(title = "exp1 Experiment", subtitle = "With Temporal Range Operation") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5))

exp1.agg <- aggregate(exp1, by = list(exp1$seed), FUN = min)
exp1.stuck.seeds <- as.numeric(subset(exp1.agg, exp1.agg$min_fitness >= .57)$seed)
exp1.stuck <- subset(exp1, seed %in% exp1.stuck.seeds)

ggplot(exp1.stuck, aes(cpu_time, avg_size, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = "exp1 Experiment", 
       subtitle = "Runs where min fitness is greater than or equal to .57") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5))

ggplot(subset(exp3, seed == 6016), 
       aes(generation, avg_parametrized, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = "Mallard", subtitle = "Average Proportion of RangeOperations in Trees") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5))
