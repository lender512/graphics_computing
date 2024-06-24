import math

def sphere_with_quadrilateral_faces(full_path_output_file, radius, center):
    def generate_vertices(radius, center):
        vertices = []
        Cx, Cy, Cz = center
        for phi in range(360):
            for theta in range(181):  # Including 180 degrees
                phi_rad = math.radians(phi)
                theta_rad = math.radians(theta)
                x = Cx + radius * math.sin(theta_rad) * math.cos(phi_rad)
                y = Cy + radius * math.sin(theta_rad) * math.sin(phi_rad)
                z = Cz + radius * math.cos(theta_rad)
                vertices.append([x, y, z])
        return vertices

    def generate_faces():
        faces = []
        for phi in range(360):
            for theta in range(180):
                p1 = phi * 181 + theta
                p2 = p1 + 1
                p3 = ((phi + 1) % 360) * 181 + theta + 1
                p4 = ((phi + 1) % 360) * 181 + theta
                faces.append([p1, p2, p3, p4])
        return faces

    def save_off(file_path, vertices, faces):
        with open(file_path, 'w') as file:
            file.write("OFF\n")
            file.write(f"{len(vertices)} {len(faces)} 0\n")
            for vertex in vertices:
                file.write(f"{' '.join(map(str, vertex))}\n")
            for face in faces:
                file.write(f"4 {' '.join(map(str, face))}\n")

    def save_ply(file_path, vertices, faces):
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
                file.write(f"4 {' '.join(map(str, face))}\n")

    vertices = generate_vertices(radius, center)
    faces = generate_faces()

    if full_path_output_file.lower().endswith('.off'):
        save_off(full_path_output_file, vertices, faces)
    elif full_path_output_file.lower().endswith('.ply'):
        save_ply(full_path_output_file, vertices, faces)

# Example usage
sphere_with_quadrilateral_faces('sphere.off', 1, [0, 0, 0])
sphere_with_quadrilateral_faces('sphere.ply', 1, [0, 0, 0])
