import matplotlib.pyplot as plt
import os
import numpy as np

FOLDER = 'exercise11'

def point_line_distance(point, start, end):

    if start == end:
        # Line is a point
        return np.linalg.norm(np.array(point) - np.array(start))
    
    line_length = np.linalg.norm(np.array(end) - np.array(start))
    if line_length == 0:
        return np.linalg.norm(np.array(point) - np.array(start))
    
    u = ((point[0] - start[0]) * (end[0] - start[0]) + (point[1] - start[1]) * (end[1] - start[1])) / (line_length ** 2)
    if u < 0:
        # Closest point is the start
        return np.linalg.norm(np.array(point) - np.array(start))
    elif u > 1:
        # Closest point is the end
        return np.linalg.norm(np.array(point) - np.array(end))
    else:
        # Closest point is on the line
        intersection_x = start[0] + u * (end[0] - start[0])
        intersection_y = start[1] + u * (end[1] - start[1])
        return np.linalg.norm(np.array(point) - np.array([intersection_x, intersection_y]))

def douglas_peucker(points, tolerance):

    if len(points) <= 2:
        return points
    
    # Find the point with the maximum distance
    max_distance = 0
    index = 0
    for i in range(1, len(points) - 1):
        distance = point_line_distance(points[i], points[0], points[-1])
        if distance > max_distance:
            index = i
            max_distance = distance
    
    # If max distance is greater than tolerance, recursively simplify
    if max_distance > tolerance:
        left_part = douglas_peucker(points[:index+1], tolerance)
        right_part = douglas_peucker(points[index:], tolerance)
        return left_part[:-1] + right_part
    else:
        return [points[0], points[-1]]



    
with open(os.path.join(FOLDER, "points.txt") , 'r') as f:
    points = eval(f.read())
    
fig, ax = plt.subplots(3, 2, figsize=(5, 10))
ax[0,0].plot([p[0] for p in points], [p[1] for p in points], 'r-')
ax[0,0].set_title('Original')
N = 6

for i in range(0, N):
    threshold = i / 10
    simplified = douglas_peucker(points, threshold)
    ax[i//2, i%2].plot([p[0] for p in simplified], [p[1] for p in simplified], 'b-')
    ax[i//2, i%2].set_title(f'Tolerance: {threshold}')
    
plt.show()