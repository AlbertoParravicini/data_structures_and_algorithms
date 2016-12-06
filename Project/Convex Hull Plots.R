library(igraph)
library(dplyr)
library(ggplot2)
library(microbenchmark)
library(scales)
library(ggforce)

set.seed(12)

# SUPPORT PLOTS
# Draw a convex hull

X <- floor(matrix(runif(40)*20, ncol = 2))
X_frame <- data.frame(X)[-c(3, 8),]

p <- ggplot(data = X_frame, aes(x = X1, y = X2)) + geom_point(size = 2, color ="#021f91") 

hull <- data.frame(X[chull(X),])

p <- p + geom_point(size = 3, color ="#a52918", data = hull, aes(x = X1, y = X2))
p <- p + geom_polygon(color ="#a52918", data = hull, aes(x = X1, y = X2), fill = "#ff9b8e", alpha = 0.2)


p <- p + theme_void()


p 



# JARVIS MARCH

X <- matrix(c(3, 21,
              6, 16,
      
              15, 10,
              24, 15,
              21, 21,
              
              21, 28,
              
              8, 25,
              
              14, 18
              ), ncol = 2, byrow = T)

X_frame = data.frame(X1 = X[, 1], X2 = X[, 2])
p <- ggplot() + xlim(c(0,32)) + ylim(c(0,32))

p <- ggplot(data = X_frame, aes(x = X1, y = X2)) 

p <- p + geom_line(size = 1, color ="#244f96", data = X_frame[1:3, ], aes(x = X1, y = X2))

for (i in 5:8) {
  p <- p + geom_line(size = 1, color ="#f49e42", data = X_frame[c(3, i), ], aes(x = X1, y = X2), linetype="dotted")
}
p <- p + geom_curve(aes(xend = 13.13, x = 16.95, yend = 11.25, y = 11.07), size = 1, color = "#244f96", linetype="dashed")
p <- p + geom_line(size = 1, color ="#a52918", data = X_frame[c(3, 4), ], aes(x = X1, y = X2))

p <- p + geom_point(size = 2, color ="#021f91") 
p <- p + geom_point(size = 2, color ="#f49e42", data = X_frame[5:8, ], aes(x = X1, y = X2))
p <- p + geom_point(size = 2, color ="#a52918", data = X_frame[4, ], aes(x = X1, y = X2))

p <- p + theme_void()

p


# CHAN'S STEP

X <- matrix(c(3, 21,
              6, 16,
              10, 20,
              8, 26,
              5, 25,
              
              
              12, 15,
              15, 10,
              24, 15,
              21, 23,
              14, 22,
              
              12, 21,
              15, 18,
              20, 22,
              17, 28,
              13, 26,
              
              21, 28,
              24, 27,
              25, 30,
              19, 31), ncol = 2, byrow = T)

X_frame = data.frame(X1 = X[, 1], X2 = X[, 2])
p <- ggplot() + xlim(c(0,32)) + ylim(c(8,32))

p <- p + geom_point(size = 2, color ="#427af4", data = X_frame[1:5, ], aes(x = X1, y = X2))
p <- p + geom_polygon(color ="#427af4", data = X_frame[1:5, ], aes(x = X1, y = X2), fill = "#427af4", alpha = 0.2)


p <- p + geom_point(size = 2, color ="#427af4", data = X_frame[6:10, ], aes(x = X1, y = X2))
p <- p + geom_polygon(color ="#427af4", data = X_frame[6:10, ], aes(x = X1, y = X2), fill = "#427af4", alpha = 0.2)

p <- p + geom_point(size = 2, color ="#427af4", data = X_frame[11:15, ], aes(x = X1, y = X2))
p <- p + geom_polygon(color ="#427af4", data = X_frame[11:15, ], aes(x = X1, y = X2), fill = "#427af4", alpha = 0.2)

p <- p + geom_point(size = 2, color ="#427af4", data = X_frame[16:19, ], aes(x = X1, y = X2))
p <- p + geom_polygon(color ="#427af4", data = X_frame[16:19, ], aes(x = X1, y = X2), fill = "#427af4", alpha = 0.2)


p <- p + geom_point(size = 2, color ="#244f96", data = X_frame[1:2, ], aes(x = X1, y = X2))
p <- p + geom_line(size = 1, color ="#244f96", data = X_frame[1:2, ], aes(x = X1, y = X2))

p <- p + geom_point(size = 2, color ="#f49e42", data = X_frame[c(17, 12), ], aes(x = X1, y = X2))
p <- p + geom_line(size = 1, color ="#f49e42", data = X_frame[c(2, 12), ], aes(x = X1, y = X2), linetype="dotted")
p <- p + geom_line(size = 1, color ="#f49e42", data = X_frame[c(2, 17), ], aes(x = X1, y = X2), linetype="dotted")



p <- p + geom_point(size = 2, color ="#a52918", data = X_frame[7, ], aes(x = X1, y = X2))
p <- p + geom_line(size = 1, color ="#a52918", data = X_frame[c(2,7), ], aes(x = X1, y = X2), linetype="dashed")


p <- p + geom_point(size = 2, color ="#244f96", data = X_frame[1:2, ], aes(x = X1, y = X2))
p <- p + geom_line(size = 1, color ="#244f96", data = X_frame[1:2, ], aes(x = X1, y = X2))

p <- p + theme_void()

p
