import numpy as np
import scipy.spatial as spatial
import sys
import matplotlib.pyplot as plt
import functools

MIN_VALUE = -1000000


class Point:
    def __init__(self, x=0, y=0):
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
    return (a.x - b.x)**2 + (a.y - b.y)**2


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


###################################
# BINARY SEARCH  ##################
###################################


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
    o_2 = orientation_test(p_0, points[(middle + 1) % len(points)],
                           query_point)
    if o_1 >= 0 and o_2 >= 0:
        return 1
    elif (o_1 <= 0 and o_2 <= 0) or (o_1 <= 0 and o_2 >= 0):
        return -1
    else:
        return 0


# Comparator used by find_intersecting_edge        
def intersection_comparator(points, query_point, middle):
    p_0 = points[0]
    o_1 = orientation_test(query_point, p_0, points[middle])
    o_2 = orientation_test(query_point, p_0, points[(middle + 1) %
                                                    len(points)])

    if (query_point.x <= p_0.x):
        if o_1 >= 0 and o_2 >= 0:
            return -1
        elif o_2 <= 0:
            return 1
        else:
            return 0
    else:
        if o_1 >= 0 and o_2 >= 0:
            return 1
        elif o_1 <= 0:
            return -1
        else:
            return 0


# Comparator used by the binary search to find the bottom tangent.
def bot_tangent_comparator(points, query_point, middle):
    o_1 = orientation_test(query_point, points[(middle - 1) % len(points)],
                           points[middle])
    o_2 = orientation_test(query_point, points[middle], points[(middle + 1) %
                                                               len(points)])

    if o_1 * o_2 <= 0:
        return 0
    elif o_1 <= 0 and o_2 <= 0:
        return 1 
    else:
        return -1 


# Generic implementation of binary search. 
# It returns the position of the found element, or False if not found. 
def binary_search(points, value, comparator=default_comparator, force_return = False, start = 0, stop = None):
    if stop == None:
        stop = len(points) - 1
    while start < stop:
        middle = (start + stop) // 2
        res = comparator(points, value, middle)
        if res > 0:
            start = middle + 1
        elif res < 0:
            stop = middle
        else:
            return middle
    return False if not force_return else (start + stop) // 2


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
    return orientation_test(points[middle], points[middle + 1],
                            query_point) > 0 if middle else False


# Given a convex polygon and an external point, find the edge of the polygon that intersect the line 
# given by the external point and the leftmost point of the polygon.
def find_intersecting_edge(points, query_point):
    if inclusion_in_hull(points, query_point):
        return False

    middle = binary_search(points, query_point, intersection_comparator)
    if middle:
        return middle
    elif query_point.y < points[0].y:
        return len(points) - 1
    else:
        return 0


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
        e_prev = orientation_test(points[i - 1], points[i], query_point)
        e_next = orientation_test(points[i], points[(i + 1) % len(points)],
                                  query_point)
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


###################################
# FIND TANGENTS TO A POLYGON, BINARY SEARCH
###################################
# Find the tangents of a point to a given convex polygon.
# Note that the input list of points must be convex,
# and must be radially sorted counter-clockwise, 
# starting from the point with smallest x.
def find_tangent_bin_search(points, query_point):
    if inclusion_in_hull(points, query_point):
        return False

    tan_index = 0
    # Find where to split the polygon.
    stop_bottom = find_intersecting_edge(points, query_point)

    if orientation_test(query_point, points[0], points[stop_bottom]) >= 0 and \
        orientation_test(query_point, points[0], points[(stop_bottom + 1) % len(points)]) <= 0:
            tan_index = binary_search(points, query_point,
                              bot_tangent_comparator, True, start = stop_bottom)
    else:
        tan_index = binary_search(points, query_point,
                              bot_tangent_comparator, True, stop = stop_bottom + 1)

    
    if not tan_index:
        tan_index = 0
    return {"tan_point": points[tan_index], "tan_index": tan_index}


