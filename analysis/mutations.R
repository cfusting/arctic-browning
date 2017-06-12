setwd("~/symbolic_results/")
system('cat mutation_stats_afsc_po_mallard_667.log | cut -d , -f1,2,3,4 > tmp.csv')
mutations <- read.csv("tmp.csv")
system('rm tmp.csv')

library(ggplot)
library(reshape2)
dat <- melt(mutations, id = c("generation"))

ggplot(dat, aes(generation, value, color = variable)) + geom_line()
