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

def translate_mesh(full_path_input_mesh, d, full_path_output_mesh):
    dx, dy, dz = d

    if full_path_input_mesh.lower().endswith('.off'):
        vertices, faces = read_off(full_path_input_mesh)
    elif full_path_input_mesh.lower().endswith('.ply'):
        vertices, faces = read_ply(full_path_input_mesh)
    else:
        raise ValueError("Unsupported file format")


    
    # translated_vertices = [[x + dx, y + dy, z + dz] + vertex[3:] for vertex in vertices]
    #fix above
    translated_vertices = [[x + dx, y + dy, z + dz] for x, y, z in vertices]

    if full_path_output_mesh.lower().endswith('.off'):
        write_off(full_path_output_mesh, translated_vertices, faces)
    elif full_path_output_mesh.lower().endswith('.ply'):
        write_ply(full_path_output_mesh, translated_vertices, faces)

# Example usage
translate_mesh(
    full_path_input_mesh='sphere.off',
    d=(25, 2, 3),
    full_path_output_mesh='sphere-translated.off'
)