###################################
# RADIAL SORT #####################
###################################
# Sort clockwise (or counter-clockwise) a list of points w.r.t. a given anchor point.
# If the points, translated w.r.t. the anchor, span multiple quadrants of the plane,
# they are sorted by taking the positive x semi-axis as starting point.
# Inspired by "http://stackoverflow.com/questions/6989100/sort-points-in-clockwise-order"
def radial_sort(points, anchor = Point(0., 0.), cw = True):
    def cmp(a, b):
        if a.x - anchor.x == 0 and a.y - anchor.y == 0 and b.x - anchor.x != 0 and b.y - anchor.y != 0:
            return -1
        if a.x - anchor.x != 0 and a.y - anchor.y != 0 and b.x - anchor.x == 0 and b.y - anchor.y == 0:
            return 1
        if a.x - anchor.x >= 0 and b.x - anchor.x < 0:
            return  -1
        if a.x - anchor.x < 0 and b.x - anchor.x >= 0:
            return  1
        if a.x - anchor.x == 0 and b.x - anchor.x == 0:
            if a.y - anchor.y < 0 and b.y - anchor.y < 0:
                return 1 if a.y < b.y else -1
            else:
                return 1 if a.y > b.y else -1
        # Check the position of b wrt the line defined by the anchor and a.
        # b has greater angle than a if it lies on the left of the line.
        orientation = orientation_test(anchor, a, b)
        # if orientation < 0, anchor-a is bigger than anchor-b, as we have a right turn.
        if orientation == 0:
            return 1 if squared_distance(anchor, a) >= squared_distance(anchor, b) else -1
        else: 
            return 1 if orientation > 0 else -1


    if len(points) == 0:
        return []
    
    points.sort(key=functools.cmp_to_key(cmp), reverse = not cw)
    
    return points

###################################
# GRAHAM SCAN #####################
###################################
# Compute the convex hull of the given list of points by using Graham scan
# Inspired by "http://www.geeksforgeeks.org/convex-hull-set-2-graham-scan/"
def convex_hull_graham_scan(input_points):
    # Copy the input points, so that it is possible to modify them
    points = list(input_points)
    convex_hull = []

    # Find the point with the smalles x.
    smallest_x_point_index = 0
    for index, p in enumerate(points):
        if (p.x < points[smallest_x_point_index].x) or \
            ((p.x == points[smallest_x_point_index].x) and (p.y < points[smallest_x_point_index].y)):
            smallest_x_point_index = index

    # Put the point with smallest x at the beginning of the list.
    points[0], points[smallest_x_point_index] = points[
        smallest_x_point_index], points[0]

    # Order the list with respect to the angle that each point forms 
    # with the anchor. Given two points a, b, in the output a is before b
    # if the polar angle of a w.r.t the anchor is bigger than the one of b,
    # in counter-clockwise direction.
    anchor = Point(points[0].x, points[0].y)
    points = [anchor] + radial_sort(points[1:], anchor, cw = False)
    # If more points have the same angle w.r.t. the anchor, keep only the farthest one.
    i = 1
    while i < len(points) and (orientation_test(anchor, points[i], points[(i + 1) % len(points)]) == 0):
        points.pop((i + 1) % len(points))
    
    # If there are fewer than 3 points, it isn't possible to build a convex hull.
    if len(points) < 3:
        raise ValueError("The hull has just ", len(points), ": at least 3 points are needed to build a hull!")
    
    # Add the first 3 points to the convex hull.
    # The first 2 will be for sure part of the hull.
    convex_hull += points[0:3]

    for p in points[3:]:
        # While the i-th point forms a non-left turn with the last 2 elements of the convex hull...
        while orientation_test(convex_hull[-2], convex_hull[-1], p) <= 0:
            # Delete from the convex hull the point that causes a right turn.
            convex_hull.pop()
        # Once no new right turns are found, add the point that gives a left turn.   
        convex_hull.append(p)

    return convex_hull



###################################
# HULL 2D - STEP ##################
###################################
def hull_2d_step(points, m, H):
    # Partition the points in groups of size at most m.
    points_in_groups = list(chunks(points, m))

    temp_hulls = []
    hulls = []

    final_hull = []

    # Compute the convex hull of each group, and store its vertices in ccw order.
    for group_i in points_in_groups:
        hulls.append(convex_hull_graham_scan(group_i))

    # Leftmost point of the list
    final_hull.append(Point(-MIN_VALUE, -MIN_VALUE))
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

    # Find the leftmost point.
    for hull_index, hull_i in enumerate(hulls):
        for i in range(0, len(hull_i)):
            if hull_i[i].x < final_hull[0].x:
                final_hull[0] = hull_i[i]
                current_hull_number = hull_index
                pos_in_last_hull = i

    for k in range(0, H):
        # Compute the next point in the hull of hull[-1],
        # also store the index of that hull
        p_k = hulls[current_hull_number][(pos_in_last_hull + 1) %
                                         len(hulls[current_hull_number])]
        old_hull = current_hull_number

        for hull_index, hull_i in enumerate(hulls):
            # Find the bottom tangent to from p_k-1, p_k to a point q_i in hull_i
            if hull_index != old_hull:
                temp_p = find_tangent_bin_search(hull_i, final_hull[-1])
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
            pos_in_last_hull = (
                pos_in_last_hull + 1) % len(hulls[current_hull_number])
        if p_k == final_hull[0]:
            return final_hull
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
