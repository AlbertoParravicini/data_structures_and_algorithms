extern crate rand;
extern crate time;
extern crate petgraph;

use petgraph::Graph;
use petgraph::graph::{NodeIndex, EdgeIndex};

use petgraph::dot::{Dot, Config};
use rand::Rng;
use rand::{thread_rng, sample};

use time::PreciseTime;

fn main() {
    let num_nodes = 1000;
    let num_edges = 4000;

    let num_iterations = 1;

    let mut g = make_random_connected_graph(num_nodes, num_edges);
    println!("{:?}", Dot::with_config(&g, &[Config::EdgeNoLabel]));

    let mut best = num_edges + 1;
    let mut tot_time = time::Duration::seconds(0);
  
    for i in 0..num_iterations {
        let mut g = make_random_connected_graph(num_nodes, num_edges);
        println!("Iteration: {}", i);

        let start = PreciseTime::now();
        let random_min_cut = karger_randomized_min_cut(&mut g);
        let end = PreciseTime::now();
        tot_time = tot_time + start.to(end);

        if random_min_cut < best {
            best = random_min_cut
        }
    }

    
   
    println!("{:?}", Dot::with_config(&g, &[Config::EdgeNoLabel]));
    println!("Random min cut: {}", best);
    println!("Average time per iteration: {:.10}", tot_time / num_iterations);
}

// Build a random undirected connected graph with the specified amount of nodes and edges.
fn make_random_connected_graph(num_nodes: u32, num_edges: u32) -> Graph<u32, (), petgraph::Undirected> {
    if num_edges < num_nodes {
        panic!("It is not possible to create a connected graph with {} nodes and {} edges", num_nodes, num_edges)
    }

    let mut g = Graph::<u32, (), petgraph::Undirected>::new_undirected();
    g.add_node(0);

    for i in 1..num_nodes {
        g.add_node(i);

        let random_node: u32 = rand::thread_rng().gen_range(0, i);
        g.add_edge(NodeIndex::<u32>::new(random_node as usize), NodeIndex::<u32>::new(i as usize), ());
    }
    for _ in num_nodes..(num_edges + 1) {
        let mut rng = thread_rng();
        let random_nodes = sample(&mut rng, 0..(num_nodes), 2);
        g.add_edge(NodeIndex::<u32>::new(random_nodes[0] as usize), NodeIndex::<u32>::new(random_nodes[1] as usize), ());
    }
    g
}

fn make_full_graph(num_nodes: u32) -> Graph<u32, (), petgraph::Undirected> {
    let mut g = Graph::<u32, (), petgraph::Undirected>::new_undirected();
    g.add_node(0);

    for i in 1..num_nodes {
        g.add_node(i);

        for j in 0..i {
            g.add_edge(NodeIndex::<u32>::new(j as usize), NodeIndex::<u32>::new(i as usize), ());
        }      
    }
    g
}

// Contract a specified edge from a given undirected graph.
// Self-loops are deleted, but multi-edges are allowed.
fn contract_edge(g: &mut Graph<u32, (), petgraph::Undirected>, edge: EdgeIndex)  {
    let (node_to_be_kept, node_to_be_removed) = g.edge_endpoints(edge).expect("Invalid endpoints");  
    let neighbours = g.neighbors(node_to_be_removed).collect::<Vec<NodeIndex>>();

    for node_i in neighbours.iter().filter(|&x| *x != node_to_be_kept) {
        g.add_edge(node_to_be_kept, *node_i, ());
    }
    g.remove_node(node_to_be_removed);
}

// Select a random edge from an undirected graph, and return its index.
fn select_random_edge(g: &Graph<u32, (), petgraph::Undirected>) -> EdgeIndex {
    let random_edge_id: u32 = rand::thread_rng().gen_range(0, g.edge_count() as u32);
    EdgeIndex::new(random_edge_id as usize) 
}

// Given an undirected graph, compute the min_cut with Karger's algorithm.
fn karger_randomized_min_cut(g: &mut Graph<u32, (), petgraph::Undirected>) -> u32 {
    for _ in 0..(g.node_count() - 2) {
        let edge_to_be_contracted = select_random_edge(&g);
        contract_edge(g, edge_to_be_contracted);
    }
    g.edge_count() as u32
}