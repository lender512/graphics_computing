import numpy as np
import pandas as pd
import os

FOLDER = "exercise05"

def pointIsinPolygon(polygon, point):
    n = len(polygon)
    p1x = polygon[0][0] 
    p1y = polygon[0][1]
    inside = False
    
    # Ray casting algorithm
    for i in range(n+1):
        p2x = polygon[i % n][0]
        p2y = polygon[i % n][1]
        # Check if the point is below the upper bound of the segment
        if point[1] > min(p1y, p2y):
            if point[1] <= max(p1y, p2y):
                if point[0] <= max(p1x, p2x):
                    if p1y != p2y:
                        # Calculate the intersection of the ray with the segment
                        xinters = (point[1] - p1y) * \
                            (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or point[0] <= xinters:
                        #negate the inside variable
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


test_df = pd.read_csv(os.path.join(FOLDER, "test.csv"))

success = 0

for i in range(len(test_df)):
    point = eval(test_df.loc[i, "point"])
    polygon = eval(test_df.loc[i, "polygon"])
    is_in_polygon = pointIsinPolygon(polygon, point)
    if is_in_polygon == test_df.loc[i, "is_in_polygon"]:
        success += 1

print(f"Accuracy: {success/len(test_df):.2%}")


N = 1000
max_p = 100

polygons = np.random.randint(0, max_p, (N, 3, 2))
points = np.random.randint(0, max_p, (N, 2))

df = pd.DataFrame()

for i in range(N):
    point = points[i]
    polygon = polygons[i]
    is_in_polygon = pointIsinPolygon(polygon, point)
    row = [str(point.tolist()), str(polygon.tolist()), is_in_polygon]
    df = pd.concat([df, pd.DataFrame([row], columns=["point", "polygon", "is_in_polygon"])], ignore_index=True)
    
df.to_csv(os.path.join(FOLDER, 'test.csv'), index=False)    
