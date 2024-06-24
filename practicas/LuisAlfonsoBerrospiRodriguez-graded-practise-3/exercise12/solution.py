import numpy as np
from math import cos, radians
import cv2 as cv

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
            face = list(map(int, lines[i].strip().split()))[
                1:]  # Skip the first number (face size)
            faces.append(face)

    return vertices, faces


def calculate_normal(vertices, face):
    v0 = np.array(vertices[face[0]])
    v1 = np.array(vertices[face[1]])
    v2 = np.array(vertices[face[2]])
    return np.cross(v1 - v0, v2 - v0)


def project_to_plane(vertices):
    projected_vertices = []
    for vertex in vertices:
        vertex[2] = max(vertex[2], 1e-6)
        
        x_proj = vertex[0] / vertex[2]
        y_proj = vertex[1] / vertex[2]
        projected_vertices.append((x_proj, y_proj))
    return projected_vertices


def simple_cosine_illumination(
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
    # translate the mesh far from the camera
    # that takes an input polygonal mesh (with all its faces assumed to be white), and takes a
    # photo of it. The cammera is assumed to be in (0, 0, 0), the vision ray is assumed to be
    # (0, 0, 1), and the projection plane is z = 1.
    for i in range(len(vertices)):
        vertices[i][2] -= 1000
        
    # Project vertices to the plane
    projected_vertices = project_to_plane(vertices)
    
    # Create image
    image = np.zeros((height_in_pixels, width_in_pixels, 3), dtype=np.uint8)
    
    # Calculate the normal of each face
    normals = [calculate_normal(vertices, face) for face in faces]
    
    # Calculate the cosine of the angle between the normal and the vision ray
    cosines = [normal[2] for normal in normals]
    
    # Iterate over the faces
    
    for face, cosine in zip(faces, cosines):
        
        # Get the vertices of the face
        v0 = projected_vertices[face[0]]
        v1 = projected_vertices[face[1]]
        v2 = projected_vertices[face[2]]
        
        # Draw the face
        cv.fillPoly(image, [np.array([v0, v1, v2], np.int32)], (255, 255, 255 * cosine))
    
    # Save the image
    cv.imwrite(full_path_output_image, image)


simple_cosine_illumination(
    full_path_input_mesh="cube.off",
    full_path_output_image="photo-of-sphere.png",
    min_x_coordinate_in_projection_plane=-10.0,
    min_y_coordinate_in_projection_plane=-10.0,
    max_x_coordinate_in_projection_plane=10.0,
    max_y_coordinate_in_projection_plane=10.0,
    width_in_pixels=640,
    height_in_pixels=480
)
