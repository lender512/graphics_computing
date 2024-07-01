import numpy as np

nemo_coin = {}
nemo_coin_values = {}

case_1_base = np.array([True, False, False, False, False, False, False, False])
case_2_base = np.array([True, True, False, False, False, False, False, False])
case_4_base = np.array([False, True, False, False, True, True, False, False])
case_5_base = np.array([True, True, False, False, True, True, False, False])
case_8_base = np.array([True, False, False, False, True, True, True, False])

vertices_indices = {}


def get_index(vertex):
    if tuple(vertex) in vertices_indices:
        return vertices_indices[tuple(vertex)]
    return -1


def rotate_point(points_3d, pivot_3d, angle_3d):
    points_3d = np.array(points_3d)
    pivot_3d = np.array(pivot_3d)
    angle_3d = np.array(angle_3d)

    points_3d = points_3d - pivot_3d

    angle_3d = np.radians(angle_3d)
    angle_x = angle_3d[0]
    angle_y = angle_3d[1]
    angle_z = angle_3d[2]

    rotation_x = np.array([[1, 0, 0],
                           [0, np.cos(angle_x), -np.sin(angle_x)],
                           [0, np.sin(angle_x), np.cos(angle_x)]])

    rotation_y = np.array([[np.cos(angle_y), 0, np.sin(angle_y)],
                           [0, 1, 0],
                           [-np.sin(angle_y), 0, np.cos(angle_y)]])

    rotation_z = np.array([[np.cos(angle_z), -np.sin(angle_z), 0],
                           [np.sin(angle_z), np.cos(angle_z), 0],
                           [0, 0, 1]])

    rotation_matrix = np.dot(np.dot(rotation_x, rotation_y), rotation_z)

    rotated_points = np.dot(points_3d, rotation_matrix.T)

    rotated_points = rotated_points + pivot_3d

    return rotated_points.tolist()


def setup_case(case, midpoint, rotation, color='k'):
    for i in range(len(case)):
        case[i] = rotate_point(case[i], midpoint, rotation)
    return case, color


def check_if_function_changes_sign_in_square(f, xmin, ymin, xmax, ymax):
    N = 500
    points = np.random.rand(N, 2)
    points = points * np.array([xmax - xmin, ymax - ymin]) + np.array([xmin, ymin])
    first_sign = f(points[0][0], points[0][1]) > 0
    for point in points:
        if (f(point[0], point[1]) > 0) != first_sign:
            return True


def check_if_function_changes_sign_in_box(f, xmin, ymin, zmin, xmax, ymax, zmax, level):
    N = int(2048 / level) + 32
    points_random_montercarlo = np.random.rand(N, 3)
    points = points_random_montercarlo * np.array([xmax - xmin, ymax - ymin, zmax - zmin]) + np.array(
        [xmin, ymin, zmin])
    first_sign = f(points[0][0], points[0][1], points[0][2]) > 0
    for point in points:
        if (f(point[0], point[1], point[2]) > 0) != first_sign:
            return True


def make_faces_point_outside(faces):
    all_vertices = np.array([vertex for face in faces for vertex in face])
    mesh_center = np.mean(all_vertices, axis=0)

    for i in range(len(faces)):
        face = np.array(faces[i])
        v0, v1, v2 = face

        normal = np.cross(v1 - v0, v2 - v0)

        face_center = np.mean(face, axis=0)

        if np.dot(normal, face_center - mesh_center) < 0:
            faces[i] = face[::-1].tolist()

    return faces


def to_OFF(faces, filename):
    faces = make_faces_point_outside(faces)

    vertices = set()
    for face in faces:
        for vertex in face:
            vertices.add(tuple(vertex))

    vertices = list(vertices)

    for i, vertex in enumerate(vertices):
        vertices_indices[vertex] = i

    with open(filename, 'w') as f:
        f.write('OFF\n')
        f.write(f'{len(vertices)} {len(faces)} 0\n')
        # for vertex in vertices:
        #     f.write(f'{vertex[0]} {vertex[1]} {vertex[2]}\n')

        to_write_vertices = ""
        for vertex in vertices:
            to_write_vertices += f'{vertex[0]} {vertex[1]} {vertex[2]}\n'
        f.write(to_write_vertices)

        to_write_faces = ""
        for face in faces:
            to_write_faces += f'{len(face)} {" ".join([str(get_index(vertex)) for vertex in face])}\n'
        f.write(to_write_faces)


