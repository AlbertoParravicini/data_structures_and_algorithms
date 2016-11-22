import numpy as np
import scipy.spatial as spatial
import sys
import matplotlib.pyplot as plt
import pprint
from convex_hull import *

def main():
    num_points = 12
    m = 4
    H = 8

    np.random.seed(1900)



    points = []
    # points = [
    #     Point(3, 3),
    #     Point(8, 1),
    #     Point(7, 7),
    #     Point(4, 5),
    #     Point(6, 4),
    #     Point(9, 8),
    #     Point(6, 9.1),
    #     Point(5, 9),
    #     Point(11, 4),
    #     Point(13, 9),
    #     Point(12, 8),
    #     Point(9, 12)
    # ]

    for i in range(0, num_points):
        points.append(Point(np.floor(np.random.rand() * 15), np.floor(np.random.rand() * 15)))
    print("\n\nPOINTS\n")
    print(points, end='\n\n')

    # Test the tangents
    print("TESTING TANGENTS")
    points_matrix = np.reshape([p.to_array() for p in points], [-1, 2])
    temp_hull = points_matrix[spatial.ConvexHull(points_matrix).vertices]

    hull = []
    for p in temp_hull:
        hull.append(Point(p[0], p[1]))

    
    plt.plot(points_matrix[:, 0], points_matrix[:, 1], "o")
    plt.plot(temp_hull[:, 0], temp_hull[:, 1], color='#6699cc', alpha=0.7,
        linewidth=3, solid_capstyle='round', zorder=2)
    plt.axis([0, 18, 0, 18])

    #plt.show()
    print("\n\nHULL FIGO:\n")
    print(hull_2d(points))
    print("\n\nHULL CORRETTO:\n")
    print(temp_hull)


main()