import json
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch

def parse_json(json_object):
    operation = json_object['op']
    if operation == 'union':
        
        

def eval_function(expr):
    def inner(x, y):
        return eval(expr)
    return inner

def eval_tree(tree):
    if tree['function']:
        return eval_function(tree['function'])
    else:
        return parse_json(tree)

def generate_grid(x_min, y_min, x_max, y_max, step):
    x, y = np.meshgrid(np.arange(x_min, x_max + step, step), np.arange(y_min, y_max + step, step))
    return x, y

def marching_squares(json_object_describing_curve, output_filename, x_min, y_min, x_max, y_max, precision):
    function = eval_tree(json_object_describing_curve)

    fig, ax = plt.subplots()
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect('equal')

    def draw_path(path):
        patch = PathPatch(path, facecolor='none', edgecolor='black')
        ax.add_patch(patch)

    def subdivide(x_min, y_min, x_max, y_max):
        if x_max - x_min < precision and y_max - y_min < precision:
            x, y = generate_grid(x_min, y_min, x_max, y_max, precision)
            z = function(x, y)
            contours = plt.contour(x, y, z, levels=[0], colors='black')
            for contour in contours.collections:
                path = contour.get_paths()[0]
                draw_path(path)
        else:
            x_mid = (x_min + x_max) / 2
            y_mid = (y_min + y_max) / 2
            subdivide(x_min, y_min, x_mid, y_mid)
            subdivide(x_mid, y_min, x_max, y_mid)
            subdivide(x_min, y_mid, x_mid, y_max)
            subdivide(x_mid, y_mid, x_max, y_max)

    subdivide(x_min, y_min, x_max, y_max)

    plt.savefig(output_filename, format='eps')
    plt.close()

# Example usage
example_json = {
    "op": "union",
    "function": "",
    "childs": [
        {
            "op": "",
            "function": "(x-2)**2 + (y-3)**2 - 4**2",
            "childs": []
        }
    ]
}

marching_squares(
    example_json,
    'example-marching-squares.eps',
    -5, -5, 6, 6,
    0.1
)
