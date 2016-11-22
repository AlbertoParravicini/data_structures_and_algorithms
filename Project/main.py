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

    MIN_VALUE = sys.float_info.min

    points = []

    for i in range(0, num_points):
        points.append(Point(np.random.rand(), np.random.rand()))
    print("\n\nPOINTS\n")
    print(points, end='\n\n')

    points_in_groups = list(chunks(points, m))
    
    print("\n\nPOINTS IN GROUPS\n")
    pprint.pprint(points_in_groups)

    print("\n\nPOINTS AS ARRAYS\n")
    print(list(map(lambda p: p.to_array(), points)))

main()