import numpy as np

def read(path, is_ply=False):
    vertices = []
    faces = []
    if is_ply:
        with open(path, 'r') as file:
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
    else:
        with open(path, 'r') as file:
            lines = file.readlines()
            assert lines[0].strip() == "OFF"
            n_vertices, n_faces, _ = map(int, lines[1].strip().split())
            for i in range(2, 2 + n_vertices):
                vertices.append(list(map(float, lines[i].strip().split())))
            for i in range(2 + n_vertices, 2 + n_vertices + n_faces):
                faces.append(list(map(int, lines[i].strip().split()[1:])))
    return vertices, faces

def save(path, vertices, faces, is_ply=False):
    if is_ply:
        with open(path, 'w') as file:
            file.write("ply\n")
            file.write("format ascii 1.0\n")
            file.write(f"element vertex {len(vertices)}\n")
            file.write("property float x\n")
            file.write("property float y\n")
            file.write("property float z\n")
            file.write(f"element face {len(faces)}\n")
            file.write("property list uchar int vertex_indices\n")
            file.write("end_header\n")
            for v in vertices:
                file.write(f"{' '.join(map(str, v))}\n")
            for f in faces:
                file.write(f"{len(f)} {' '.join(map(str, f))}\n")
    else:
        with open(path, 'w') as file:
            file.write("OFF\n")
            file.write(f"{len(vertices)} {len(faces)} 0\n")
            for v in vertices:
                file.write(f"{' '.join(map(str, v))}\n")
            for f in faces:
                file.write(f"{len(f)} {' '.join(map(str, f))}\n")

def rotation_matrix(ax, theta):
    ax = np.asarray(ax)
    ax = ax / np.sqrt(np.dot(ax, ax))
    a = np.cos(theta / 2.0)
    b, c, d = -ax * np.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                    [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                    [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

def rotate_mesh_around_line(full_path_input_mesh, axis_of_rotation, alpha, full_path_output_mesh):

    vertices, faces = read(full_path_input_mesh, 
                           full_path_input_mesh.lower().endswith('.ply') or full_path_input_mesh.lower().endswith('.PLY'))

    d = np.array(axis_of_rotation[1])
    p = np.array(axis_of_rotation[0])

    matrix = rotation_matrix(d, alpha)
    
    vertices = np.array(vertices)
    vertices_xyz = vertices[:, :3]
    rotated_xyz = np.dot(matrix, (vertices_xyz - p).T).T + p
    rotated_vertices = vertices.copy()
    rotated_vertices[:, :3] = rotated_xyz

    save(full_path_output_mesh, 
         rotated_vertices, faces, 
         full_path_output_mesh.lower().endswith('.ply') or full_path_output_mesh.lower().endswith('.PLY'))
        
if __name__ == '__main__':
    rotate_mesh_around_line(
        full_path_input_mesh='sphere_triangular.off',
        axis_of_rotation=((10, 10, 0), (10, 0, 10)),
        alpha=40,
        full_path_output_mesh='sphere-rotated.off'
    )

