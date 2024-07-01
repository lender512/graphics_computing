import numpy as np
import math

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
                file.write(f"3 {' '.join(map(str, f))}\n")
    else:
        with open(path, 'w') as file:
            file.write("OFF\n")
            file.write(f"{len(vertices)} {len(faces)} 0\n")
            for v in vertices:
                file.write(f"{' '.join(map(str, v))}\n")
            for f in faces:
                file.write(f"{len(f)} {' '.join(map(str, f))}\n")

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


def face_normal(vertices, face):
    normalize = lambda v: v / np.linalg.norm(v)
    v0, v1, v2 = [np.array(vertices[face[i]]) for i in range(3)]
    edge1 = v1 - v0
    edge2 = v2 - v0
    return normalize(np.cross(edge1, edge2))

def orient_face(vertices, face):
    normal = face_normal(vertices, face)
    center = np.mean([vertices[v] for v in face], axis=0)
    if np.dot(normal, center) < 0:
        return face[::-1]
    return face

def catmull_clark(full_path_input_mesh, number_of_iterations, full_path_output_mesh):
    vertices, faces = read(full_path_input_mesh, is_ply=full_path_input_mesh.endswith(".ply") or full_path_input_mesh.endswith(".PLY"))
    
    for _ in range(number_of_iterations):
        updated_vertices = vertices.copy()
        edge_points = {}
        face_centroids = []

        for face in faces:
            centroid = np.mean([vertices[v] for v in face], axis=0)
            face_centroids.append(centroid)
            updated_vertices.append(centroid)

        for face in faces:
            for i in range(len(face)):
                v1, v2 = sorted((face[i], face[(i + 1) % len(face)]))
                if (v1, v2) not in edge_points:
                    midpoint_value = np.mean([vertices[v1], vertices[v2]], axis=0)
                    edge_points[(v1, v2)] = len(updated_vertices)
                    updated_vertices.append(midpoint_value)

        for index, vertex in enumerate(vertices):
            num_adjacent_faces = 0
            face_sum = [0, 0, 0]
            edge_sum = [0, 0, 0]

            for face in faces:
                if index in face:
                    num_adjacent_faces += 1
                    face_index = faces.index(face)
                    face_sum = np.add(face_sum, face_centroids[face_index])

                    prev_vertex = face[(face.index(index) - 1) % len(face)]
                    next_vertex = face[(face.index(index) + 1) % len(face)]
                    edge1_index = edge_points[(min(index, prev_vertex), max(index, prev_vertex))]
                    edge2_index = edge_points[(min(index, next_vertex), max(index, next_vertex))]
                    edge_sum = [edge_sum[j] + updated_vertices[edge1_index][j] + updated_vertices[edge2_index][j] for j in range(3)]

            face_average = [x / num_adjacent_faces for x in face_sum]
            edge_average = [x / (2 * num_adjacent_faces) for x in edge_sum]
            vertex_adjustment = [vertex[j] * (num_adjacent_faces - 3) for j in range(3)]
            updated_vertices[index] = [(face_average[j] + 2 * edge_average[j] + vertex_adjustment[j]) / num_adjacent_faces for j in range(3)]

        new_faces = []
        for face in faces:
            face_centroid_index = len(vertices) + faces.index(face)
            num_vertices = len(face)
            for i in range(num_vertices):
                v1 = face[i]
                v2 = face[(i + 1) % num_vertices]
                edge1_index = edge_points[(min(v1, v2), max(v1, v2))]
                edge2_index = edge_points[(min(v1, face[i - 1]), max(v1, face[i - 1]))]
                new_face = [v1, edge1_index, face_centroid_index, edge2_index]
                new_faces.append(orient_face(updated_vertices, new_face))

        vertices = updated_vertices
        faces = new_faces

    for i, vertex in enumerate(vertices):
        vertices[i] = vertex / np.linalg.norm(vertex)

    faces = [orient_face(vertices, face) for face in faces]
    
    save(full_path_output_mesh, vertices, faces, is_ply=full_path_output_mesh.endswith(".ply") or full_path_output_mesh.endswith(".PLY"))

if __name__ == "__main__":
    catmull_clark(
        full_path_input_mesh="cube.off",
        number_of_iterations=5,
        full_path_output_mesh="catmull-clark-from-tetraedro-3-iterations.off"
    )