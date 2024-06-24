import numpy as np
import cv2

def load_off_mesh(file_path):
    vertices = []
    faces = []

    with open(file_path, 'r') as f:
        lines = f.readlines()
        vertex_count, face_count, _ = map(int, lines[1].strip().split())
        
        for i in range(2, 2 + vertex_count):
            vertex = list(map(float, lines[i].strip().split()))
            vertices.append(vertex)
        
        for i in range(2 + vertex_count, 2 + vertex_count + face_count):
            face = list(map(int, lines[i].strip().split()))[1:]  # Skip the first number (face size)
            faces.append(face)
    
    return vertices, faces

def calculate_normal(vertices, face):
    v0 = np.array(vertices[face[0]])
    v1 = np.array(vertices[face[1]])
    v2 = np.array(vertices[face[2]])
    return np.cross(v1 - v0, v2 - v0)

PLANE = np.array([0, 0, 1])
CAMERA = np.array([0, 0, 0])

def project_to_plane(vertices):
    direction_to_camera = CAMERA - vertices
    projection_along_normal = (np.dot(direction_to_camera, PLANE) / np.linalg.norm(PLANE))[:, np.newaxis] * PLANE
    projected_vertices = vertices - projection_along_normal
    
    return projected_vertices

def painter_algorithm_simple_cosine_illuminatio(
    full_path_input_mesh,
    full_path_output_image,
    min_x_coordinate_in_projection_plane,
    min_y_coordinate_in_projection_plane,
    max_x_coordinate_in_projection_plane,
    max_y_coordinate_in_projection_plane,
    width_in_pixels,
    height_in_pixels
):
    # Load mesh
    vertices, faces = load_off_mesh(full_path_input_mesh)
    
    # Calculate triangle normals
    normals = [calculate_normal(vertices, face) for face in faces]

    # Calculate maximum distance to origin for sorting
    def calculate_max_distance(face):
        return max(np.linalg.norm(vertices[face[0]]), np.linalg.norm(vertices[face[1]]), np.linalg.norm(vertices[face[2]]))

    # Sort faces by maximum distance
    sorted_faces = sorted(faces, key=calculate_max_distance, reverse=True)

    # Initialize image as white canvas
    image = np.zeros((height_in_pixels, width_in_pixels, 3), np.uint8) * 255

    # Project and draw triangles
    for face in sorted_faces:
        v0 = vertices[face[0]]
        v1 = vertices[face[1]]
        v2 = vertices[face[2]]

        # Calculate illumination (cosine of angle with respect to (0, 0, -1))
        normal = normals[faces.index(face)]
        cos_alpha = abs(np.dot(normal, np.array([0, 0, -1])) / np.linalg.norm(normal))

        # Project vertices to 2D plane
        projected_vertices = project_to_plane([v0, v1, v2])

        # Scale to image coordinates
        scaled_vertices = [
            (
                int((x - min_x_coordinate_in_projection_plane) / (max_x_coordinate_in_projection_plane - min_x_coordinate_in_projection_plane) * width_in_pixels),
                int((y - min_y_coordinate_in_projection_plane) / (max_y_coordinate_in_projection_plane - min_y_coordinate_in_projection_plane) * height_in_pixels)
            )
            for x, y in projected_vertices[:, :2]
        ]

        # Convert to OpenCV points format
        pts = np.array(scaled_vertices, np.int32)
        pts = pts.reshape((-1, 1, 2))

        # Draw filled triangle with adjusted color
        color = tuple(int(255 * cos_alpha) for _ in range(3))
        cv2.fillPoly(image, [pts], color)

    cv2.imwrite(full_path_output_image, image)




painter_algorithm_simple_cosine_illuminatio(
    full_path_input_mesh="loop-from-cube-3-iterations.off",
    full_path_output_image="photo-of-sphere.png",
    min_x_coordinate_in_projection_plane=-1.0,
    min_y_coordinate_in_projection_plane=-1.0,
    max_x_coordinate_in_projection_plane=1.0,
    max_y_coordinate_in_projection_plane=1.0,
    width_in_pixels=640,
    height_in_pixels=480
)
