extern crate rand;
extern crate time;
extern crate csv;

use time::PreciseTime;
use csv::Writer;
use rand::Rng;
use std::path::Path;

fn main() {
    // Choose what test to perform;
    let profile_size = false;
    let profile_rank = true;

    // PROFILE_SIZE: Parameters for the vector;
    let min_vec_size: usize = 10000;
    let max_vec_size: usize = 1000000;
    let size_step: usize = 10000;

    // PROFILE_RANK: Parameters for the vector;
    let vector_size = 100000;
    let min_rank = 0;
    let max_rank = vector_size - 1;
    // step should be a divisor of max_rank;
    let rank_step = 123;

    // General parameters for profiling;
    let num_iterations: u32 = 1000;
    let mut start = PreciseTime::now();
    let mut end = PreciseTime::now();
    let mut tot_time = time::Duration::seconds(0);
    // Keep the result just for debugging;
    let mut result = 0;

    // Write the results in a file;
    let mut filename = String::new();
    if profile_size {
        filename = String::from(format!("Results/increasing_n_{}.csv", time::now().tm_nsec));
    }
    else if profile_rank {
        filename = String::from(format!("Results/increasing_rank_{}.csv", time::now().tm_nsec));
    }
    else {
        panic!("NO PROFILING OPTION SELECTED!")
    }
    let path = Path::new(&filename);
    let mut writer = Writer::from_file(&path).expect("Couldn't create writer");
     
    let header = ("iteration_number", "vector_size", "rank", "num_of_comparisons", "th_num_of_comparisons", "time [usec]");
    writer.encode(header).ok().expect("CSV Writer Error");

    // Profile quickselect on vectors of increasing size;
    if profile_size {
        let mut vec_size_i: usize = min_vec_size;
        while vec_size_i <= max_vec_size {
            // Build a vector;
            let mut vec:Vec<usize> = (0..vec_size_i).collect();
            // Look for the median (+1, as the vector size is even);
            let rank_i = vec_size_i / 2;
            // Total number of comparisons;
            let mut tot_comp = 0;

            println!("\nWorking on a vector of size: {}\n", vec_size_i);
            let th_num_of_comparisons = theoretical_num_of_comparisons(vec_size_i, rank_i + 1);
            for iteration_i in 0..num_iterations {
                start = PreciseTime::now();
                let (temp_result, num_of_comparisons) = quickselect(&mut vec, 0, vec_size_i - 1, rank_i, 0);
                end = PreciseTime::now();

                tot_comp += num_of_comparisons;
                tot_time = tot_time + start.to(end);
                result = temp_result;
                let row = (iteration_i + 1, vec_size_i, rank_i, num_of_comparisons, th_num_of_comparisons, start.to(end).num_microseconds());
                writer.encode(row).ok().expect("CSV Writer Error");
            }      
            println!("Average time per iteration: {:.10}, Total time: {:.10}", tot_time / num_iterations as i32, tot_time);
            println!("Result: {}, avg_num_of_comparisons: {}", result, tot_comp / num_iterations);
            println!("Theoretical num_of_comparisons {}", th_num_of_comparisons);

            // Go to the next vector;
            vec_size_i += size_step;
        }    
    }
    
    // Profile quickselect on increasing values of rank.
    if profile_rank {
        // Build a vector;
        let mut vec:Vec<usize> = (0..vector_size).collect();
        let mut rank_i: usize = min_rank;  
        while rank_i <= max_rank {
            // Total number of comparisons;
            let mut tot_comp = 0;

            println!("\nLooking for an element of rank: {}\n", rank_i);
            let th_num_of_comparisons = theoretical_num_of_comparisons(vector_size, rank_i + 1);
            for iteration_i in 0..num_iterations {
                start = PreciseTime::now();
                let (temp_result, num_of_comparisons) = quickselect(&mut vec, 0, vector_size - 1, rank_i, 0);
                end = PreciseTime::now();

                tot_comp += num_of_comparisons;
                tot_time = tot_time + start.to(end);
                result = temp_result;
                let row = (iteration_i + 1, vector_size, rank_i, num_of_comparisons, th_num_of_comparisons, start.to(end).num_microseconds());
                writer.encode(row).ok().expect("CSV Writer Error");
            }      
            println!("Average time per iteration: {:.10}, Total time: {:.10}", tot_time / num_iterations as i32, tot_time);
            println!("Result: {}, avg_num_of_comparisons: {}", result, tot_comp / num_iterations);
            println!("Theoretical num_of_comparisons {}", th_num_of_comparisons);

            // Go to the next rank;
            rank_i += rank_step;
        }    
    }
}

fn quicksort(vec: &mut Vec<usize>, start: usize, end: usize) {
        if start >= end {
            return
        }  
        let pivot_index = rand::thread_rng().gen_range(start, end + 1); 
        // Put the current pivot in its correct place, and return its position;
        let (pivot_index, _) = partition(vec, start, end, pivot_index);    
        // Recursively sort the left and right portions of the vector;
        quicksort(vec, start, pivot_index);
        quicksort(vec, pivot_index + 1, end);     
}

fn quickselect(vec: &mut Vec<usize>, start: usize, end: usize, k: usize, num_of_comparisons: u32) -> (usize, u32) {
    let mut num_of_comparisons: u32 = num_of_comparisons;

    if k < start || k > end {
        panic!("INVALID VALUE OF K: {}", k)
    }
    // If just one element is present, return it;
    if start >= end {
        return (vec[end], num_of_comparisons)
    }  
    let pivot_index = rand::thread_rng().gen_range(start, end + 1); 
    // Put the current pivot in its correct place, and return its position;
    let (pivot_index, temp_num_of_comparisons) = partition(vec, start, end, pivot_index);    
    num_of_comparisons += temp_num_of_comparisons;
    
    // Apply the sorting only where the desired element could be, 
    // or return it if it was found;
    if k == pivot_index {
        return (vec[k], num_of_comparisons)
    }
    else if k < pivot_index {
        let result = quickselect(vec, start, pivot_index, k, num_of_comparisons);
        return result
    }
    else {
        let result = quickselect(vec, pivot_index + 1, end, k, num_of_comparisons);
        return result
    }   
}

fn partition(vec: &mut Vec<usize>, start: usize, end: usize, pivot_index: usize) -> (usize, u32) {
    let pivot_value = vec[pivot_index];
    let mut temp_num_of_comparisons: u32 = 0;

    // Temporarily put the pivot at the end of the vector; 
    vec.swap(pivot_index, end);
    let mut store_index = start;
    for i in start..end {
        temp_num_of_comparisons += 1;
        if vec[i] < pivot_value {
            // If a value lower than the pivot is found, put it in the left part of the vector;
            vec.swap(store_index, i);
            // store_index keeps track of how many values lower that the pivot exist,
            // and where the pivot should be placed at the end;
            store_index += 1;
        }
    }
    // Put the pivot in its correct place;
    vec.swap(end, store_index);

    // Return the sorted position of the pivot and the number of comparisons performed;
    (store_index, temp_num_of_comparisons)
}

// n: size of th input vector;
// k: rank of the item to be found;
fn theoretical_num_of_comparisons(n: usize, k: usize) -> f64 {
    let n: f64 = n as f64;
    let mut k: f64 = k as f64;
    if k > n {
        panic!("k: {} is bigger than n: {}", k, n)
    }
    // The formula is not defined if k == n,
    // but the result is approximately the same as k = 1, i.e ~2*n;
    if k == n {
        k = 1.;
    }
    2. * n +
        2. * n * (n / (n - k)).ln() +
            2. * k * ((n - k) / k).ln()
}
