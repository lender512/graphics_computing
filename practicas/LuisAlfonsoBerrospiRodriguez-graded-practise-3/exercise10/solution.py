import numpy as np
import matplotlib.pyplot as plt


def marching_squares(f, output_filename, xmin, ymin, xmax, ymax, precision):
    f = evaluate_function_2d(f)

    def marching_squares_u(f, xmin, ymin, xmax, ymax, precision, lines):
        xmid = (xmin + xmax) / 2
        ymid = (ymin + ymax) / 2

        f00 = f(xmin, ymin)
        f10 = f(xmax, ymin)
        f01 = f(xmin, ymax)
        f11 = f(xmax, ymax)

        square = (f01 > 0, f11 > 0, f00 > 0, f10 > 0)

        if square in [(True, True, True, True)]:
            if not check_if_function_changes_sign_in_square(f, xmin, ymin, xmax, ymax):
                return
        if square in [(False, False, False, False)]:
            if not check_if_function_changes_sign_in_square(f, xmin, ymin, xmax, ymax):
                return
        if ((xmax - xmin) < precision) and (ymax - ymin < precision):
            if square in [(False, False, False, True), (True, True, True, False)]:
                lines.append(((xmid, ymin), (xmax, ymid)))
            if square in [(True, False, False, False), (False, True, True, True)]:
                lines.append(((xmin, ymid), (xmid, ymax)))
            if square in [(False, True, False, False), (True, False, True, True)]:
                lines.append(((xmid, ymax), (xmax, ymid)))
            if square in [(False, False, True, False), (True, True, False, True)]:
                lines.append(((xmin, ymid), (xmid, ymin)))
            if square in [(True, False, True, False), (False, True, False, True)]:
                lines.append(((xmid, ymin), (xmid, ymax)))
            if square in [(True, True, False, False), (False, False, True, True)]:
                lines.append(((xmin, ymid), (xmax, ymid)))
            if square in [(True, False, False, True)]:
                lines.append(((xmin, ymid), (xmid, ymin)))
                lines.append(((xmid, ymax), (xmax, ymid)))
            if square in [(False, True, True, False)]:
                lines.append(((xmin, ymid), (xmid, ymax)))
                lines.append(((xmid, ymin), (xmax, ymid)))
            return

        marching_squares_u(f, xmin, ymin, xmid, ymid, precision, lines)
        marching_squares_u(f, xmin, ymid, xmid, ymax, precision, lines)
        marching_squares_u(f, xmid, ymin, xmax, ymid, precision, lines)
        marching_squares_u(f, xmid, ymid, xmax, ymax, precision, lines)

    lines = []
    marching_squares_u(f, xmin, ymin, xmax, ymax, precision, lines)

    plt.axis('equal')
    for line in lines:
        plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], 'k-')
    plt.axis('off')
    plt.savefig(output_filename, format='eps')


def check_if_function_changes_sign_in_square(f, xmin, ymin, xmax, ymax):
    N = 500
    points = np.random.rand(N, 2)
    points = points * np.array([xmax - xmin, ymax - ymin]
                               ) + np.array([xmin, ymin])
    first_sign = f(points[0][0], points[0][1]) > 0
    for point in points:
        if (f(point[0], point[1]) > 0) != first_sign:
            return True


def evaluate_function_2d(node):
    if node["op"] == "":
        function = node["function"]
        function = function.replace("^", "**")
        lambda_evaluated = eval("lambda x, y: " + function)
        return lambda x, y: 1 if lambda_evaluated(x, y) > 0 else -1

    children = node["childs"]
    if node["op"] == "union":
        lambdas = []
        for child in children:
            lambda_evaluated = evaluate_function_2d(child)
            lambdas.append(lambda_evaluated)
        return lambda x, y: 1 if all([lambda_evaluated(x, y) == 1 for lambda_evaluated in lambdas]) else -1
    elif node["op"] == "intersection":
        lambdas = []
        for child in children:
            lambda_evaluated = evaluate_function_2d(child)
            lambdas.append(lambda_evaluated)
        return lambda x, y: 1 if any([lambda_evaluated(x, y) == 1 for lambda_evaluated in lambdas]) else -1
    elif node["op"] == "diff":
        lambda_result_first = evaluate_function_2d(children[0])
        lambdas_other = []
        for child in children[1:]:
            lambda_evaluated = evaluate_function_2d(child)
            lambdas_other.append(lambda_evaluated)

        return lambda x, y: 1 if lambda_result_first(x, y) == 1 and all(
            [lambda_evaluated(x, y) == -1 for lambda_evaluated in lambdas_other]) else -1
    else:
        raise Exception("Invalid operation")


if __name__ == '__main__':
    example_json_2d = {
        "op": "union",
        "function": "",
        "childs": [
            {
                "op": "",
                "function": "(x-2)^2 + (y-3)^2 - 2^2",
                "childs": []
            }, {
                "op": "",
                "function": "(x+1)^2 + (y-3)^2 - 2^2",
                "childs": []
            },
        ]
    }
    marching_squares(example_json_2d, "output.eps", -5, -5, 5, 5, 0.1)
