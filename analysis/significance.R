range01 <- function(x){(x)/(max(x))}
control <- read.csv("~/symbolic_results/complex_random.csv_control/complex_random_control_best_validation")
experiment <- read.csv("~/symbolic_results/complex_random.csv_lesser_scaup/complex_random_lesser_scaup_best_validation")
both <- rbind(control, experiment)
both <- both$test_error
both <- c(both, 1609.7507484)
both <- c(both, 0.381876650791)
control$test_error_scaled <- range01(both)[1:40]
experiment$test_error_scaled <- range01(both)[41:80]
mu.scaled <- range01(both)[81]
cv.scaled <- range01(both)[82]
summary(control)
summary(experiment)
wilcox.test(control$test_error_scaled, experiment$test_error_scaled, 
            conf.level = 0.99, conf.int = TRUE)
wilcox.test(control$test_error_scaled, mu = mu.scaled, alternative = "l", 
            conf.level = 0.99, conf.int = TRUE)
wilcox.test(experiment$test_error_scaled, mu = mu.scaled, alternative = "l", 
            conf.level = 0.99, conf.int = TRUE)
rm(list=ls())
range01 <- function(x){(x)/(max(x))}
getInfIndex <- function(x) {
  inf.index <- nrow(x) + 1
  for(i in 1:nrow(x)) {
    if(x[i,]$test_error == Inf) {
      inf.index <- i
      break
    }
  } 
  return(inf.index)
}
control <- read.csv("~/symbolic_results/training_matrix_lst_snow_2002_2013_.15.hdf_control/training_matrix_lst_snow_2002_2013_.15_control_best_validation")
experiment <- read.csv("~/symbolic_results/training_matrix_lst_snow_2002_2013_.15.hdf_lesser_scaup/training_matrix_lst_snow_2002_2013_.15_lesser_scaup_best_validation")
control <- control[order(control$test_error), ]
control.inf.index <- getInfIndex(control)
experiment <- experiment[order(experiment$test_error), ]
experiment.inf.index <- getInfIndex(experiment)
remove.index <- min(control.inf.index, experiment.inf.index) - 1
control <- control[1:remove.index, ]
experiment <- experiment[1:remove.index, ]
both <- rbind(control, experiment)
both <- both$test_error
both <- c(both, 436449.887661)
both <- c(both, 429879.34591)
control$test_error_scaled <- range01(both)[1:39]
experiment$test_error_scaled <- range01(both)[40:78]
mu.scaled <- range01(both)[79]
cv.scaled <- range01(both)[80]
summary(control)
summary(experiment)
wilcox.test(control$test_error_scaled, experiment$test_error_scaled, conf.level = 0.99, conf.int = TRUE)
wilcox.test(control$test_error_scaled, mu = mu.scaled, alternative = "l", conf.level = 0.99, conf.int = TRUE)
wilcox.test(experiment$test_error_scaled, mu = mu.scaled, alternative = "l", conf.level = 0.99, conf.int = TRUE)
