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
    filename = "Results/increasing_n_GS" + time.strftime("%Y_%m_%d_%H_%M_%S.csv")

    with open(filename, "a") as results:
        results.write("iteration_number, input_size, hull_size, time[sec]\n")

    min_size = 10000
    max_size = 210000
    increment = 10000

    repetitions = 10

    fixed_hull_size = 1000

    radius = 0.5

    center_x = 0.5
    center_y = 0.5

    for r in range(1, repetitions + 1):
        print("\n\nITERATION NUMBER ", r)
        tot_time = 0

        # Generate a list of points. 
        # "fixed_hull_size" points will lie on a circle, and will form a hull of fixed size. 
        # "max_size" - "fixed_hull_size" points will lie strictly inside the circle. 
        # For each sub-iteration of increasing size, only a portion of the internal points is used. 
        points = []
        for i in range(0, fixed_hull_size):
            angle = 2 * np.pi * np.random.rand()
            x = radius * np.cos(angle) + center_x
            y = radius * np.sin(angle) + center_y
            points.append(Point(x,y))
        for i in range(0, max_size - fixed_hull_size):
            angle = 2 * np.pi * np.random.rand()
            r_i = 0.9 * radius * np.random.rand()
            x = r_i * np.cos(angle) + center_x
            y = r_i * np.sin(angle) + center_y
            points.append(Point(x,y))
        
        # TO USE spatial.ConvexHull
        # points_matrix = np.reshape([p.to_array() for p in points], [-1, 2])

        # PLOTTING
        # plt.plot(points_matrix[:, 0], points_matrix[:, 1], "o")
        # plt.show()



        for n in range(min_size, max_size, increment):
            print("\n WORKING WITH VECTOR OF SIZE ", n)
            
            start_time = timeit.default_timer()
            #hull = points_matrix[spatial.ConvexHull(points_matrix[:n, ]).vertices]
            hull = convex_hull_graham_scan(points[:n])
            end_time = timeit.default_timer()
            print("!!! HULL OF SIZE ", len(hull), " -> EXECUTION TIME:", (end_time - start_time), "\n")

            with open(filename, "a") as results:
                results.write(str(r) + ", " + str(n) + ", " + str(len(hull)) + ", " + str(end_time - start_time) + "\n")
            tot_time += end_time - start_time
        print("\n\nTOTAL ITERATION TIME: ", tot_time)

def test_increasing_hull():
    filename = "Results/increasing_hull_" + time.strftime("%Y_%m_%d_%H_%M_%S.csv")

    with open(filename, "a") as results:
        results.write("iteration_number, input_size, hull_size, time[sec]\n")

    min_size = 1000
    max_size = 20000
    increment = 1000

    repetitions = 10

    fixed_size = 40000

    radius = 0.5

    center_x = 0.5
    center_y = 0.5

    for r in range(1, repetitions + 1):
        print("\n\nITERATION NUMBER ", r)
        tot_time = 0

         # Generate a list of points. 
         # "h" points will lie on a circle, and will form a hull of fixed size. 
         # "fixed_size" - "h" points will lie strictly inside the circle. 
        circle_points = []
        points = []
        for i in range(0, max_size):
            angle = 2 * np.pi * np.random.rand()
            x = radius * np.cos(angle) + center_x
            y = radius * np.sin(angle) + center_y
            circle_points.append(Point(x,y))
        for i in range(0, fixed_size - min_size):
            angle = 2 * np.pi * np.random.rand()
            r_i = 0.9 * radius * np.random.rand()
            x = r_i * np.cos(angle) + center_x
            y = r_i * np.sin(angle) + center_y
            points.append(Point(x,y))

        for h in range(min_size, max_size + increment, increment):        

            # TO USE spatial.ConvexHull
            #points_matrix = np.reshape([p.to_array() for p in points], [-1, 2])
            
            # PLOTTING
            # plt.plot(points_matrix[:, 0], points_matrix[:, 1], "o")
            # plt.show()

            print("\n WORKING WITH HULL OF SIZE ", h)
            
            start_time = timeit.default_timer()
            #hull = points_matrix[spatial.ConvexHull(points_matrix).vertices]
            len_points = len(circle_points[:h] + points[:(fixed_size - h)])
            print("NUM POINTS: ", len_points)
            hull = hull_2d(circle_points[:h] + points[:(fixed_size - min_size - h)])
            end_time = timeit.default_timer()
            print("!!! HULL OF SIZE ", len(hull), " -> EXECUTION TIME:", (end_time - start_time), "\n")

            with open(filename, "a") as results:
                results.write(str(r) + ", " + str(len_points) + ", " + str(len(hull)) + ", " + str(end_time - start_time) + "\n")
            tot_time += end_time - start_time
        print("\n\nTOTAL ITERATION TIME: ", tot_time)

def test_increasing_points_hull():
    filename = "Results/increasing_points_hull_" + time.strftime("%Y_%m_%d_%H_%M_%S.csv")

    with open(filename, "a") as results:
        results.write("iteration_number, input_size, hull_size, time[sec]\n")

    min_size = 10000
    max_size = 110000
    increment = 10000

    repetitions = 10

    radius = 0.5

    center_x = 0.5
    center_y = 0.5

    for r in range(1, repetitions + 1):
        print("\n\nITERATION NUMBER ", r)
        tot_time = 0

        # Generate a list of points. 
        # "fixed_hull_size" points will lie on a circle, and will form a hull of fixed size. 
        # "max_size" - "fixed_hull_size" points will lie strictly inside the circle. 
        # For each sub-iteration of increasing size, only a portion of the internal points is used. 
        points = []
        for i in range(0, max_size):
            x = np.random.rand()
            y = np.random.rand()
            points.append(Point(x,y))
        
        # TO USE spatial.ConvexHull
        # points_matrix = np.reshape([p.to_array() for p in points], [-1, 2])

        # PLOTTING
        # plt.plot(points_matrix[:, 0], points_matrix[:, 1], "o")
        # plt.show()

        for n in range(min_size, max_size, increment):
            print("\n WORKING WITH VECTOR OF SIZE ", n)
            
            start_time = timeit.default_timer()
            #hull = points_matrix[spatial.ConvexHull(points_matrix[:n, ]).vertices]
            hull = hull_2d(points[:n])
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
    #     Point(0.0013889274677962571, -0.013555650889113225)
    #     ,Point(-0.0016666666666666668, 0.004385810623020935)
    #     ,Point(0.0008334027792245672, 0.0030711794594722613)
    #     ,Point(0.0016666666666666668, 0.000616710127083022)
    #     ,Point(-0.0014437584577056057, -0.0062082663462808335)
    #     ,Point(-0.009678865108180433, 0.2804668674955018)
    #     ,Point(0.001909352591070292, 0.007336821668514451)
    #     ,Point(-0.003083182977989309, -0.0012405374580908382)
    # ]
    
    # print(convex_hull_graham_scan(points))
main()