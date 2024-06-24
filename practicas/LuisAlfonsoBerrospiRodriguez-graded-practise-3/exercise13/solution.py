import numpy as np
import cv2

def load_off_mesh(file_path):
    vertices = []
    faces = []
    texcoords = []  # List to store UV coordinates

    with open(file_path, 'r') as f:
        lines = f.readlines()
        vertex_count, face_count, _ = map(int, lines[1].strip().split())
        
        for i in range(2, 2 + vertex_count):
            data = list(map(float, lines[i].strip().split()))
            vertices.append(data[:3])  # Vertex coordinates
            texcoords.append(data[3:])  # UV coordinates
        
        for i in range(2 + vertex_count, 2 + vertex_count + face_count):
            face = list(map(int, lines[i].strip().split()))[1:]  # Skip the first number (face size)
            faces.append(face)
    
    return vertices, faces, texcoords

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

def painter_algorithm_simple_cosine_illumination(
    full_path_input_mesh,
    full_path_texture_image,
    full_path_output_image,
    min_x_coordinate_in_projection_plane,
    min_y_coordinate_in_projection_plane,
    max_x_coordinate_in_projection_plane,
    max_y_coordinate_in_projection_plane,
    width_in_pixels,
    height_in_pixels
):
    # Load mesh and UV coordinates
    vertices, faces, texcoords = load_off_mesh(full_path_input_mesh)
    #rotate the mesh
    
    # Load texture image
    texture_image = cv2.imread(full_path_texture_image)
    
    # Calculate triangle normals
    normals = [calculate_normal(vertices, face) for face in faces]

    # Calculate maximum distance to origin for sorting
    def calculate_max_distance(face):
        return max(np.linalg.norm(vertices[face[0]]), np.linalg.norm(vertices[face[1]]), np.linalg.norm(vertices[face[2]]))

    # Sort faces by maximum distance
    sorted_faces = sorted(faces, key=calculate_max_distance, reverse=True)

    # Initialize image as white canvas
    image = np.ones((height_in_pixels, width_in_pixels, 3), np.uint8) * 255

    # Project and draw textured triangles
    for face in sorted_faces:
        v0 = vertices[face[0]]
        v1 = vertices[face[1]]
        v2 = vertices[face[2]]

        # Get UV coordinates for the vertices
        uv0 = texcoords[face[0]]
        uv1 = texcoords[face[1]]
        uv2 = texcoords[face[2]]

        # Calculate illumination (cosine of angle with respect to (0, 0, -1))
        normal = normals[faces.index(face)]
        cos_alpha = abs(np.dot(normal, np.array([0, 0, -1])) / np.linalg.norm(normal))

        # Project vertices to 2D plane
        projected_vertices = project_to_plane(np.array([v0, v1, v2]))

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

        # Define corresponding UV coordinates
        uvs = np.array([uv0, uv1, uv2], np.float32)

        # Get bounding box of the triangle
        rect = cv2.boundingRect(pts)

        # Get the ROI in the texture image
        x, y, w, h = rect
        tex_roi = texture_image[y:y+h, x:x+w]

        # Create mask for the triangle
        mask = np.zeros((h, w), np.uint8)
        tri_pts = np.array([[scaled_vertices[i][0] - x, scaled_vertices[i][1] - y] for i in range(3)], np.int32)
        cv2.fillConvexPoly(mask, tri_pts, 255)

        # Warp the texture to the triangle
        src_tri = np.array(uvs, np.float32)
        dst_tri = np.array(tri_pts, np.float32)
        warp_mat = cv2.getAffineTransform(src_tri, dst_tri)
        warped_texture = cv2.warpAffine(tex_roi, warp_mat, (w, h))

        # Apply the mask to the warped texture
        warped_texture = cv2.bitwise_and(warped_texture, warped_texture, mask=mask)

        # Overlay the warped texture onto the image
        image_roi = image[y:y+h, x:x+w]
        image_bg = cv2.bitwise_and(image_roi, image_roi, mask=cv2.bitwise_not(mask))
        image_roi = cv2.add(image_bg, warped_texture)
        image[y:y+h, x:x+w] = image_roi

    cv2.imwrite(full_path_output_image, image)


# Example usage:
painter_algorithm_simple_cosine_illumination(
    full_path_input_mesh="icosahedron.off",
    full_path_texture_image="texture1.png",
    full_path_output_image="photo-of-sphere-texture.png",
    min_x_coordinate_in_projection_plane=-1.0,
    min_y_coordinate_in_projection_plane=-1.0,
    max_x_coordinate_in_projection_plane=1.0,
    max_y_coordinate_in_projection_plane=1.0,
    width_in_pixels=640,
    height_in_pixels=480
)
