import numpy as np
from collections import defaultdict

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
            file.write(f"3 {' '.join(map(str, face))}\n")

def read_ply(file_path):
    vertices = []
    faces = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        header_ended = False
        vertex_count = 0
        face_count = 0
        vertex_read = 0
        face_read = 0
        for line in lines:
            if header_ended:
                if vertex_read < vertex_count:
                    vertices.append(list(map(float, line.strip().split())))
                    vertex_read += 1
                elif face_read < face_count:
                    faces.append(list(map(int, line.strip().split()[1:])))
                    face_read += 1
            else:
                if line.startswith("element vertex"):
                    vertex_count = int(line.split()[2])
                elif line.startswith("element face"):
                    face_count = int(line.split()[2])
                elif line.strip() == "end_header":
                    header_ended = True
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

def loop(full_path_input_mesh, number_of_iterations, full_path_output_mesh):
    def split_edge(vertices, edge_vertices):
        edge_midpoints = {}
        for edge in edge_vertices:
            v1, v2 = edge
            mid = tuple(sorted([v1, v2]))
            if mid not in edge_midpoints:
                edge_midpoints[mid] = len(vertices)
                vertices.append((np.array(vertices[v1]) + np.array(vertices[v2])) / 2.0)
        return edge_midpoints

    def calculate_new_vertex_positions(vertices, faces, edge_midpoints):
        edge_face_map = defaultdict(list)
        for face in faces:
            for i in range(3):
                edge = tuple(sorted([face[i], face[(i + 1) % 3]]))
                edge_face_map[edge].append(face)

        new_vertices = np.array(vertices)
        valence = defaultdict(int)
        for face in faces:
            for v in face:
                valence[v] += 1
        
        for i, v in enumerate(vertices):
            if valence[i] == 0:
                continue
            beta = (0.625 - (0.375 + 0.25 * np.cos(2 * np.pi / valence[i])) ** 2) / valence[i]
            neighbor_sum = np.zeros(3)
            for edge in edge_face_map:
                if i in edge:
                    neighbor = edge[1] if edge[0] == i else edge[0]
                    neighbor_sum += vertices[neighbor]
            new_vertices[i] = (1 - valence[i] * beta) * np.array(v) + beta * neighbor_sum

        for edge, mid_idx in edge_midpoints.items():
            faces_adj = edge_face_map[edge]
            if len(faces_adj) == 2:
                f1, f2 = faces_adj
                other_vertices = [v for v in f1 if v not in edge] + [v for v in f2 if v not in edge]
                new_vertices[mid_idx] = 0.375 * (np.array(vertices[edge[0]]) + np.array(vertices[edge[1]])) + 0.125 * (np.array(vertices[other_vertices[0]]) + np.array(vertices[other_vertices[1]]))
            else:
                new_vertices[mid_idx] = 0.5 * (np.array(vertices[edge[0]]) + np.array(vertices[edge[1]]))

        return new_vertices.tolist()

    def create_new_faces(faces, edge_midpoints):
        new_faces = []
        for face in faces:
            mid_indices = [edge_midpoints[tuple(sorted([face[i], face[(i + 1) % 3]]))] for i in range(3)]
            new_faces.append([face[0], mid_indices[0], mid_indices[2]])
            new_faces.append([face[1], mid_indices[1], mid_indices[0]])
            new_faces.append([face[2], mid_indices[2], mid_indices[1]])
            new_faces.append([mid_indices[0], mid_indices[1], mid_indices[2]])
        return new_faces

    if full_path_input_mesh.lower().endswith('.off'):
        vertices, faces = read_off(full_path_input_mesh)
        file_format = 'off'
    elif full_path_input_mesh.lower().endswith('.ply'):
        vertices, faces = read_ply(full_path_input_mesh)
        file_format = 'ply'
    else:
        raise ValueError("Unsupported file format")

    for _ in range(number_of_iterations):
        edge_vertices = [(face[i], face[(i + 1) % 3]) for face in faces for i in range(3)]
        edge_midpoints = split_edge(vertices, edge_vertices)
        vertices = calculate_new_vertex_positions(vertices, faces, edge_midpoints)
        faces = create_new_faces(faces, edge_midpoints)

    if file_format == 'off':
        write_off(full_path_output_mesh, vertices, faces)
    elif file_format == 'ply':
        write_ply(full_path_output_mesh, vertices, faces)

# Example usage
loop(
    full_path_input_mesh='icosahedron.off',
    number_of_iterations=3,
    full_path_output_mesh='loop-from-cube-3-iterations.off'
)
