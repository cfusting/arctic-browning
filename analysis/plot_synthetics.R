rm(list=ls())
source("~/Dropbox/arctic-browning/analysis/lib.R")
DATA_DIR <- "~/symbolic_results/tests"
EXP1 = "simulation_control_mandarin"
EXP2 = "simulation_mandarin"
EXP1.name = "Control"
EXP2.name = "Mandarin"
EXP1.SUB = "Without Range Operator"
EXP2.SUB = "With Range Operator"
exp1 <- getDataFrame(EXP1) 
exp2 <- getDataFrame(EXP2)
library(ggplot2)
XMAX <- max(exp1$generation, exp2$generation)
YMAX.fitness <- max(exp1$min_fitness, exp2$min_fitness)
YMAX.size <- max(exp1$avg_size, exp2$avg_size)
ggplot(exp1, aes(generation, min_fitness, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = EXP1.name, subtitle = EXP1.SUB) +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(0, YMAX.fitness) + xlim(0, XMAX)
ggplot(exp2, aes(generation, min_fitness, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = EXP2.name, subtitle = EXP2.SUB) +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(0, YMAX.fitness) + xlim(0, XMAX)
ggplot(exp1, aes(generation, avg_size, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = EXP1.name, subtitle = EXP1.SUB) +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(0, YMAX.size)
ggplot(exp2, aes(generation, avg_size, colour = seed)) + geom_line(show.legend = FALSE) +
  labs(title = EXP2.name, subtitle = EXP2.SUB) +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(0, YMAX.size)

exp1.avg <- calcAvg(exp1)
exp2.avg <- calcAvg(exp2)
exp1.avg$experiment <- EXP1.name
exp2.avg$experiment <- EXP2.name
exps <- rbind(exp1.avg, exp2.avg)
XMAX.avg <- max(exps$generation)
YMAX.fitness.avg <- max(exps$min_fitness)
YMAX.size.avg <- max(exps$avg_size)
ggplot(exps, aes(generation, min_fitness, colour = experiment)) + geom_line() +
  labs(title = "Minimum Fitness Averaged Over Seeds") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(0, YMAX.fitness.avg) + xlim(0, XMAX.avg)
ggplot(exps, aes(generation, avg_size, colour = experiment)) + geom_line() +
  labs(title = "Average Size Averaged Over Seeds") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(0, YMAX.size.avg) + xlim(0, XMAX.avg)
