extern crate rand;
extern crate time;
extern crate csv;

use time::PreciseTime;
use csv::Writer;
use rand::Rng;
use std::path::Path;

fn main() {
    // Parameters for the vector;
    let mut vec_size: usize = 10000;
    let mut vec:Vec<usize> = (0..vec_size).collect();
    let rank = 1000;
    // Total number of comparisons;
    let mut tot_comp = 0;

    // Parameters for profiling;
    let num_iterations: u32 = 100;
    let mut start = PreciseTime::now();
    let mut end = PreciseTime::now();
    let mut tot_time = time::Duration::seconds(0);
    // Keep the result just for debugging;
    let mut result = 0;

    // Write the results in a file 
    let filename = String::from(format!("Results/increasing_n_{}.csv", time::now().tm_nsec));
    let path = Path::new(&filename);
    println!("{:?}", format!("Results/increasing_n_{}.csv", time::now().tm_nsec));
    let mut writer = Writer::from_file(&path).expect("Couldn't create writer");
     
    for i in 0..num_iterations {
        start = PreciseTime::now();
        let (temp_result, num_of_comparisons) = quickselect(&mut vec, 0, vec_size - 1, 1000, 0);
        end = PreciseTime::now();

        tot_comp += num_of_comparisons;
        tot_time = tot_time + start.to(end);
        result = temp_result;
        let row = (i + 1, vec_size, rank, num_of_comparisons, start.to(end).num_microseconds());
        writer.encode(row).ok().expect("CSV Writer Error");
    }
    
    println!("Average time per iteration: {:.10}, Total time: {:.10}", tot_time / num_iterations as i32, tot_time);
    println!("Result: {}, avg_num_of_comparisons: {}", result, tot_comp / num_iterations);
    println!("Theoretical num_of_comparisons {}", theoretical_num_of_comparisons(vec_size, rank))
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
    if k > n {
        panic!("k: {} is bigger than n: {}", k, n)
    }
    2. * n as f64 +
        2. * n as f64 * ((n / (n - k)) as f64).ln() +
            2. * k as f64 * (((n - k) / k) as f64).ln()
}