def rotate_z_curve(cube, angle_x, angle_y, angle_z):
    coords = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [0, 1, 0],
        [1, 1, 0],
        [0, 0, 1],
        [1, 0, 1],
        [0, 1, 1],
        [1, 1, 1]
    ])

    rotated_coords = rotate_point(coords, (0.5, 0.5, 0.5), (angle_x, angle_y, angle_z))

    rotated_cube = np.zeros(8, dtype=bool)
    for i in range(8):
        x = int(rotated_coords[i][0] + 0.5)
        y = int(rotated_coords[i][1] + 0.5)
        z = int(rotated_coords[i][2] + 0.5)
        rotated_cube[i] = cube[x + 2 * y + 4 * z]

    return np.array(rotated_cube)


def marching_cubes_u(f, xmin, ymin, zmin, xmax, ymax, zmax, precision, faces, colors, level=1):
    xmid = (xmin + xmax) / 2
    ymid = (ymin + ymax) / 2
    zmid = (zmin + zmax) / 2

    f000 = f(xmin, ymin, zmin)
    f100 = f(xmax, ymin, zmin)
    f010 = f(xmin, ymax, zmin)
    f110 = f(xmax, ymax, zmin)
    f001 = f(xmin, ymin, zmax)
    f101 = f(xmax, ymin, zmax)
    f011 = f(xmin, ymax, zmax)
    f111 = f(xmax, ymax, zmax)

    cube = np.array([f000 > 0, f100 > 0, f010 > 0, f110 > 0, f001 > 0, f101 > 0, f011 > 0, f111 > 0])

    if np.all(cube) or np.all(~cube):
        if not check_if_function_changes_sign_in_box(f, xmin, ymin, zmin, xmax, ymax, zmax, level):
            return

    if ((xmax - xmin) < precision) and (ymax - ymin < precision) and (zmax - zmin < precision):
        case_1 = [[(xmin, ymin, zmid), (xmid, ymin, zmin), (xmin, ymid, zmin)]]
        case_2 = [[(xmin, ymin, zmid), (xmax, ymin, zmid), (xmin, ymid, zmin)],
                  [(xmax, ymid, zmin), (xmax, ymin, zmid), (xmin, ymid, zmin)]]
        # case_3 = [case_1,
        #           rotate_point(case_1, (xmid, ymid, zmid), (0, 0, 180))]
        case_4 = [[(xmid, ymin, zmin), (xmin, ymin, zmid), (xmax, ymid, zmin)],
                  [(xmin, ymin, zmid), (xmin, ymid, zmax), (xmax, ymid, zmin)],
                  [(xmin, ymid, zmax), (xmax, ymid, zmin), (xmax, ymid, zmax)]]
        case_5 = [[(xmin, ymid, zmin), (xmax, ymid, zmax), (xmax, ymid, zmin)],
                  [(xmin, ymid, zmin), (xmax, ymid, zmax), (xmin, ymid, zmax)]]
        case_8 = [[(xmin, ymid, zmin), (xmin, ymax, zmid), (xmid, ymax, zmax)],
                  [(xmin, ymid, zmin), (xmid, ymin, zmin), (xmid, ymax, zmax)],
                  [(xmid, ymin, zmin), (xmid, ymax, zmax), (xmax, ymid, zmax)],
                  [(xmax, ymid, zmax), (xmid, ymin, zmin), (xmax, ymin, zmid)]]

        local_faces = []

        cases = [case_1, case_2, case_4, case_5, case_8]

        if tuple(cube) in nemo_coin:
            case, rotation = nemo_coin[tuple(cube)]
            local_faces = setup_case(cases[case], (xmid, ymid, zmid), rotation)
        else:
            found = False
            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        x = i * 90
                        y = j * 90
                        z = k * 90

                        rotated_cube = rotate_z_curve(cube, x, y, z)

                        if (rotated_cube == case_1_base).all() or (rotated_cube == ~case_1_base).all():
                            local_faces = setup_case(case_1, (xmid, ymid, zmid), (x, y, z))
                            found = True
                            nemo_coin[tuple(cube)] = (0, (x, y, z))
                            break
                        if (rotated_cube == case_2_base).all() or (rotated_cube == ~case_2_base).all():
                            local_faces = setup_case(case_2, (xmid, ymid, zmid), (x, y, z))
                            found = True
                            nemo_coin[tuple(cube)] = (1, (x, y, z))
                            break
                        if (rotated_cube == case_4_base).all() or (rotated_cube == ~case_4_base).all():
                            local_faces = setup_case(case_4, (xmid, ymid, zmid), (x, y, z))
                            found = True
                            nemo_coin[tuple(cube)] = (2, (x, y, z))
                            break
                        if (rotated_cube == case_5_base).all() or (rotated_cube == ~case_5_base).all():
                            local_faces = setup_case(case_5, (xmid, ymid, zmid), (x, y, z))
                            found = True
                            nemo_coin[tuple(cube)] = (3, (x, y, z))
                            break
                        if (rotated_cube == case_8_base).all() or (rotated_cube == ~case_8_base).all():
                            local_faces = setup_case(case_8, (xmid, ymid, zmid), (x, y, z))
                            found = True
                            nemo_coin[tuple(cube)] = (4, (x, y, z))
                            break
                    if found:
                        break
                if found:
                    break

        if len(local_faces) != 0:
            for face in local_faces[0]:
                faces.append(face)
            colors.append(local_faces[1])

        return

    marching_cubes_u(f, xmin, ymin, zmin, xmid, ymid, zmid, precision, faces, colors, level + 1)
    marching_cubes_u(f, xmid, ymin, zmin, xmax, ymid, zmid, precision, faces, colors, level + 1)
    marching_cubes_u(f, xmin, ymid, zmin, xmid, ymax, zmid, precision, faces, colors, level + 1)
    marching_cubes_u(f, xmid, ymid, zmin, xmax, ymax, zmid, precision, faces, colors, level + 1)
    marching_cubes_u(f, xmin, ymin, zmid, xmid, ymid, zmax, precision, faces, colors, level + 1)
    marching_cubes_u(f, xmid, ymin, zmid, xmax, ymid, zmax, precision, faces, colors, level + 1)
    marching_cubes_u(f, xmin, ymid, zmid, xmid, ymax, zmax, precision, faces, colors, level + 1)
    marching_cubes_u(f, xmid, ymid, zmid, xmax, ymax, zmax, precision, faces, colors, level + 1)


