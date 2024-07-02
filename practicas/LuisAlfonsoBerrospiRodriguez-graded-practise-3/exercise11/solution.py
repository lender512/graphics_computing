import numpy as np

cases_memoization = {}

cases_base = {
    0: np.array([True, False, False, False, False, False, False, False]),
    1: np.array([True, True, False, False, False, False, False, False]),
    2: np.array([True, False, False, False, False, True, False, False]),
    3: np.array([False, True, False, False, True, True, False, False]),
    4: np.array([True, True, False, False, True, True, False, False]),
    5: np.array([False, True, True, True, True, False, False, False]),
    6: np.array([True, False, False, True, False, True, True, False]),
    7: np.array([True, False, False, False, True, True, True, False]),
    8: np.array([False, True, True, True, False, False, True, False]),
    9: np.array([True, False, False, False, False, False, False, True]),
    10: np.array([True, True, False, False, False, False, False, True]),
    11: np.array([False, True, False, False, True, False, False, True]),
    12: np.array([True, False, False, True, True, False, False, True]),
    13: np.array([True, False, True, True, False, False, False, True])
}
cases_dict = {
    0: lambda xmin, ymin, zmin, xmid, ymid, zmid, xmax, ymax, zmax: [[(xmin, ymin, zmid), (xmid, ymin, zmin), (xmin, ymid, zmin)]],
    1: lambda xmin, ymin, zmin, xmid, ymid, zmid, xmax, ymax, zmax: [[(xmin, ymin, zmid), (xmax, ymin, zmid), (xmin, ymid, zmin)],
                                                                     [(xmax, ymid, zmin), (xmax, ymin, zmid), (xmin, ymid, zmin)]],
    2: lambda xmin, ymin, zmin, xmid, ymid, zmid, xmax, ymax, zmax: [[(xmin, ymin, zmid), (xmid, ymin, zmin), (xmin, ymid, zmin)],
                                                                     [(xmid, ymin, zmax), (xmax, ymin, zmid), (xmax, ymid, zmax)]],
    3: lambda xmin, ymin, zmin, xmid, ymid, zmid, xmax, ymax, zmax: [[(xmid, ymin, zmin), (xmin, ymin, zmid), (xmax, ymid, zmin)],
                                                                     [(xmin, ymin, zmid), (xmin, ymid, zmax), (
                                                                         xmax, ymid, zmin)],
                                                                     [(xmin, ymid, zmax), (xmax, ymid, zmin), (xmax, ymid, zmax)]],
    4: lambda xmin, ymin, zmin, xmid, ymid, zmid, xmax, ymax, zmax: [[(xmin, ymid, zmin), (xmax, ymid, zmax), (xmax, ymid, zmin)],
                                                                     [(xmin, ymid, zmin), (xmax, ymid, zmax), (xmin, ymid, zmax)]],
    5: lambda xmin, ymin, zmin, xmid, ymid, zmid, xmax, ymax, zmax: [[(xmin, ymin, zmid), (xmid, ymin, zmax), (xmin, ymid, zmax)],
                                                                     [(xmid, ymin, zmin), (xmin, ymin, zmid), (
                                                                         xmax, ymid, zmin)],
                                                                     [(xmin, ymin, zmid), (xmin, ymid, zmax), (
                                                                         xmax, ymid, zmin)],
                                                                     [(xmin, ymid, zmax), (xmax, ymid, zmin), (xmax, ymid, zmax)]],
    6: lambda xmin, ymin, zmin, xmid, ymid, zmid, xmax, ymax, zmax: [[(xmin, ymin, zmid), (xmid, ymin, zmin), (xmin, ymid, zmin)],
                                                                     [(xmid, ymin, zmax), (xmax, ymin, zmid), (
                                                                         xmax, ymid, zmax)],
                                                                     [(xmin, ymid, zmax), (xmin, ymax, zmid), (
                                                                         xmid, ymax, zmax)],
                                                                     [(xmax, ymid, zmin), (xmid, ymax, zmin), (xmax, ymax, zmid)]],
    7: lambda xmin, ymin, zmin, xmid, ymid, zmid, xmax, ymax, zmax: [[(xmin, ymid, zmin), (xmin, ymax, zmid), (xmid, ymax, zmax)],
                                                                     [(xmin, ymid, zmin), (xmid, ymin, zmin), (
                                                                         xmid, ymax, zmax)],
                                                                     [(xmid, ymin, zmin), (xmid, ymax, zmax), (
                                                                         xmax, ymid, zmax)],
                                                                     [(xmax, ymid, zmax), (xmid, ymin, zmin), (xmax, ymin, zmid)]],
    8: lambda xmin, ymin, zmin, xmid, ymid, zmid, xmax, ymax, zmax: [[(xmin, ymid, zmin), (xmid, ymin, zmin), (xmin, ymid, zmax)],
                                                                     [(xmid, ymin, zmin), (xmin, ymid, zmax), (
                                                                         xmax, ymax, zmid)],
                                                                     [(xmin, ymid, zmax), (xmax, ymax, zmid), (
                                                                         xmid, ymax, zmax)],
                                                                     [(xmid, ymin, zmin), (xmax, ymin, zmid), (xmax, ymax, zmid)]],
    9: lambda xmin, ymin, zmin, xmid, ymid, zmid, xmax, ymax, zmax: [[(xmin, ymin, zmid), (xmid, ymin, zmin), (xmin, ymid, zmin)],
                                                                     [(xmax, ymid, zmax), (xmax, ymax, zmid), (xmid, ymax, zmax)]],
    10: lambda xmin, ymin, zmin, xmid, ymid, zmid, xmax, ymax, zmax: [[(xmin, ymin, zmid), (xmax, ymin, zmid), (xmin, ymid, zmin)],
                                                                      [(xmax, ymid, zmin), (xmax, ymin, zmid), (
                                                                          xmin, ymid, zmin)],
                                                                      [(xmax, ymid, zmax), (xmax, ymax, zmid), (xmid, ymax, zmax)]],
    11: lambda xmin, ymin, zmin, xmid, ymid, zmid, xmax, ymax, zmax: [[(xmin, ymin, zmid), (xmid, ymin, zmax), (xmin, ymid, zmax)],
                                                                      [(xmax, ymid, zmax), (xmax, ymax, zmid), (
                                                                          xmid, ymax, zmax)],
                                                                      [(xmid, ymin, zmin), (xmax, ymid, zmin), (xmax, ymin, zmid)]],
    12: lambda xmin, ymin, zmin, xmid, ymid, zmid, xmax, ymax, zmax: [[(xmin, ymid, zmin), (xmid, ymin, zmin), (xmin, ymid, zmax)],
                                                                      [(xmid, ymin, zmin), (xmin, ymid, zmax), (
                                                                          xmid, ymin, zmax)],
                                                                      [(xmid, ymax, zmin), (xmax, ymid, zmin), (
                                                                          xmid, ymax, zmax)],
                                                                      [(xmax, ymid, zmin), (xmid, ymax, zmax), (xmax, ymid, zmax)]],
    13: lambda xmin, ymin, zmin, xmid, ymid, zmid, xmax, ymax, zmax: [[(xmin, ymin, zmid), (xmid, ymin, zmin), (xmin, ymax, zmid)],
                                                                      [(xmid, ymin, zmin), (xmin, ymax, zmid), (
                                                                          xmax, ymid, zmax)],
                                                                      [(xmax, ymid, zmax), (xmid, ymax, zmax), (
                                                                          xmin, ymax, zmid)],
                                                                      [(xmid, ymin, zmin), (xmax, ymid, zmin), (xmax, ymid, zmax)]],
}

