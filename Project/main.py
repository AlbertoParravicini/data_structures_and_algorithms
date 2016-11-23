import numpy as np
import scipy.spatial as spatial
import sys
import matplotlib.pyplot as plt
import pprint
from convex_hull import *

def main():
    num_points = 12
    #np.random.seed(47516)
    seed = int(np.floor(np.random.rand() * 100000))
    print("\n\nSEED: ", seed, "\n\n")
    np.random.seed(seed)

    points = []
    for i in range(0, num_points):
        #points.append(Point(np.floor((np.random.rand() * 20)), np.floor((np.random.rand() * 20))))
        points.append(Point((np.random.rand() * 20), (np.random.rand() * 20)))
    print("\n\nPOINTS\n")
    pprint.pprint(points)

   
    points_matrix = np.reshape([p.to_array() for p in points], [-1, 2])
    temp_hull = points_matrix[spatial.ConvexHull(points_matrix).vertices]

    hull = []
    for p in temp_hull:
        hull.append(Point(p[0], p[1]))

    
    plt.plot(points_matrix[:, 0], points_matrix[:, 1], "o")
    plt.plot(temp_hull[:, 0], temp_hull[:, 1], color='#6699cc', alpha=0.7,
        linewidth=3, solid_capstyle='round', zorder=2)
    plt.axis([0, 22, 0, 22])

    #plt.show()
    print("\n\nGRAHAM SCAN\n")
    pprint.pprint(convex_hull_graham_scan(points))
    print("LEN:", len(convex_hull_graham_scan(points)))
    print("\n\nHULL FIGO:\n")
    pprint.pprint((hull_2d(points)))
    print("LEN:", len(hull_2d(points)))
    print("\n\nHULL CORRETTO:\n")
    print((temp_hull))
    print(len(temp_hull))


    # points = [     
    #     Point(1.66, 15.76),
    #     Point(17.93, 4.27),
    #      Point(9.44, 19.60),
    #     Point(5.26, 19.20)
    # ]
    # query_point = Point(19.94, 6.89)
    # print(find_tangent_bin_search(points, query_point))
main()