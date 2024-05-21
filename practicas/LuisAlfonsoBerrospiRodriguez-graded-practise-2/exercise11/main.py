import numpy as np

def areaOfConvexPolygon(points):
    determinant = 0
    for i in range(len(points)):
        determinant += points[i][0]*points[(i+1)%len(points)][1] - points[i][1]*points[(i+1)%len(points)][0]
    return 0.5*abs(determinant)

#https://www.mathwords.com/a/area_convex_polygon.htm
#Assume that the polygon is given by the points (x1, y1), (x2, y2), ..., (xn, yn) in counterclockwise order.
print(areaOfConvexPolygon([(-4,3), (2,5), (5,1)]))