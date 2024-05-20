import numpy as np
import pandas as pd
import os

FOLDER = "exercise04"

def pointIsInTriangle(point, triangle):
    sign_0 = np.sign(np.cross(triangle[1] - triangle[0], point - triangle[0]))
    sign_1 = np.sign(np.cross(triangle[2] - triangle[1], point - triangle[1]))
    sign_2 = np.sign(np.cross(triangle[0] - triangle[2], point - triangle[2]))
    return (sign_0 == sign_1 and sign_1 == sign_2)   


triangle = [
    np.array([0, 0]),
    np.array([1, 0]),
    np.array([0, 1])
]

point = np.array([0.1, 0.2])

print(f"Point is in triangle: {pointIsInTriangle(point, triangle)}")

triangle = [
    np.array([0, 0]),
    np.array([1, 0]),
    np.array([0, 1])
]

point = np.array([2, 2])

print(f"Point is in triangle: {pointIsInTriangle(point, triangle)}")
