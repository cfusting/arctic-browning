rm(list=ls())
source("~/Dropbox/arctic-browning/analysis/lib.R")
DATA.SET <- "simulation"
DATA.TYPE <- "csv"
EXP1.id <- "lesser_scaup"
EXP2.id <- "bufflehead"
EXP1 <- paste(DATA.SET, EXP1.id, sep = "_")
EXP2 <- paste(DATA.SET, EXP2.id, sep = "_")
EXP1.dir <- paste(paste("~/symbolic_results/", paste(DATA.SET, DATA.TYPE, sep = "."), sep = ""), EXP1.id, sep = "_")
EXP2.dir <- paste(paste("~/symbolic_results/", paste(DATA.SET, DATA.TYPE, sep = "."), sep = ""), EXP2.id, sep = "_")
EXP1.name <- "Lesser Scaup"
EXP2.name <- "Bufflhead"
EXP1.SUB <- "Without Range Operator"
EXP2.SUB <- "With Range Operator"
exp1 <- getDataFrame(EXP1, EXP1.dir) 
exp2 <- getDataFrame(EXP2, EXP2.dir)
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

min(exp1.avg$min_fitness)
min(exp2.avg$min_fitness)
min(exp1.avg$avg_fitness)
min(exp2.avg$avg_fitness)

ggplot(exps, aes(generation, log(avg_fitness) / max(log(avg_fitness)), colour = experiment)) + 
  geom_point() + labs(title = "Average Fitness Averaged Over Seeds") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(0, 1) + xlim(0, XMAX.avg)
ggplot(exps, aes(generation, avg_parametrized, colour = experiment)) + 
  geom_line() + labs(title = "Average Parametrized Terminals Averaged Over Seeds") +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  ylim(0, 1) + xlim(0, XMAX.avg)
