import math
import numpy as np

def read_off(file_path):
    vertices = []
    faces = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        assert lines[0].strip() == "OFF"
        n_vertices, n_faces, _ = map(int, lines[1].strip().split())
        for i in range(2, 2 + n_vertices):
            vertices.append(list(map(float, lines[i].strip().split())))
        for i in range(2 + n_vertices, 2 + n_vertices + n_faces):
            faces.append(list(map(int, lines[i].strip().split()[1:])))
    return vertices, faces

def write_off(file_path, vertices, faces):
    with open(file_path, 'w') as file:
        file.write("OFF\n")
        file.write(f"{len(vertices)} {len(faces)} 0\n")
        for vertex in vertices:
            file.write(f"{' '.join(map(str, vertex))}\n")
        for face in faces:
            file.write(f"{len(face)} {' '.join(map(str, face))}\n")

def read_ply(file_path):
    vertices = []
    faces = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        header_ended = False
        vertex_count = 0
        face_count = 0
        reading_vertices = False
        reading_faces = False
        for line in lines:
            if line.startswith("end_header"):
                header_ended = True
                reading_vertices = True
                continue
            if not header_ended:
                if line.startswith("element vertex"):
                    vertex_count = int(line.split()[-1])
                if line.startswith("element face"):
                    face_count = int(line.split()[-1])
            else:
                if reading_vertices:
                    if vertex_count > 0:
                        vertices.append(list(map(float, line.strip().split())))
                        vertex_count -= 1
                        if vertex_count == 0:
                            reading_vertices = False
                            reading_faces = True
                elif reading_faces:
                    if face_count > 0:
                        faces.append(list(map(int, line.strip().split()[1:])))
                        face_count -= 1
    return vertices, faces

def write_ply(file_path, vertices, faces):
    with open(file_path, 'w') as file:
        file.write("ply\n")
        file.write("format ascii 1.0\n")
        file.write(f"element vertex {len(vertices)}\n")
        file.write("property float x\n")
        file.write("property float y\n")
        file.write("property float z\n")
        file.write(f"element face {len(faces)}\n")
        file.write("property list uchar int vertex_indices\n")
        file.write("end_header\n")
        for vertex in vertices:
            file.write(f"{' '.join(map(str, vertex))}\n")
        for face in faces:
            file.write(f"3 {' '.join(map(str, face))}\n")

def rotate_mesh_around_line(full_path_input_mesh, axis_of_rotation, alpha, full_path_output_mesh):
    def rotation_matrix(axis, theta):
        axis = np.asarray(axis)
        theta = np.radians(theta)
        axis = axis / math.sqrt(np.dot(axis, axis))
        a = math.cos(theta / 2.0)
        b, c, d = -axis * math.sin(theta / 2.0)
        aa, bb, cc, dd = a * a, b * b, c * c, d * d
        bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
        return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                         [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                         [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

    if full_path_input_mesh.lower().endswith('.off'):
        vertices, faces = read_off(full_path_input_mesh)
    elif full_path_input_mesh.lower().endswith('.ply'):
        vertices, faces = read_ply(full_path_input_mesh)
    else:
        raise ValueError("Unsupported file format")

    p, d = axis_of_rotation
    d = np.array(d)
    p = np.array(p)

    R = rotation_matrix(d, alpha)
    rotated_vertices = []

    for vertex in vertices:
        v = np.array(vertex[:3]) - p
        rotated_v = np.dot(R, v) + p
        if len(vertex) > 3:
            rotated_vertices.append(list(rotated_v) + vertex[3:])
        else:
            rotated_vertices.append(list(rotated_v))

    if full_path_output_mesh.lower().endswith('.off'):
        write_off(full_path_output_mesh, rotated_vertices, faces)
    elif full_path_output_mesh.lower().endswith('.ply'):
        write_ply(full_path_output_mesh, rotated_vertices, faces)

# Example usage
rotate_mesh_around_line(
    full_path_input_mesh='sphere.off',
    axis_of_rotation=((0, 0, 0), (0, 0, 100)),
    alpha=40,
    full_path_output_mesh='sphere-rotated.off'
)

