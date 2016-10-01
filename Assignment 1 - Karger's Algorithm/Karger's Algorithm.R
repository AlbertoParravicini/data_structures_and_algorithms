library(igraph)
library(dplyr)
library(ggplot2)

setwd("C:\\Users\\albyr\\OneDrive\\Documenti\\ULB\\First Year\\Data Structures and Algorithms\\Assigments\\Assignment 1 - Karger's Algorithm")

# Generate a random connected graph with given number of vertices and edges.
make_random_connected_graph <- function(num_vertices = 10, num_edges = 20, details = T) {
  g <- make_empty_graph(directed = F)
  g <- g + vertex("1")
  # Add a new vertex, connect it to a random existing vertex.
  # Repeat the process num_vertices times.
  for(i in 2:num_vertices) {
    random_vertex <- V(g)[sample(1:length(V(g)), 1)]
    g <- g + vertex(as.character(i))
    g <- g + edge(i, random_vertex)
  }
  
  # Add the remaining num_edges - num_vertices edges.
  for(j in 1:(num_edges - num_vertices + 1)) {
    # Select two random, distinct vertices.
    random_vertices <- V(g)[sample(1:length(V(g)), 2, replace = F)]
    g <- g + edge(random_vertices[1], random_vertices[2])
  }
  if(details) {
    plot(g)
    print(g)
  }
  return(g)
}

# Given a graph, compute the min_cut with Karger's algorithm.
# "plot_graphs" and "plot_intermediate_graphs" control the verbosity of the output, 
# and are used for debugging
karger_random_min_cut <- function(g, plot_graphs = T, plot_intermediate_graphs = F) {
  if(plot_graphs) {
    plot(g)
    print(g)
  }
  
  num_vertices = length(V(g))
  
  for(i in 1:(num_vertices - 2)) {
    # Select a random edge, and keep its endpoints.
    random_edge <- E(g)[sample(1:length(E(g)), 1)]
    from_vertex <- ends(g, random_edge)[[1]]
    to_vertex <- ends(g, random_edge)[[2]]
    
    # Contract the selected edge.
    edges_to_be_changed <- neighbors(g, to_vertex)
    for (j in 1:length(edges_to_be_changed)) {
      g <- g + edge(from_vertex, V(g)[edges_to_be_changed[j]]$name)
    }
    g <- delete.vertices(g, to_vertex)
    g <- simplify(g, remove.multiple = F, remove.loops = T)
    
    if (plot_intermediate_graphs) {
      plot(g)
    }
  }
  if(plot_graphs) {
    plot(g)
    print(g)
  }
  # Return the number of edges, as our randomized min_cut
  return(length(E(g)))
}

