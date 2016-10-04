library(igraph)
library(dplyr)
library(ggplot2)
library(microbenchmark)

setwd("C:\\Users\\albyr\\Documents\\data_structures_and_algorithms\\Assignment 1 - Karger's Algorithm")
source("Karger's Algorithm.R")

# -------------------
# -------------------
# Profling Utilities
# -------------------
# -------------------
# Write a csv with the given name and current time.
write_with_name_and_date <- function(results, name, append = T) {
  name <- sprintf("Results/%s - %s.csv", name, Sys.time())
  name <- gsub(":", "", name)
  write.table(results, file = name, append = append, quote = F, col.names = T, sep = " ", row.names = F)
  return(name)
} 

# increasing nodes and edges, 4*k edges
# 50 nodes, increasing edges
# 10 different graphs, 100 tests each

# ---- TEST 1 ----
# Increasing nodes and edges; num_nodes = 20:100, num_edges = 4*num_nodes
min_num_nodes = 1000
max_num_nodes = 1000
step = 10
edge_amplification = 4

results = data.frame(num_vertices = numeric(0), num_edges = numeric(0), iteration = numeric(0), correct = logical(0), time = numeric(0))
file_name <- write_with_name_and_date(results, "karkger_incr_vertices_edges", append = F)


for (num_vert_i in seq(min_num_nodes, max_num_nodes, by = step)) {
  results = data.frame(num_vertices = numeric(0), num_edges = numeric(0), iteration = numeric(0), correct = logical(0), time = numeric(0))
  g <- make_random_connected_graph(num_vert_i, edge_amplification * num_vert_i, details = F)
  real_min_cut <- min_cut(g)
  
  num_iterations <- 50
  correct_results <- 0
  
  for(iteration_i in 1:num_iterations) {
    
    temp_res <- -1
    exec_time <- microbenchmark(
      temp_res <- karger_random_min_cut(g, F, F),
      times = 1,
      unit = "ms"
    )
    if (temp_res == real_min_cut) {
      correct_results <- correct_results + 1
    }
    
    # Store the result in the data frame
    temp_row <-  c(num_vert_i, edge_amplification * num_vert_i, iteration_i, real_min_cut == temp_res, exec_time$time)
    print(temp_row)
    results <- rbind(results, temp_row)
  }
  write.table(file = file_name, x = results, append = T, row.names = F, col.names = F, sep = " ")
}

results <- read.csv("Results/karger_incr_vertices_edges_tot.csv", header = T, sep = " ")
grouped_data <- results  %>% group_by(num_vertices, num_edges) %>% summarise_each(funs(mean(.)), -iteration)

p <- ggplot(grouped_data, aes(x=num_vertices, y = correct))
p <- p + geom_line(size = 1, color = "#4f72fc") + geom_point(size = 2.5, color ="#021f91") 

p <- p + theme_minimal() + xlab("Number of vertices") + ylab("Percentage of correct results")
p <- p + theme(axis.text=element_text(size=12), axis.title=element_text(size=14))
p <- p + scale_x_discrete(limits = grouped_data$num_vertices, expand = 0.05)
p <- p  +  ggtitle(bquote(atop(.("Karger's algorithm with increasing number of vertices and edges"), atop(italic(.("Number of edges: 4 * num_vertices")), "")))) 

theoretical_results <- data.frame(num_vertices = grouped_data$num_vertices, baseline = 2 / (grouped_data$num_vertices * (grouped_data$num_vertices - 1)))
p <- p + geom_line(data = theoretical_results, size = 1, color = "#ff4d4d", aes(x = num_vertices, y = baseline)) + geom_point(data = theoretical_results, size = 2.5, color ="#800000", aes(x = num_vertices, y = baseline)) 
p


# ---- TEST 2 ----
# Increasing edges with fixed number of nodes; num_nodes = 50, num_edges = 50:500
min_num_edges = 50
max_num_edges = 500
step = 50
num_vertices = 50

results = data.frame(num_vertices = numeric(0), num_edges = numeric(0), iteration = numeric(0), correct = logical(0), time = numeric(0))
file_name <- write_with_name_and_date(results, "karkger_incr_edges", append = F)

