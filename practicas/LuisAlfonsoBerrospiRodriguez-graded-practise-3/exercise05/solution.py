import numpy as np
import cv2

def read_ply(file_path):
    vertices = []
    faces = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        header = True
        for line in lines:
            if header:
                if line.startswith('end_header'):
                    header = False
            else:
                parts = line.strip().split()
                if len(parts) == 3:
                    vertices.append(tuple(map(float, parts)))
                elif len(parts) > 3:
                    faces.append(tuple(map(int, parts[1:])))
    return np.array(vertices), np.array(faces)

def write_ply(file_path, vertices, faces, texture_file):
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
        file.write("property list uchar int vertex_index\n")
        file.write("end_header\n")
        
        for vertex in vertices:
            file.write(f"{vertex[0]} {vertex[1]} {vertex[2]} {vertex[3]} {vertex[4]}\n")
        for face in faces:
            file.write(f"{len(face)} " + " ".join(map(str, face)) + "\n")
    
    # Write MeshLab MTL file
    with open(file_path.replace('.ply', '.mtl'), 'w') as mtl_file:
        mtl_file.write("newmtl material_0\n")
        mtl_file.write(f"map_Kd {texture_file}\n")

def sphere_with_texture(full_path_input_ply, full_path_texture, center, full_path_output_ply):
    vertices, faces = read_ply(full_path_input_ply)
    cx, cy, cz = center
    
    # Load texture to get size
    texture = cv2.imread(full_path_texture)
    tex_height, tex_width, _ = texture.shape
    
    texture_coords = []
    for vx, vy, vz in vertices:
        x = vx - cx
        y = vy - cy
        z = vz - cz
        
        r = np.sqrt(x**2 + y**2 + z**2)
        theta = np.arctan2(y, x)
        phi = np.arccos(z / r)
        
        # Calculate UV coordinates
        u = (theta + np.pi) / (2 * np.pi)
        v = (1 - phi / np.pi)
        
        # Scale by texture dimensions
        u *= tex_width
        v *= tex_height
        
        texture_coords.append((u, v))
    
    vertices_with_texture = np.hstack((vertices, np.array(texture_coords)))
    write_ply(full_path_output_ply, vertices_with_texture, faces, full_path_texture)

# Example usage
sphere_with_texture(
    full_path_input_ply='sphere_triangular.ply',
    full_path_texture='texture1.png',
    center=(2, 3, 5),
    full_path_output_ply='sphere-with-texture-1.ply'
)
