import math
import cv2

def read_ply(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    header = []
    vertices = []
    faces = []
    vertex_count = 0
    face_count = 0

    in_header = True

    for line in lines:
        if in_header:
            header.append(line.strip())
            if line.startswith('element vertex'):
                vertex_count = int(line.split()[-1])
            if line.startswith('element face'):
                face_count = int(line.split()[-1])
            if line.startswith('end_header'):
                header.append('property float texture_u')
                header.append('property float texture_v')
                in_header = False
        else:
            if vertex_count > 0:
                vertices.append([float(v) for v in line.strip().split()])
                vertex_count -= 1
            else:
                faces.append([int(f) for f in line.strip().split()[1:]])

    return header, vertices, faces

def write_ply(filename, header, vertices, faces, texture_u, texture_v):
    with open(filename, 'w') as file:
        for line in header:
            file.write(f"{line}\n")
        file.write('end_header\n')
        for i, vertex in enumerate(vertices):
            file.write(f"{vertex[0]} {vertex[1]} {vertex[2]} {texture_u[i]} {texture_v[i]}\n")
        for face in faces:
            file.write(f"4 {' '.join(map(str, face))}\n")

def sphere_with_texture(full_path_input_ply, full_path_texture, center, full_path_output_ply):
    # Read the PLY file manually
    header, vertices, faces, = read_ply(full_path_input_ply)
    
    cx, cy, cz = center
    texture_u = []
    texture_v = []

    # Load the texture to get dimensions using cv2
    texture_image = cv2.imread(full_path_texture)
    texture_height, texture_width, _ = texture_image.shape

    # Calculate texture coordinates for each vertex
    for vertex in vertices:
        vx, vy, vz = vertex

        # Calculate spherical coordinates
        phi = math.atan2(vy - cy, vx - cx)
        theta = math.acos((vz - cz) / math.sqrt((vx - cx)**2 + (vy - cy)**2 + (vz - cz)**2))

        # Normalize to texture coordinates
        u = (phi + math.pi) / (2 * math.pi)
        v = theta / math.pi

        # Scale texture coordinates by texture dimensions
        u_scaled = u * texture_width
        v_scaled = (1 - v) * texture_height  # v is flipped vertically

        texture_u.append(u_scaled)
        texture_v.append(v_scaled)

    # Write the updated PLY file manually
    write_ply(full_path_output_ply, header, vertices, faces, texture_u, texture_v)
# Example usage
sphere_with_texture(
    full_path_input_ply='sphere.ply',
    full_path_texture='texture1.png',
    center=(2, 3, 5),
    full_path_output_ply='sphere-with-texture-1.ply'
)
