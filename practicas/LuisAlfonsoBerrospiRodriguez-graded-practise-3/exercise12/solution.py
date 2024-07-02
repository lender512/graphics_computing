import numpy as np
import cv2

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

def normal(vertices, face):
    v0, v1, v2 = (np.array(vertices[i]) for i in face[:3])
    return np.cross(v1 - v0, v2 - v0)


def project_to_plane(vertices):
    plane = np.array([0, 0, 1])
    direction = np.array([0, 0, 0]) - vertices
    normal_projection = (np.dot(direction, plane) / np.linalg.norm(plane))[:, np.newaxis] * plane
    return vertices - normal_projection

def painter_algorithm_simple_cosine_illumination(
    full_path_input_mesh,
    full_path_output_image,
    min_x_coordinate_in_projection_plane,
    min_y_coordinate_in_projection_plane,
    max_x_coordinate_in_projection_plane,
    max_y_coordinate_in_projection_plane,
    width_in_pixels,
    height_in_pixels
):
    vertices, faces = read(full_path_input_mesh, is_ply=full_path_input_mesh.endswith(".ply") or full_path_input_mesh.endswith(".PLY"))
    
    normals = [normal(vertices, face) for face in faces]

    def max_distance(face):
        return max(np.linalg.norm(vertices[vertex]) for vertex in face)

    sorted_faces = sorted(faces, key=max_distance, reverse=True)

    image = np.zeros((height_in_pixels, width_in_pixels, 3), np.uint8) * 255

    for face in sorted_faces:
        v0, v1, v2 = (vertices[vertex] for vertex in face[:3])
        
        normal = normals[faces.index(face)]
        cos_alpha = abs(np.dot(normal, np.array([0, 0, -1])) / np.linalg.norm(normal))

        projected_vertices = project_to_plane(np.array([v0, v1, v2]))

        scaled_vertices = [
            (
                int((x - min_x_coordinate_in_projection_plane) / (max_x_coordinate_in_projection_plane - min_x_coordinate_in_projection_plane) * width_in_pixels),
                int((y - min_y_coordinate_in_projection_plane) / (max_y_coordinate_in_projection_plane - min_y_coordinate_in_projection_plane) * height_in_pixels)
            )
            for x, y in projected_vertices[:, :2]
        ]

        pts = np.array(scaled_vertices, np.int32).reshape((-1, 1, 2))

        color = tuple(int(255 * cos_alpha) for _ in range(3))
        cv2.fillPoly(image, [pts], color)

    cv2.imwrite(full_path_output_image, image)




painter_algorithm_simple_cosine_illumination(
    full_path_input_mesh="loop-from-cube-3-iterations.off",
    full_path_output_image="photo-of-sphere.png",
    min_x_coordinate_in_projection_plane=-2.0,
    min_y_coordinate_in_projection_plane=-2.0,
    max_x_coordinate_in_projection_plane=2.0,
    max_y_coordinate_in_projection_plane=2.0,
    width_in_pixels=480,
    height_in_pixels=480
)