def marching_cubes(f, output_filename, xmin, ymin, zmin, xmax, ymax, zmax, precision):
    faces = []
    colors = []
    marching_cubes_u(f, xmin, ymin, zmin, xmax, ymax, zmax, precision, faces, colors)
    to_OFF(faces, output_filename)


example_json_3d = {
    "op": "union",
    "function": "",
    "childs": [
        {
            "op": "",
            "function": "(x-2)^2 + (y-3)^2 + (z-3)^2 - 2^2",
            "childs": []
        }, {
            "op": "",
            "function": "(x+1)^2 + (y-3)^2 + (z-3)^2 - 2^2",
            "childs": []
        },
    ]
}


def evaluate_function_3d(node):
    if node["op"] == "":
        function = node["function"]
        function = function.replace("^", "**")
        lambda_evaluated = eval("lambda x, y, z: " + function)
        return lambda x, y, z: 1 if lambda_evaluated(x, y, z) > 0 else -1

    children = node["childs"]
    if node["op"] == "union":
        lambdas = []
        for child in children:
            lambda_evaluated = evaluate_function_3d(child)
            lambdas.append(lambda_evaluated)
        return lambda x, y, z: 1 if all([lambda_evaluated(x, y, z) == 1 for lambda_evaluated in lambdas]) else -1

    elif node["op"] == "intersection":
        lambdas = []
        for child in children:
            lambda_evaluated = evaluate_function_3d(child)
            lambdas.append(lambda_evaluated)
        return lambda x, y, z: 1 if any([lambda_evaluated(x, y, z) == 1 for lambda_evaluated in lambdas]) else -1

    elif node["op"] == "diff":
        lambda_result_first = evaluate_function_3d(children[0])
        lambdas_other = []
        for child in children[1:]:
            lambda_evaluated = evaluate_function_3d(child)
            lambdas_other.append(lambda_evaluated)

        return lambda x, y, z: 1 if lambda_result_first(x, y, z) == 1 and all(
            [lambda_evaluated(x, y, z) == -1 for lambda_evaluated in lambdas_other]) else -1
    else:
        raise Exception("Invalid operation")


if __name__ == '__main__':
    evaluated_function_3d = evaluate_function_3d(example_json_3d)
    marching_cubes(evaluated_function_3d, "output.OFF", -5, -5, -5, 5, 5, 5, 0.1)