vertices_indices = {}


def get_idx(vertex):
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


def get_case(case, midpoint, rotation, color='k'):
    for i in range(len(case)):
        case[i] = rotate_point(case[i], midpoint, rotation)
    return case, color


def check_if_function_changes_sign(f, xmin, ymin, zmin, xmax, ymax, zmax, rec):
    N = int(2000 / rec) + 32
    montecarlo_points = np.random.rand(N, 3)
    points = montecarlo_points * np.array([xmax - xmin, ymax - ymin, zmax - zmin]) + np.array(
        [xmin, ymin, zmin])
    first_sign = f(points[0][0], points[0][1], points[0][2]) > 0
    for point in points:
        if (f(point[0], point[1], point[2]) > 0) != first_sign:
            return True


def fix_faces(faces):
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


def write(faces, path, is_ply=False):
    faces = fix_faces(faces)

    vertices = set()
    for face in faces:
        for vertex in face:
            vertices.add(tuple(vertex))

    vertices = list(vertices)

    for i, vertex in enumerate(vertices):
        vertices_indices[vertex] = i

    if is_ply:
        with open(path, 'w') as file:
            file.write("ply\n")
            file.write("format ascii 1.0\n")
            file.write(f"element vertex {len(vertices)}\n")
            file.write("property float x\n")
            file.write("property float y\n")
            file.write("property float z\n")
            file.write(f"element face {len(faces)}\n")
            file.write("property list uchar int vertex_index\n")
            file.write("end_header\n")
            for v in vertices:
                file.write(f"{' '.join(map(str, v))}\n")
            for f in faces:
                file.write(f"{len(f)} {' '.join(
                    [str(get_idx(vertex)) for vertex in f])}\n")
    else:
        with open(path, 'w') as file:
            file.write("OFF\n")
            file.write(f"{len(vertices)} {len(faces)} 0\n")
            for v in vertices:
                file.write(f"{' '.join(map(str, v))}\n")
            for f in faces:
                file.write(f"{len(f)} {' '.join(
                    [str(get_idx(vertex)) for vertex in f])}\n")


