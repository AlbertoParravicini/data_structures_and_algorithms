import numpy as np
import scipy.spatial as spatial
import sys
import matplotlib.pyplot as plt

MIN_VALUE = -1000000

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

def squared_distance(a, b):
  return (a.x - b.x) ** 2 + (a.y - b.y) ** 2

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
def find_tangent_bottom(points, query_point):
    if inclusion_in_hull(points, query_point):
        return False
    
    tan_b = points[0]
    tan_index = 0
    for i in range(1, len(points)):
        e_prev = orientation_test(points[i - 1], points[i], query_point) >= 0
        e_next = orientation_test(points[i], points[(i + 1) % len(points)], query_point)
        if e_prev == 0:
            tan_b = points[i - 1]
            tan_index = i - 1
        elif e_next == 0:
            tan_b = points[(i + 1) % len(points)]
            tan_index = (i + 1) % len(points)
        elif e_prev < 0 and e_next >= 0:
            tan_b = points[i]
            tan_index = i
    return {"tan_point": tan_b, "tan_index": tan_index}



def hull_2d_step(points, m, H):
    # Partition the points in groups of size at most m.
    points_in_groups = list(chunks(points, m))
    
    temp_hulls = []
    hulls = []

    final_hull = []

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
    
    final_hull.append(Point(0, MIN_VALUE))
    # Rigthmost point of the list
    final_hull.append(Point(MIN_VALUE, MIN_VALUE))
    # Find the next point, ccw, belonging to the hull of p_1
    p_k = Point(MIN_VALUE, MIN_VALUE)

    # Hull index of the last point added to the final hull,
    # and during the loop of the hull that is a candidate for containing the next point of the final hull.
    current_hull_number = -1
    # Position of the last point added to the final hull, 
    # inside its partial hull
    pos_in_last_hull = -1

    # Hull number of the last point inserted, updated after inserting a new point in the final hull.
    old_hull = -1

    for hull_index, hull_i in enumerate(hulls):
        for i in range(0, len(hull_i)):
            if hull_i[i].x > final_hull[1].x:
                final_hull[1] = hull_i[i]
                current_hull_number = hull_index 
                pos_in_last_hull = i

    # Find the next point, ccw, belonging to the hull of p_1


    for k in range(0, H):
        p_k = hulls[current_hull_number][(pos_in_last_hull + 1) % len(hulls[current_hull_number])]
        old_hull = current_hull_number
        # compute the next point in the hull of hull[-1]
        # also store the index of that hull
        for hull_index, hull_i in enumerate(hulls):
            # Find the bottom tangent to from p_k-1, p_k to a point q_i in hull_i
            if hull_index != current_hull_number:
                temp_p = find_tangent_bottom(hull_i, final_hull[-1])
                if temp_p:
                    temp_tan = temp_p["tan_point"]
                    temp_tan_index = temp_p["tan_index"]

                    # Test if the tangent point lies on the left of the segment hull[-1], p_k:
                    # If so, the angle given by the tangent point is bigger, and we have a new candidate.
                    o = orientation_test(final_hull[-1], temp_tan, p_k)

                    # If angle (hull[-2], hull[-1], temp_p) > angle(hull[-2], hull[-1], p_k)
                    if o > 0:
                        p_k = temp_tan
                        current_hull_number = hull_index
                        pos_in_last_hull = temp_tan_index                  
        if old_hull == current_hull_number:
            pos_in_last_hull = (pos_in_last_hull + 1) % len(hulls[current_hull_number])
        if p_k == final_hull[1]:
            return final_hull[1:]
        final_hull.append(p_k)
    
    return False
  

def hull_2d(points):
    t = 1
    while True:
        H = min(2**2**t, len(points))
        hull = hull_2d_step(points, H, H)
        if hull:
            return hull
        t += 1
