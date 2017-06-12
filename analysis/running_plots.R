rm(list=ls())
DATA_DIR <- "~/symbolic_results/tests"
source("~/Dropbox/arctic-browning/analysis/lib.R")
EXP1 = "control_mandarin"
EXP2 = "mandarin"
#EXP3 = "mallard"
exp1 <- getDataFrame(EXP1) 
exp2 <- getDataFrame(EXP2)
#exp3 <- getDataFrame(EXP3)
library(ggplot2)
XMAX <- max(exp1$generation, exp2$generation)

ggplot(exp1, aes(generation, min_fitness, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = "Control", subtitle = "Without Range Operator") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(0, 1) + xlim(0, XMAX)

ggplot(exp2, aes(generation, min_fitness, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = "Experiment", subtitle = "With Range Operator") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(0, 1) + xlim(0, XMAX)

ggplot(exp3, aes(generation, min_fitness, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = "Experiment 2", subtitle = "Mutate Single Range Operator.") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(.4, 1) + xlim(0, XMAX)


exp1.avg <- calcAvg(exp1)
exp2.avg <- calcAvg(exp2)
exp3.avg <- calcAvg(exp3)

exp1.avg$experiment <- EXP1
exp2.avg$experiment <- EXP2
exp3.avg$experiment <- EXP3

all.exp <- rbind(
  exp1.avg[, c(which(names(exp1.avg) == "generation"), 
               which(names(exp1.avg) == "min_fitness"),
               which(names(exp1.avg) == "avg_size"),
               which(names(exp1.avg) == "size_min_best_tree"),
               which(names(exp1.avg) == "experiment"))], 
  exp2.avg[, c(which(names(exp2.avg) == "generation"), 
               which(names(exp2.avg) == "min_fitness"),
               which(names(exp2.avg) == "avg_size"),
               which(names(exp2.avg) == "size_min_best_tree"),
               which(names(exp2.avg) == "experiment"))], 
  exp3.avg[, c(which(names(exp3.avg) == "generation"), 
               which(names(exp3.avg) == "min_fitness"),
               which(names(exp3.avg) == "avg_size"),
               which(names(exp3.avg) == "size_min_best_tree"),
               which(names(exp3.avg) == "experiment"))])

ggplot(all.exp, aes(generation, min_fitness, colour = experiment)) + geom_line() +
  labs(title = "Experiments", subtitle = "Average Minimum Fitness") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(.4, 1) + xlim(0, XMAX)

ggplot(all.exp, aes(generation, avg_size, colour = experiment)) + geom_line() +
  labs(title = "Experiments", subtitle = "Average Size") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5))

ggplot(all.exp, aes(generation, size_min_best_tree, colour = experiment)) + geom_line() +
  labs(title = "Experiments", subtitle = "Average Size Minimum Best Tree") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5))

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
