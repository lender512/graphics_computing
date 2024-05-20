import numpy as np
import pandas as pd
import os

FOLDER = 'exercise02'

def isConvex(vertices):
    if len(vertices) < 3:
        return False
    clockwise = 0
    # Check if the polygon is convex
    for i in range(len(vertices)):
        # Get the three consecutive vertices
        p1 = vertices[i]
        p2 = vertices[(i + 1) % len(vertices)]
        p3 = vertices[(i + 2) % len(vertices)]

        # Calculate the cross product of the two vectors
        crossProduct = (p2[0] - p1[0]) * (p3[1] - p2[1]) - (p2[1] - p1[1]) * (p3[0] - p2[0])

        if clockwise == 0:
            clockwise = crossProduct
        else:
            # If the cross product changes sign, the polygon is not convex
            if (crossProduct > 0 and clockwise < 0) or (crossProduct < 0 and clockwise > 0):
                return False
    return True

test = pd.read_csv(os.path.join(FOLDER, 'test.csv'))
y = test['is_convex']
Y = test['vertices'].apply(lambda x: isConvex(eval(x)))

succes_ratio = np.mean(y == Y)
print(f'Succes ratio: {succes_ratio:.2%}')