for (num_edge_i in seq(min_num_edges, max_num_edges, by = step)) {
  results = data.frame(num_vertices = numeric(0), num_edges = numeric(0), iteration = numeric(0), correct = logical(0), time = numeric(0))
  g <- make_random_connected_graph(num_vertices, num_edge_i, details = F)
  real_min_cut <- min_cut(g)
  
  num_iterations <- 50
  correct_results <- 0
  
  for(iteration_i in 1:num_iterations) {
    temp_res <- -1
    exec_time <- microbenchmark(
      temp_res <- karger_random_min_cut(g, F, F),
      times = 1,
      unit = "ms"
    )
    if (temp_res == real_min_cut) {
      correct_results <- correct_results + 1
    }
    
    # Store the result in the data frame
    temp_row <-  c(num_vertices, num_edge_i, iteration_i, real_min_cut == temp_res, (exec_time$time))
    print(temp_row)
    results <- rbind(results, temp_row)
  }
  write.table(file = file_name, x = results, append = T, row.names = F, col.names = F, sep = " ")
}

results <- read.csv("Results/karger_incr_edges_total.csv", header = T, sep = " ")
grouped_data <- results  %>% group_by(num_vertices, num_edges) %>% summarise_each(funs(mean(.)), -iteration)

p <- ggplot(grouped_data, aes(x=num_edges, y = correct))
p <- p + geom_line(size = 1, color = "#4f72fc") + geom_point(size = 2.5, color ="#021f91") 

p <- p + theme_minimal() + xlab("Number of edges") + ylab("Percentage of correct results")
p <- p + theme(axis.text=element_text(size=12), axis.title=element_text(size=14))
p <- p + scale_x_discrete(limits = grouped_data$num_edges, expand = 0.05)
p <- p  +  ggtitle(bquote(atop(.("Karger's algorithm with increasing number of edges"), atop(italic(.("Number of vertices: 50")), "")))) 

theoretical_results <- data.frame(num_vertices = grouped_data$num_edges, baseline = 2 / (grouped_data$num_vertices * (grouped_data$num_vertices - 1)))
p <- p + geom_line(data = theoretical_results, size = 1, color = "#ff4d4d", aes(x = num_vertices, y = baseline)) + geom_point(data = theoretical_results, size = 2.5, color ="#800000", aes(x = num_vertices, y = baseline)) 
p


# ------ PLOT THE EXECUTION TIME ----

# TEST 1
results <- read.csv("Results/karger_incr_vertices_edges_tot.csv", header = T, sep = " ")
grouped_data <- filter(results, time != 0, time < 10^11)  %>% group_by(num_vertices, num_edges) %>% summarise_each(funs(mean(.)), -iteration)

p <- ggplot(grouped_data, aes(x=num_vertices, y = time / 10^9))
p <- p + geom_line(size = 1, color = "#4f72fc") + geom_point(size = 2.5, color ="#021f91") 

p <- p + theme_minimal() + xlab("Number of vertices") + ylab("Execution time [sec]")
p <- p + theme(axis.text=element_text(size=12), axis.title=element_text(size=14))
p <- p + scale_x_discrete(limits = grouped_data$num_vertices, expand = 0.05)
p <- p  +  ggtitle(bquote(atop(.("Karger's algorithm with increasing number of edges"), atop(italic(.("Execution time. Number of edges: 4 * num_vertices")), "")))) 

theoretical_results <- data.frame(num_vertices = grouped_data$num_vertices, baseline = 2 / (grouped_data$num_vertices * (grouped_data$num_vertices - 1)))
p <- p + geom_line(data = theoretical_results, size = 1, color = "#ff4d4d", aes(x = num_vertices, y = baseline)) + geom_point(data = theoretical_results, size = 2.5, color ="#800000", aes(x = num_vertices, y = baseline)) 
p


# TEST 2
results <- read.csv("Results/karger_incr_edges_total.csv", header = T, sep = " ")
grouped_data <- filter(results, time != 0, time < 10^11)  %>% group_by(num_vertices, num_edges) %>% summarise_each(funs(mean(.)), -iteration)

p <- ggplot(grouped_data, aes(x=num_edges, y = time / 10^9))
p <- p + geom_line(size = 1, color = "#4f72fc") + geom_point(size = 2.5, color ="#021f91") 

p <- p + theme_minimal() + xlab("Number of edges") + ylab("Execution time [sec]")
p <- p + theme(axis.text=element_text(size=12), axis.title=element_text(size=14))
p <- p + scale_x_discrete(limits = grouped_data$num_edges, expand = 0.05)
p <- p  +  ggtitle(bquote(atop(.("Karger's algorithm with increasing number of edges"), atop(italic(.("Execution time with 50 vertices")), "")))) 

theoretical_results <- data.frame(num_vertices = grouped_data$num_edges, baseline = 2 / (grouped_data$num_vertices * (grouped_data$num_vertices - 1)))
p <- p + geom_line(data = theoretical_results, size = 1, color = "#ff4d4d", aes(x = num_vertices, y = baseline)) + geom_point(data = theoretical_results, size = 2.5, color ="#800000", aes(x = num_vertices, y = baseline)) 
p




