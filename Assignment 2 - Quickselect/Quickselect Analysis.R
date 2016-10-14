library(igraph)
library(dplyr)
library(ggplot2)
library(microbenchmark)
library(scales)

setwd("C:\\Users\\albyr\\Documents\\data_structures_and_algorithms\\Assignment 2 - Quickselect/")

results_size <- read.csv("quickselect/Results/increasing_n_972354100.csv", header = T, sep = ",")
results_rank <- read.csv("quickselect/Results/increasing_rank_214438400.csv", header = T, sep = ",")

grouped_data_size <- results_size  %>% group_by(vector_size) %>% summarise_each(funs(mean(.)), -iteration_number)

# NUMBER OF COMPARISONS
p <- ggplot(grouped_data_size, aes(x= vector_size, y = num_of_comparisons))
p <- p + geom_line(size = 3, color = "#ff4d4d", aes(x = vector_size, y = th_num_of_comparisons), lineend = "round")

p <- p + geom_line(size = 0.8, color = "#4f72fc") + geom_point(size = 1.5, color ="#021f91") 

p <- p + theme_minimal() + xlab("Size of the vector") + ylab("Number of comparisons")
p <- p + theme(axis.text=element_text(size=12), axis.title=element_text(size=14)) + theme(axis.text.x = element_text(angle = 90, hjust = 1))
p <- p + scale_y_continuous(labels = comma)
p <- p  +  ggtitle(bquote(atop(.("Quickselect applied on a vector of increasing size"), atop(italic(.("Rank of the element to be found: vector_size / 2;  Size of each steps: 10000")), "")))) 

p

# TIME COMPLEXITY
p <- ggplot(grouped_data_size, aes(x= vector_size, y = time..usec. / 1000))

fit <- lm(time..usec. ~ vector_size, data = grouped_data_size)
p <- p + geom_line(size = 3, color = "#ff4d4d", aes(x = vector_size, y = (vector_size * fit$coefficients[2] + fit$coefficients[1]) / 1000), lineend = "round")

p <- p + geom_line(size = 0.8, color = "#4f72fc") + geom_point(size = 1.5, color ="#021f91") 

p <- p + theme_minimal() + xlab("Size of the vector") + ylab("Time required [msec]")
p <- p + theme(axis.text=element_text(size=12), axis.title=element_text(size=14)) + theme(axis.text.x = element_text(angle = 90, hjust = 1))
p <- p + scale_y_continuous(labels = comma)
p <- p  +  ggtitle(bquote(atop(.("Quickselect applied on a vector of increasing size"), atop(italic(.("Linear model: slope = 4.39 * 10^-6, intercept = -29.02")), "")))) 
p

# NUMBER OF COMPARISONS
grouped_data_rank <- results_rank  %>% group_by(rank) %>% summarise_each(funs(mean(.)), -iteration_number)

p <- ggplot(grouped_data_rank, aes(x= rank, y = num_of_comparisons))
p <- p + geom_line(size = 5, color = "#ff4d4d", aes(x = rank, y = th_num_of_comparisons), lineend = "round")

p <- p + geom_line(size = 0.8, color = "#4f72fc") + geom_point(size = 1, color ="#021f91") 

p <- p + theme_minimal() + xlab("Rank") + ylab("Number of comparisons")
p <- p + theme(axis.text=element_text(size=12), axis.title=element_text(size=14)) + theme(axis.text.x = element_text(angle = 90, hjust = 1))
p <- p + scale_y_continuous(labels = comma)
p <- p  +  ggtitle(bquote(atop(.("Quickselect, select items of increasing rank"), atop(italic(.("Size of the vector: 100000; Size of each step: 123")), "")))) 

p

# TIME COMPLEXITY
p <- ggplot(grouped_data_rank, aes(x= rank, y = time..usec. / 1000))

fit <- lm(time..usec. ~ poly(rank,3), data = grouped_data_rank)
p <- p + geom_line(size = 3, color = "#ff4d4d", aes(x = rank, y = predict(fit, newdata = data.frame(rank = grouped_data_rank$rank)) / 1000), lineend = "round")

p <- p + geom_line(size = 0.8, color = "#4f72fc") + geom_point(size = 1.5, color ="#021f91") 

p <- p + theme_minimal() + xlab("Rank") + ylab("Time required [msec]")
p <- p + theme(axis.text=element_text(size=12), axis.title=element_text(size=14)) + theme(axis.text.x = element_text(angle = 90, hjust = 1))
p <- p + scale_y_continuous(labels = comma)
p <- p  +  ggtitle(bquote(atop(.("Quickselect, select items of increasing rank"), atop(italic(.("Regression done with a polynomial model of order 3")), "")))) 
p


