extern crate rand;
extern crate time;
extern crate csv;

use time::PreciseTime;
use csv::Writer;
use rand::Rng;

fn main() {
    // Parameters for the vector;
    let mut vec_size: i32 = 10000;
    let mut vec:Vec<i32> = (0..vec_size).collect();
    let rank = 1000;
    // Total number of comparisons;
    let mut tot_comp = 0;

    // Parameters for profiling;
    let num_iterations: u32 = 1000;
    let mut start = PreciseTime::now();
    let mut end = PreciseTime::now();
    let mut tot_time = time::Duration::seconds(0);
    // Keep the result just for debugging;
    let mut result = -1;
    
    for _ in 0..num_iterations {
        start = PreciseTime::now();
        let (temp_result, num_of_comparisons) = quickselect(&mut vec, 0, vec_size - 1, 1000, 0);
        end = PreciseTime::now();

        tot_comp += num_of_comparisons;
        tot_time = tot_time + start.to(end);
        result = temp_result;
    }
    
    println!("Average time per iteration: {:.10}", tot_time / num_iterations as i32);
    println!("Result: {}, avg_num_of_comparisons: {}", result, tot_comp / num_iterations);
    println!("Theoretical num_of_comparisons {}", theoretical_num_of_comparisons(vec_size, rank))
}

fn quicksort(vec: &mut Vec<i32>, start: i32, end: i32) {
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

fn quickselect(vec: &mut Vec<i32>, start: i32, end: i32, k: i32, num_of_comparisons: u32) -> (i32, u32) {
    let mut num_of_comparisons: u32 = num_of_comparisons;

    if k < start || k > end {
        panic!("INVALID VALUE OF K: {}", k)
    }
    // If just one element is present, return it;
    if start >= end {
        return (vec[end as usize], num_of_comparisons)
    }  
    let pivot_index = rand::thread_rng().gen_range(start, end + 1); 
    // Put the current pivot in its correct place, and return its position;
    let (pivot_index, temp_num_of_comparisons) = partition(vec, start, end, pivot_index);    
    num_of_comparisons += temp_num_of_comparisons;
    
    // Apply the sorting only where the desired element could be, 
    // or return it if it was found;
    if k == pivot_index {
        return (vec[k as usize], num_of_comparisons)
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

fn partition(vec: &mut Vec<i32>, start: i32, end: i32, pivot_index: i32) -> (i32, u32) {
    let pivot_value = vec[pivot_index as usize];
    let mut temp_num_of_comparisons: u32 = 0;

    // Temporarily put the pivot at the end of the vector; 
    vec.swap(pivot_index as usize, end as usize);
    let mut store_index = start;
    for i in start..end {
        temp_num_of_comparisons += 1;
        if vec[i as usize] < pivot_value {
            // If a value lower than the pivot is found, put it in the left part of the vector;
            vec.swap(store_index as usize, i as usize);
            // store_index keeps track of how many values lower that the pivot exist,
            // and where the pivot should be placed at the end;
            store_index += 1;
        }
    }
    // Put the pivot in its correct place;
    vec.swap(end as usize, store_index as usize);

    // Return the sorted position of the pivot and the number of comparisons performed;
    (store_index, temp_num_of_comparisons)
}

// n: size of th input vector;
// k: rank of the item to be found;
fn theoretical_num_of_comparisons(n: i32, k: i32) -> f64 {
    if k > n {
        panic!("k: {} is bigger than n: {}", k, n)
    }
    2. * n as f64 +
        2. * n as f64 * ((n / (n - k)) as f64).ln() +
            2. * k as f64 * (((n - k) / k) as f64).ln()
}
