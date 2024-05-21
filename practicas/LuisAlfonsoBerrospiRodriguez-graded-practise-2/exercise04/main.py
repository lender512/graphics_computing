import numpy as np
import pandas as pd
import os

FOLDER = "exercise04"

def pointIsInTriangle(point, triangle):
    # Calculate the sign of the cross product of the vectors
    sign_0 = np.sign(np.cross(triangle[1] - triangle[0], point - triangle[0]))
    sign_1 = np.sign(np.cross(triangle[2] - triangle[1], point - triangle[1]))
    sign_2 = np.sign(np.cross(triangle[0] - triangle[2], point - triangle[2]))
    # If the signs are the same, the point is inside the triangle
    return (sign_0 == sign_1 and sign_1 == sign_2)   


df_test = pd.read_csv(os.path.join(FOLDER, "test.csv"))

success = 0

for i in range(len(df_test)):
    tA = np.fromstring(df_test.loc[i, "tA"][1:-1], sep=" ", dtype=np.float64)
    tB = np.fromstring(df_test.loc[i, "tB"][1:-1], sep=" ", dtype=np.float64)
    tC = np.fromstring(df_test.loc[i, "tC"][1:-1], sep=" ", dtype=np.float64)
    point = np.fromstring(df_test.loc[i, "point"][1:-1], sep=" ", dtype=np.float64)
    is_in_triangle = pointIsInTriangle(point, [tA, tB, tC])
    if is_in_triangle == df_test.loc[i, "is_in_triangle"]:
        success += 1

print(f"Accuracy: {success/len(df_test):.2%}")
