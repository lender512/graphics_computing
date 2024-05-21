import numpy as np
import matplotlib.pyplot as plt


# Function to find the closest pair of points
def closest_pair(points):
    # Sort the points by x-coordinate
    points = sorted(points, key=lambda x: x[0])
    plt.plot([p[0] for p in points], [p[1] for p in points], 'r.')
    closest_distance = float('inf')
    closest_pair = None

    # Initialize the sweep line at the first point
    sweep_line_x = points[0][0]
    active_set = [points[0]]  # Points intersecting the sweep line
    plt.plot([sweep_line_x, sweep_line_x], [0, 10], 'b--')
    plt.pause(0.1)
    
    

    # Iterate through points
    for i in range(1, len(points)):
        # Update the sweep line position
        sweep_line_x = points[i][0]
        plt.clf()
        plt.plot([p[0] for p in points], [p[1] for p in points], 'r.')
        plt.plot([sweep_line_x, sweep_line_x], [0, 10], 'b--', label='Sweep line')
        #plot the search window in a square around the current point
        plt.plot([points[i][0] - closest_distance, points[i][0] - closest_distance, points[i][0] + closest_distance, points[i][0] + closest_distance, points[i][0] - closest_distance], [points[i][1] - closest_distance, points[i][1] + closest_distance, points[i][1] + closest_distance, points[i][1] - closest_distance, points[i][1] - closest_distance], 'g-')
        if closest_pair:
            plt.plot([closest_pair[0][0], closest_pair[1][0]], [closest_pair[0][1], closest_pair[1][1]], 'b-')
            plt.title(f"Current closest distance: {closest_distance:.4f}")
        plt.pause(0.1)

        # Remove points from the active set if they are outside the current window
        while active_set and points[i][0] - active_set[0][0] > closest_distance:
            active_set.pop(0)

        # Compare each point in the active set with the current point
        for j in range(len(active_set)):
            d = np.linalg.norm(np.array(points[i]) - np.array(active_set[j]))
            if d < closest_distance:
                closest_distance = d
                closest_pair = (points[i], active_set[j])

        # Add the current point to the active set
        active_set.append(points[i])

        # Sort the active set by y-coordinate
        active_set.sort(key=lambda x: x[1])

    return closest_pair, closest_distance

n = 100
points = np.random.rand(n, 2) * 10
closest_pair, distance = closest_pair(points)

plt.show()

print("Closest pair:", closest_pair)
print("Distance:", distance)
