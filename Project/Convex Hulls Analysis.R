library(igraph)
library(dplyr)
library(ggplot2)
library(microbenchmark)
library(scales)

set.seed()

setwd("C:/Users/albyr/Documents/data_structures_and_algorithms/Project/")

results_points <- read.csv("Results/increasing_n_2016_11_24_12_26_38.csv", header = T, sep = ",")
results_hulls <- read.csv("Results/increasing_hull_2016_11_24_14_56_23.csv", header = T, sep = ",") %>% filter(time.sec. <= 15)
results_all <- read.csv("Results/increasing_points_hull_2016_12_04_22_52_13.csv", header = T, sep = ",")

grouped_data_points <- results_points %>% group_by(input_size) %>% summarise_each(funs(median(.)), -iteration_number)#summarise_each(funs(median(.), mean(.), sd(.), min(.), max(.)), -iteration_number, -hull_size)

# INCREASING POINTS
p <- ggplot(grouped_data_points, aes(x= input_size, y = time.sec.))

# Linear regression of the points
cols <- c("Real Data" = "#4f72fc", "Linear Model" = "#ff4d4d")

fit <- lm(time.sec. ~ input_size, data = grouped_data_points)
p <- p + stat_boxplot(geom ='errorbar', width = 0, data = results_points, aes(group = input_size, y = time.sec., col = "Real Data"), coef = 1) 
p <- p + geom_line(size = 1, aes(x = input_size, y = (input_size * fit$coefficients[2] + fit$coefficients[1]), col = "Linear Model"), lineend = "round", linetype = "twodash")

p <- p + geom_line(size = 1.4, alpha = 0.4, aes(col = "Real Data"), linetype = "solid") + geom_point(size = 2, color ="#021f91") 

p <- p + theme_minimal() + xlab("Number of Points") + ylab("Execution time [sec]")
p <- p + theme(axis.text=element_text(size=12), axis.title=element_text(size=14)) + theme(axis.text.x = element_text(angle = 90, hjust = 1))
p <- p + scale_y_continuous(labels = comma)
p <- p + ggtitle("")
# <- p + ggtitle(bquote(atop(.("Chan's algorithm with increasing number of points"), atop(italic(.("Hull size: 1000")), "")))) 
p <- p + scale_colour_manual(name="",values=cols) + theme(legend.position="top")

p



# INCREASING HULL SIZE
grouped_data_hulls <- results_hulls %>% group_by(hull_size)  %>% summarise_each(funs(mean(.)), -iteration_number)#%>% summarise_each(funs(median(.), mean(.), sd(.), min(.), max(.)), -iteration_number, -input_size)

p <- ggplot(grouped_data_hulls, aes(x= hull_size, y = time.sec.))

# Linear regression of the hull size
cols <- c("Real Data" = "#4f72fc", "Logarithmic Model" = "#ff4d4d")

fit <- lm(time.sec. ~ log(hull_size), data = grouped_data_hulls)
pred = seq(1000, 20000, by = 1000)
y_pred = predict(fit, newdata = data.frame(hull_size = pred))

pred_table = data.frame(x = pred, y = y_pred)

p <- p + stat_boxplot(geom ='errorbar', width = 0, data = results_hulls, aes(group = hull_size, y = time.sec., col = "Real Data"), coef = 1) 
p <- p + geom_line(data = pred_table, size = 1, aes(x = x, y = y, col = "Logarithmic Model"), lineend = "round", linetype = "twodash")

p <- p + geom_line(size = 1.4, alpha = 0.6, aes(col = "Real Data"), linetype = "solid") + geom_point(size = 2, color ="#021f91") 

p <- p + theme_minimal() + xlab("Size of the Hull") + ylab("Execution time [sec]")
p <- p + theme(axis.text=element_text(size=12), axis.title=element_text(size=14)) + theme(axis.text.x = element_text(angle = 90, hjust = 1))
p <- p + scale_y_continuous(labels = comma)
#p <- p + ggtitle(bquote(atop(.("Chan's algorithm with hulls of increasing size"), atop(italic(.("Total number of points: 40000")), "")))) 
p <- p + ggtitle
p <- p + scale_colour_manual(name="",values=cols) + theme(legend.position="top")

p



# INCREASING POINTS AND HULL

grouped_data_all <- results_all %>% group_by(input_size) %>% summarise_each(funs(median(.), mean(.), sd(.), min(.), max(.)), -iteration_number, -time.sec.)

# INCREASING POINTS
p <- ggplot(grouped_data_all, aes(x= input_size, y = time.sec.))

# Linear regression of the points
cols <- c("Real Data" = "#4f72fc", "n log(h)" = "#ff4d4d")

fit <- lm(time.sec. ~ (input_size * log(hull_size)), data = grouped_data_all)
pred = seq(10000, 100000, by = 10000)
y_pred = predict(fit, newdata = data.frame(input_size = pred))

pred_table = data.frame(x = pred, y = y_pred)

p <- p + stat_boxplot(geom ='errorbar', width = 0, data = results_all, aes(group = input_size, y = time.sec., col = "Real Data"), coef = 1) 
p <- p + geom_line(data = pred_table, size = 1, aes(x = x, y = y, col = "n log(h)"), lineend = "round", linetype = "twodash")

p <- p + geom_line(size = 1.4, alpha = 0.6, aes(col = "Real Data"), linetype = "solid") + geom_point(size = 2, color ="#021f91") 

p <- p + theme_minimal() + xlab("Number of Points") + ylab("Execution time [sec]")
p <- p + theme(axis.text=element_text(size=12), axis.title=element_text(size=14)) + theme(axis.text.x = element_text(angle = 90, hjust = 1))
p <- p + scale_y_continuous(labels = comma)
p <- p + ggtitle(bquote(atop(.("Chan's algorithm with increasing number of points"), atop(italic(.("Hull size: 1000")), "")))) 
p <- p + scale_colour_manual(name="",values=cols) + theme(legend.position="top")

p


