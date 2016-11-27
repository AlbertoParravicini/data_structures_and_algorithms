import numpy as np
import scipy.spatial as spatial
import sys
import matplotlib.pyplot as plt
import pprint
from convex_hull import *
import timeit
from inspect import getsource
import time 




def test_increasing_points():
    filename = "Results/increasing_n_" + time.strftime("%Y_%m_%d_%H_%M_%S.csv")

    with open(filename, "a") as results:
        results.write("iteration_number, input_size, hull_size, time[sec]\n")

    min_size = 10000
    max_size = 400000
    increment = 20000

    repetitions = 1

    fixed_hull_size = 100

    radius = 0.5

    center_x = 0.5
    center_y = 0.5

    for r in range(0, repetitions):
        print("\n\nITERATION NUMBER ", r)
        tot_time = 0
        for n in range(min_size, max_size, increment):
            print("\n WORKING WITH VECTOR OF SIZE ", n)
            points = []
            for i in range(0, fixed_hull_size):
                angle = 2 * np.pi * np.random.rand()
                x = r * np.cos(angle) + center_x
                y = r * np.sin(angle) + center_y
                points.append(Point(x,y))
            for i in range(0, n - fixed_hull_size):
                angle = 2 * np.pi * np.random.rand()
                r = radius * np.random.rand()
                x = r * np.cos(angle) + center_x
                y = r * np.sin(angle) + center_y
                points.append(Point(x,y))
        
            # TO USE spatial.ConvexHull
            #points_matrix = np.reshape([p.to_array() for p in points], [-1, 2])

            start_time = timeit.default_timer()
            #hull = points_matrix[spatial.ConvexHull(points_matrix).vertices]
            hull = convex_hull_graham_scan(points)
            end_time = timeit.default_timer()
            print("!!! HULL OF SIZE ", len(hull), " -> EXECUTION TIME:", (end_time - start_time), "\n")

            with open(filename, "a") as results:
                results.write(str(r) + ", " + str(n) + ", " + str(len(hull)) + ", " + str(end_time - start_time) + "\n")
            tot_time += end_time - start_time
        print("\n\nTOTAL ITERATION TIME: ", tot_time)

def main():
    test_increasing_points()
    
    # num_points = 1200
    # #np.random.seed(47516)
    # seed = int(np.floor(np.random.rand() * 100000))
    # print("\n\nSEED: ", seed, "\n\n")
    # np.random.seed(seed)

    # points = []
    # for i in range(0, num_points):
    #     #points.append(Point(np.floor((np.random.rand() * 20)), np.floor((np.random.rand() * 20))))
    #     points.append(Point((np.random.rand() * 200000), (np.random.rand() * 200000)))
    # print("\n\nPOINTS\n")
    # #pprint.pprint(points)

   
    # points_matrix = np.reshape([p.to_array() for p in points], [-1, 2])
    # temp_hull = points_matrix[spatial.ConvexHull(points_matrix).vertices]

    # hull = []
    # for p in temp_hull:
    #     hull.append(Point(p[0], p[1]))

    
    # plt.plot(points_matrix[:, 0], points_matrix[:, 1], "o")
    # plt.plot(temp_hull[:, 0], temp_hull[:, 1], color='#6699cc', alpha=0.7,
    #     linewidth=3, solid_capstyle='round', zorder=2)
    # plt.axis([0, 22, 0, 22])

    # #plt.show()
    # print("\n\nGRAHAM SCAN\n")
    # measure_time(lambda: convex_hull_graham_scan(points))
   
    # print("\n\nHULL FIGO:\n")
    # measure_time(lambda: hull_2d(points))
    
    # print("\n\nHULL CORRETTO:\n")
    # measure_time(lambda: spatial.ConvexHull(points_matrix))
    # print(len(temp_hull))


    # points = [     
    #     Point(1.66, 15.76),
    #     Point(17.93, 4.27),
    #      Point(9.44, 19.60),
    #     Point(5.26, 19.20)
    # ]
    # query_point = Point(19.94, 6.89)
    # print(find_tangent_bin_search(points, query_point))
main()