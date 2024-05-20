import numpy as np

def point_segment_distance(point, segment):
    # Calculate the distance between a point and a segment
    sign_0 = np.sign(np.dot(segment[1] - segment[0], point - segment[0]))
    sign_1 = np.sign(np.dot(segment[0] - segment[1], point - segment[1]))
    # If the point is on the same side of the segment, return the distance
    if sign_0 == sign_1:
        return abs(np.cross(segment[1] - segment[0], point - segment[0]) / np.linalg.norm(segment[1] - segment[0]))
    else:
        # Otherwise, return the distance to the closest endpoint
        return min(abs(np.linalg.norm(point - segment[0])), abs(np.linalg.norm(point - segment[1])))
    
random_line = np.random.rand(2, 2)
random_point = np.random.rand(2)
print(f"Random line: {random_line}")
print(f"Random point: {random_point}")
print(f"Distance: {point_segment_distance(random_point, random_line)}")