def rotate_1d_cube(cube, angle_x, angle_y, angle_z):
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

    rotated_coords = rotate_point(
        coords, (0.5, 0.5, 0.5), (angle_x, angle_y, angle_z))

    rotated_cube = np.zeros(8, dtype=bool)
    for i in range(8):
        x = int(rotated_coords[i][0] + 0.5)
        y = int(rotated_coords[i][1] + 0.5)
        z = int(rotated_coords[i][2] + 0.5)
        rotated_cube[i] = cube[x + 2 * y + 4 * z]

    return np.array(rotated_cube)


def utility(f, xmin, ymin, zmin, xmax, ymax, zmax, precision, faces, colors, level=1):
    xmid = (xmin + xmax) / 2
    ymid = (ymin + ymax) / 2
    zmid = (zmin + zmax) / 2

    cube = np.array([
                    f(xmin, ymin, zmin) > 0,
                    f(xmax, ymin, zmin) > 0,
                    f(xmin, ymax, zmin) > 0,
                    f(xmax, ymax, zmin) > 0,
                    f(xmin, ymin, zmax) > 0,
                    f(xmax, ymin, zmax) > 0,
                    f(xmin, ymax, zmax) > 0,
                    f(xmax, ymax, zmax) > 0
                    ])

    if np.all(cube) or np.all(~cube):
        if not check_if_function_changes_sign(f, xmin, ymin, zmin, xmax, ymax, zmax, level):
            return

    if ((xmax - xmin) < precision) and (ymax - ymin < precision) and (zmax - zmin < precision):

        local_faces = []

        cases = []
        for case in cases_dict:
            cases.append(cases_dict[case](
                xmin, ymin, zmin, xmid, ymid, zmid, xmax, ymax, zmax))

        if tuple(cube) in cases_memoization:
            case, rotation = cases_memoization[tuple(cube)]
            local_faces = get_case(cases[case], (xmid, ymid, zmid), rotation)
        else:
            found = False
            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        x = i * 90
                        y = j * 90
                        z = k * 90
                        rotated_cube = rotate_1d_cube(cube, x, y, z)
                        for case in cases_dict:
                            if (rotated_cube == cases_base[case]).all() or (rotated_cube == ~cases_base[case]).all():
                                local_faces = get_case(
                                    cases_dict[case](xmin, ymin, zmin, xmid, ymid, zmid, xmax, ymax, zmax), (xmid, ymid, zmid), (x, y, z))
                                found = True
                                cases_memoization[tuple(cube)] = (
                                    case, (x, y, z))
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

    utility(f, xmin, ymin, zmin, xmid, ymid, zmid,
            precision, faces, colors, level + 1)
    utility(f, xmid, ymin, zmin, xmax, ymid, zmid,
            precision, faces, colors, level + 1)
    utility(f, xmin, ymid, zmin, xmid, ymax, zmid,
            precision, faces, colors, level + 1)
    utility(f, xmid, ymid, zmin, xmax, ymax, zmid,
            precision, faces, colors, level + 1)
    utility(f, xmin, ymin, zmid, xmid, ymid, zmax,
            precision, faces, colors, level + 1)
    utility(f, xmid, ymin, zmid, xmax, ymid, zmax,
            precision, faces, colors, level + 1)
    utility(f, xmin, ymid, zmid, xmid, ymax, zmax,
            precision, faces, colors, level + 1)
    utility(f, xmid, ymid, zmid, xmax, ymax, zmax,
            precision, faces, colors, level + 1)


def marching_cubes(json_object_describing_surface, output_filename, xmin, ymin, zmin, xmax, ymax, zmax, precision):
    f = evaluate_function_3d(json_object_describing_surface)
    faces = []
    colors = []
    utility(f, xmin, ymin, zmin, xmax, ymax,
            zmax, precision, faces, colors)
    write(faces, output_filename, is_ply=output_filename.endswith(
        ".ply") or output_filename.endswith(".PLY"))


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
    example_json_3d = {
        "op": "diff",
        "function": "",
        "childs": [
            {
                "op": "",
                "function": "(x-2)^2 + (y-3)^2 + (z-3)^2 - 2^2",
                "childs": []
            }, {
                "op": "",
                "function": "(x)^2 + (y-3)^2 + (z-3)^2 - 2^2",
                "childs": []
            },
        ]
    }
    marching_cubes(example_json_3d, "output.PLY", -5, -5, -5, 5, 5, 5, 0.05)
