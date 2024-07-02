import numpy as np
import cv2

def read_ply_with_texture(path):
    vertices = []
    faces = []
    texture_coords = []
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
                        parts = list(map(float, line.strip().split()))
                        vertices.append(parts[:3])
                        texture_coords.append(parts[3:5])
                        vertex_count -= 1
                        if vertex_count == 0:
                            reading_vertices = False
                            reading_faces = True
                elif reading_faces:
                    if face_count > 0:
                        faces.append(list(map(int, line.strip().split()[1:])))
                        face_count -= 1
    
    return np.array(vertices), np.array(faces), np.array(texture_coords)

def project_vertex(vertex, min_x, min_y, max_x, max_y, width, height):
    x, y, z = vertex
    if z == 0:
        z = 0.0001
    px = x / z
    py = y / z
    screen_x = int((px - min_x) / (max_x - min_x) * width)
    screen_y = int((py - min_y) / (max_y - min_y) * height)
    return screen_x, screen_y

def barycentric_coordinates(p, a, b, c):
    v0 = b - a
    v1 = c - a
    v2 = p - a
    d00 = np.dot(v0, v0)
    d01 = np.dot(v0, v1)
    d11 = np.dot(v1, v1)
    d20 = np.dot(v2, v0)
    d21 = np.dot(v2, v1)
    denom = d00 * d11 - d01 * d01
    if abs(denom) < 1e-6:
        return -1, -1, -1
    v = (d11 * d20 - d01 * d21) / denom
    w = (d00 * d21 - d01 * d20) / denom
    u = 1.0 - v - w
    return u, v, w

def painter_algorithm_textures(full_path_input_mesh, full_path_input_texture, full_path_output_image,
                               min_x, min_y, max_x, max_y, width, height):
    vertices, faces, texture_coords = read_ply_with_texture(full_path_input_mesh)
    texture = cv2.imread(full_path_input_texture)
    
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    sorted_faces = sorted(faces, key=lambda f: max(np.linalg.norm(vertices[v]) for v in f), reverse=True)
    
    for face in sorted_faces:
        v1, v2, v3 = vertices[face]
        t1, t2, t3 = texture_coords[face]
        
        p1 = project_vertex(v1, min_x, min_y, max_x, max_y, width, height)
        p2 = project_vertex(v2, min_x, min_y, max_x, max_y, width, height)
        p3 = project_vertex(v3, min_x, min_y, max_x, max_y, width, height)
        
        min_x_bb = max(0, min(p1[0], p2[0], p3[0]))
        max_x_bb = min(width - 1, max(p1[0], p2[0], p3[0]))
        min_y_bb = max(0, min(p1[1], p2[1], p3[1]))
        max_y_bb = min(height - 1, max(p1[1], p2[1], p3[1]))
        
        for y in range(min_y_bb, max_y_bb + 1):
            for x in range(min_x_bb, max_x_bb + 1):
                u, v, w = barycentric_coordinates(np.array([x, y]), np.array(p1), np.array(p2), np.array(p3))
                
                if u >= 0 and v >= 0 and w >= 0:
                    tx = u * t1[0] + v * t2[0] + w * t3[0]
                    ty = u * t1[1] + v * t2[1] + w * t3[1]
                    
                    tx = int(tx * texture.shape[1]) % texture.shape[1]
                    ty = int(ty * texture.shape[0]) % texture.shape[0]
                    color = texture[ty, tx]
                    
                    image[y, x] = color
    
    cv2.imwrite(full_path_output_image, image)

painter_algorithm_textures(
    full_path_input_mesh='sphere-with-texture-1.ply',
    full_path_input_texture='texture1.png',
    full_path_output_image='photo-of-sphere.png',
    min_x=-1.0,
    min_y=-1.0,
    max_x=1.0,
    max_y=1.0,
    width=640,
    height=480
)