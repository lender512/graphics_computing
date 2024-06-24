import math

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
        file.write("property float u\n")
        file.write("property float v\n")
        file.write(f"element face {len(faces)}\n")
        file.write("property list uchar int vertex_indices\n")
        file.write("end_header\n")
        for vertex in vertices:
            file.write(f"{' '.join(map(str, vertex))}\n")
        for face in faces:
            file.write(f"3 {' '.join(map(str, face))}\n")

def sphere_with_texture(full_path_input_ply, full_path_texture, center, full_path_output_ply):
    vertices, faces = read_ply(full_path_input_ply)
    Cx, Cy, Cz = center

    # Calculate texture coordinates
    for vertex in vertices:
        x, y, z = vertex[:3]
        theta = math.atan2(y - Cy, x - Cx)
        phi = math.acos((z - Cz) / math.sqrt((x - Cx)**2 + (y - Cy)**2 + (z - Cz)**2))
        u = (theta + math.pi) / (2 * math.pi)
        v = phi / math.pi
        vertex.extend([u, v])

    write_ply(full_path_output_ply, vertices, faces)

# Example usage
sphere_with_texture(
    full_path_input_ply='sphere_triangular.ply',
    full_path_texture='texture2.png',
    center=(2, 3, 5),
    full_path_output_ply='sphere-with-texture-1.ply'
)
