import math
import numpy as np
import cv2

def read(path):
    vertices = []
    faces = []
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
    
    return vertices, faces

def save(path, vertices, faces, texture_coords):
    with open(path, 'w') as file:
        file.write("ply\n")
        file.write("format ascii 1.0\n")
        file.write(f"element vertex {len(vertices)}\n")
        file.write("property float x\n")
        file.write("property float y\n")
        file.write("property float z\n")
        file.write("property float s\n")
        file.write("property float t\n")
        file.write(f"element face {len(faces)}\n")
        file.write("property list uchar int vertex_indices\n")
        file.write("end_header\n")
        for v, tc in zip(vertices, texture_coords):
            file.write(f"{' '.join(map(str, v))} {tc[0]} {tc[1]}\n")
        for f in faces:
            file.write(f"{len(f)} {' '.join(map(str, f))}\n")

def calculate_texture_coords(vertices, center, texture_size):
    texture_coords = []
    width, height = texture_size
    aspect_ratio = width / height

    for v in vertices:
        v_rel = np.array(v) - np.array(center)
        
        theta = math.atan2(v_rel[1], v_rel[0])
        phi = math.atan2(math.sqrt(v_rel[0]**2 + v_rel[1]**2), v_rel[2])
        
        s = (theta + math.pi) / (2 * math.pi)
        t = phi / math.pi
        
        s = s * aspect_ratio
        
        s = s % 1.0
        t = 1 - t
        
        texture_coords.append([s, t])
    
    return texture_coords

def sphere_with_texture(full_path_input_ply, full_path_texture, center, full_path_output_ply):
    vertices, faces = read(full_path_input_ply)
    
    texture_image = cv2.imread(full_path_texture)
    texture_size = texture_image.shape[1], texture_image.shape[0]
    
    texture_coords = calculate_texture_coords(vertices, center, texture_size)
    
    save(full_path_output_ply, vertices, faces, texture_coords)

if __name__ == '__main__':
    sphere_with_texture(
        full_path_input_ply='sphere_triangular.ply',
        full_path_texture='texture1.png',
        center=(2,3,5),
        full_path_output_ply='sphere-with-texture-1.ply'
    )