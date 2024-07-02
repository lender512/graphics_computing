import numpy as np
import matplotlib.pyplot as plt

cases = {
    1: np.array([True, True, True, True]),
    2: np.array([False, False, False, True]),
    3: np.array([True, False, False, False]),
    4: np.array([False, True, False, False]),
    5: np.array([False, False, True, False]),
    6: np.array([True, False, True, False]),
    7: np.array([True, True, False, False]),
    8: np.array([True, False, False, True]),
    9: np.array([False, True, True, False]),
}


def marching_squares(f, output_filename, xmin, ymin, xmax, ymax, precision):
    f = evaluate(f)

    def utility(f, xmin, ymin, xmax, ymax, precision, lines):
        xmid = (xmin + xmax) / 2
        ymid = (ymin + ymax) / 2

        square = np.array([f(xmin, ymax) > 0, f(xmax, ymax)
                          > 0, f(xmin, ymin) > 0, f(xmax, ymin) > 0])

        if (square == cases[1]).all() or (~square == cases[1]).all():
            if not check_if_function_changes_sign_in_square(f, xmin, ymin, xmax, ymax):
                return
        if ((xmax - xmin) < precision) and (ymax - ymin < precision):
            if (square == cases[2]).all() or (~square == cases[2]).all():
                lines.append(((xmid, ymin), (xmax, ymid)))
            if (square == cases[3]).all() or (~square == cases[3]).all():
                lines.append(((xmin, ymid), (xmid, ymax)))
            if (square == cases[4]).all() or (~square == cases[4]).all():
                lines.append(((xmid, ymax), (xmax, ymid)))
            if (square == cases[5]).all() or (~square == cases[5]).all():
                lines.append(((xmin, ymid), (xmid, ymin)))
            if (square == cases[6]).all() or (~square == cases[6]).all():
                lines.append(((xmid, ymin), (xmid, ymax)))
            if (square == cases[7]).all() or (~square == cases[7]).all():
                lines.append(((xmin, ymid), (xmax, ymid)))
            if (square == cases[8]).all():
                lines.append(((xmin, ymid), (xmid, ymin)))
                lines.append(((xmid, ymax), (xmax, ymid)))
            if (square == cases[9]).all():
                lines.append(((xmin, ymid), (xmid, ymax)))
                lines.append(((xmid, ymin), (xmax, ymid)))
            return

        utility(f, xmin, ymin, xmid, ymid, precision, lines)
        utility(f, xmin, ymid, xmid, ymax, precision, lines)
        utility(f, xmid, ymin, xmax, ymid, precision, lines)
        utility(f, xmid, ymid, xmax, ymax, precision, lines)

    lines = []
    utility(f, xmin, ymin, xmax, ymax, precision, lines)

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


def evaluate(node):
    if node["op"] == "":
        function = node["function"]
        function = function.replace("^", "**")
        lambda_evaluated = eval("lambda x, y: " + function)
        return lambda x, y: 1 if lambda_evaluated(x, y) > 0 else -1

    children = node["childs"]
    if node["op"] == "union":
        lambdas = []
        for child in children:
            lambda_evaluated = evaluate(child)
            lambdas.append(lambda_evaluated)
        return lambda x, y: 1 if all([lambda_evaluated(x, y) == 1 for lambda_evaluated in lambdas]) else -1
    elif node["op"] == "intersection":
        lambdas = []
        for child in children:
            lambda_evaluated = evaluate(child)
            lambdas.append(lambda_evaluated)
        return lambda x, y: 1 if any([lambda_evaluated(x, y) == 1 for lambda_evaluated in lambdas]) else -1
    elif node["op"] == "diff":
        lambda_result_first = evaluate(children[0])
        lambdas_other = []
        for child in children[1:]:
            lambda_evaluated = evaluate(child)
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
