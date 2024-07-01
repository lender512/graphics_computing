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

def loop(full_path_input_mesh, number_of_iterations, full_path_output_mesh):
    def split_edges(vertices, edge_list):
        midpoints = {}
        for edge in edge_list:
            vertex1, vertex2 = edge
            midpoint = tuple(sorted([vertex1, vertex2]))
            if midpoint not in midpoints:
                midpoints[midpoint] = len(vertices)
                vertices.append((np.array(vertices[vertex1]) + np.array(vertices[vertex2])) / 2.0)
        return midpoints

    def update_vertex_positions(vertices, faces, midpoints):
        edge_to_face_map = {}
        for face in faces:
            for i in range(3):
                edge = tuple(sorted([face[i], face[(i + 1) % 3]]))
                if edge not in edge_to_face_map:
                    edge_to_face_map[edge] = []
                edge_to_face_map[edge].append(face)

        new_positions = np.array(vertices)
        valences = {}
        for face in faces:
            for vertex in face:
                if vertex not in valences:
                    valences[vertex] = 0
                valences[vertex] += 1
        
        for index, vertex in enumerate(vertices):
            if index not in valences:
                continue
            beta = (0.625 - (0.375 + 0.25 * np.cos(2 * np.pi / valences[index])) ** 2) / valences[index]
            neighbor_sum = np.zeros(3)
            for edge in edge_to_face_map:
                if index in edge:
                    neighbor = edge[1] if edge[0] == index else edge[0]
                    neighbor_sum += vertices[neighbor]
            new_positions[index] = (1 - valences[index] * beta) * np.array(vertex) + beta * neighbor_sum

        for edge, mid_index in midpoints.items():
            adjacent_faces = edge_to_face_map[edge]
            if len(adjacent_faces) == 2:
                face1, face2 = adjacent_faces
                other_vertices = [v for v in face1 if v not in edge] + [v for v in face2 if v not in edge]
                new_positions[mid_index] = 0.375 * (np.array(vertices[edge[0]]) + np.array(vertices[edge[1]])) + 0.125 * (np.array(vertices[other_vertices[0]]) + np.array(vertices[other_vertices[1]]))
            else:
                new_positions[mid_index] = 0.5 * (np.array(vertices[edge[0]]) + np.array(vertices[edge[1]]))

        return new_positions.tolist()

    def generate_new_faces(faces, midpoints):
        new_faces = []
        for face in faces:
            mid_indices = [midpoints[tuple(sorted([face[i], face[(i + 1) % 3]]))] for i in range(3)]
            new_faces.extend([
                [face[0], mid_indices[0], mid_indices[2]],
                [face[1], mid_indices[1], mid_indices[0]],
                [face[2], mid_indices[2], mid_indices[1]],
                [mid_indices[0], mid_indices[1], mid_indices[2]]
            ])
        return new_faces

    vertices, faces = read(full_path_input_mesh, is_ply=full_path_input_mesh.lower().endswith('.ply'))

    for _ in range(number_of_iterations):
        edges = [(face[i], face[(i + 1) % 3]) for face in faces for i in range(3)]
        midpoints = split_edges(vertices, edges)
        vertices = update_vertex_positions(vertices, faces, midpoints)
        faces = generate_new_faces(faces, midpoints)

    save(full_path_output_mesh, vertices, faces, is_ply=full_path_output_mesh.lower().endswith('.ply'))


if __name__ == '__main__':
    loop(
        full_path_input_mesh='icosahedron.off',
        number_of_iterations=5,
        full_path_output_mesh='loop-from-cube-3-iterations.off'
    )
