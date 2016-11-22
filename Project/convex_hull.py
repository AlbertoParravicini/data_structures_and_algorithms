import numpy as np
import scipy.spatial as spatial
import sys
import matplotlib.pyplot as plt


class Point:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point(%.2f, %.2f)" % (self.x, self.y)
    
    def __repr__(self):
        return "Point(%.2f, %.2f)" % (self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        return NotImplemented
    
    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented
    
    def to_array(self):
        return [self.x, self.y]

# Taken from http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(list, size):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(list), size):
        yield list[i:i + size]



###################################
# ORIENTATION DETERMINANT #########
# Test whether the point "r" lies on the left or on the right
# of the line passing for points "p" and "q".
# Based on "http://dccg.upc.edu/people/vera/wp-content/uploads/2013/06/GeoC-OrientationTests.pdf",
# pages 5-6.
def orientation_test(p, q, r):
    determinant = (q.x - p.x) * (r.y - p.y) - (q.y - p.y) * (r.x - p.x)
    # determinant == 0: p, q, r are on the same line
    # determinant > 0: r is on the left of p and q (counter-clockwise turn)
    # determinant < 0: r is on the right of p and q (clockwise turn)
    #console.log "det:", determinant, "\n"
    return determinant

#Default comparator used in binary search.
def default_comparator(points, value, middle):
    if points[middle] < value:
        return 1
    elif points[middle] > value:
        return -1
    else:
         return 0
# Comparator used in binary search to test the point inclusion in a convex polygon.
def inclusion_comparator(points, query_point, middle):
    p_0 = points[0]
    o_1 = orientation_test(p_0, points[middle], query_point)
    o_2 = orientation_test(p_0, points[middle + 1], query_point)
    if o_1 >= 0 and o_2 >= 0:
        return 1
    elif (o_1 <= 0 and o_2 <= 0) or (o_1 <= 0 and o_2 >= 0):
        return -1
    else:
        return 0

# Generic implementation of binary search. 
# It returns the position of the found element, or False if not found. 
def binary_search(points, value, comparator=default_comparator):
    
    start = 0
    stop = len(points) - 1
    while start < stop:
        middle = (start + stop) // 2
        if comparator(points, value, middle) > 0:
            start = middle + 1
        elif comparator(points, value, middle) < 0:
            stop = middle
        else:
             return middle
    return False

##################################
# POINT INCLUSION IN HULL #########
###################################

# Find if a given point is inside a convex polygon.
# Note that the input list of points must be convex,
# and must be radially sorted counter-clockwise, 
# starting from the point with smallest x
def inclusion_in_hull(points, query_point):
  # pick the first point p0 of the hull as reference
  # pick the start and stop indexes
  # pick the middle index 
  # if  p0-q-middle is left and p0-q-middle+1 is right, stop
  # if both are left, q is below:
  #   stop = middle - 1,
  #   middle = ...
  # else q is above
  middle = binary_search(points, query_point, inclusion_comparator)
  return orientation_test(points[middle], points[middle + 1], query_point) > 0 if middle else False










###################################
# FIND TANGENTS TO A POLYGON, LINEAR TIME
###################################
# Find the bottom tangent of a point to a given convex polygon.
# Note that the input list of points must be convex,
# and must be radially sorted counter-clockwise, 
# starting from the point with biggest x.
# Works in linear time, inspired by "http://geomalgorithms.com/a15-_tangents.html"
def find_tangent_bottom(query_point, points):
    pass




# Test the tangents
# print("TESTING TANGENTS")
# points_matrix = np.reshape([p.to_array() for p in points], [-1, 2])
# hull = points_matrix[spatial.ConvexHull(points_matrix).vertices]

# query_point = Point(0.0, 0.0)
# plt.plot(query_point.x, query_point.y, 'ro')

# plt.plot(hull[:, 0], hull[:, 1], color='#6699cc', alpha=0.7,
#     linewidth=3, solid_capstyle='round', zorder=2)
# plt.axis([0, 1, 0, 1])

# plt.show()




def hull_2d(points, m, H):
    # Partition the points in groups of size at most m.
    points_in_groups = list(chunks(points, m))
    
    temp_hulls = []
    hulls = []
    # Compute the convex hull of each group, and store its vertices in ccw order.
    for group_i in points_in_groups:
        array_points = np.reshape([p.to_array() for p in group_i], [-1, 2])
       
        hull = array_points[spatial.ConvexHull(array_points).vertices]
        temp_hulls.append(hull)

    # TEMPORARY: rebuild points
    for hull in temp_hulls:
        temp_hull = []
        for p in hull:
            temp_hull.append(Point(p[0], p[1]))
        hulls.append(temp_hull)

    p_0 = Point(0, MIN_VALUE)
    # Rigthmost point of the list
    p_1 = max(points, key=lambda p: p.x)

    for k in range(0, H):
        for i in range(1, np.ceil(len(points) / m)):
            # Find the bottom tangent to from p_k-1, p_k to a point q_i in hull_i
            pass


    return hulls
  


# print("\n\nFOUND HULLS\n") 
# import matplotlib.pyplot as plt
# for hull in hulls:
#     plt.plot(hull[:,0], hull[:,1], 'b', lw=2)
#     print(hull)
# plt.show()

# import numpy as np
# from scipy.spatial import ConvexHull

# points = np.random.rand(30, 2)
# hull = ConvexHull(points)
# plt.plot(points[:,0], points[:,1], 'o')
# for simplex in hull.simplices:
#     plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
# plt.plot(points[hull.vertices,0], points[hull.vertices,1], 'r--', lw=2)
# plt.plot(points[hull.vertices[0],0], points[hull.vertices[0],1], 'ro')
# #plt.show()
# print(points[hull.vertices])
