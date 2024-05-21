import matplotlib.pyplot as plt
import os
import numpy as np

FOLDER = 'exercise14'

def calculate_triangle_area(p1, p2, p3):
    """Calculate the area of a triangle formed by three points."""
    return 0.5 * abs((p1[0]*(p2[1]-p3[1]) + p2[0]*(p3[1]-p1[1]) + p3[0]*(p1[1]-p2[1])))

def visvalingam_whyatt(points, num_points_to_keep):
    """Simplify a line using the Visvalingam-Whyatt algorithm."""
    # Calculate the area of each triangle formed by three consecutive points
    areas = [calculate_triangle_area(points[i-1], points[i], points[i+1]) for i in range(1, len(points)-1)]
    # Initialize the list of points to keep
    points_to_keep = points.copy()
    # Remove points iteratively until the desired number of points is reached
    while len(points_to_keep) > num_points_to_keep:
        # Find the index of the point with the smallest triangle area
        min_area_index = np.argmin(areas)
        # Remove the point with the smallest triangle area
        points_to_keep.pop(min_area_index+1)
        # Update the areas list
        if min_area_index > 0:
            areas[min_area_index-1] = calculate_triangle_area(points_to_keep[min_area_index-1], points_to_keep[min_area_index], points_to_keep[(min_area_index+1) % len(points_to_keep)])
        if min_area_index < len(areas):
            areas[min_area_index] = calculate_triangle_area(points_to_keep[min_area_index], points_to_keep[min_area_index+1], points_to_keep[(min_area_index+2) % len(points_to_keep)])
        # Remove the area of the triangle that was removed
        areas.pop(min_area_index)
    return points_to_keep


    
with open(os.path.join(FOLDER, "points.txt") , 'r') as f:
    points = eval(f.read())
    
fig, ax = plt.subplots(3, 1, figsize=(5, 10))
ax[0].plot([p[0] for p in points], [p[1] for p in points], 'r-')
ax[0].set_title('Original')
lst = [100, 10]

for i, keep in enumerate(lst):
    simplified =  visvalingam_whyatt(points, keep)
    ax[i+1].plot([p[0] for p in simplified], [p[1] for p in simplified], 'r-')
    ax[i+1].set_title(f'N = {keep}')
    
plt.show()