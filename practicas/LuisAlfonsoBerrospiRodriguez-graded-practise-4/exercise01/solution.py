import numpy as np
import cv2
import time


def read(path):
    with open(path, 'r') as file:
        # Read the first two lines to get the header and counts
        header = file.readline().strip()
        assert header in {"OFF", "COFF", "NOFF", "STOFF"}, "Invalid file format"
        
        n_vertices, n_faces, _ = map(int, file.readline().strip().split())

        # Initialize the lists with pre-allocated sizes
        vertices = [None] * n_vertices
        faces = [None] * n_faces
        uv = [] if header == "STOFF" else None
        
        for i in range(n_vertices):
            line = file.readline().strip().split()
            if header == "STOFF":
                vertices[i] = list(map(float, line[:3]))
                uv.append(list(map(float, line[3:])))
            else:
                vertices[i] = list(map(float, line))

    return vertices, faces

def project_points(
    full_path_input_mesh,
    optical_center_x,
    optical_center_y,
    optical_center_z,
    optical_axis_x,
    optical_axis_y,
    optical_axis_z,
    focal_distance,
    output_width_in_pixels,
    output_height_in_pixels,
    full_path_output
):
    # start = time.time()

    vertices, faces = read(full_path_input_mesh)
    # print(f"Time taken to read: {time.time() - start:.2f} seconds")
    
    colors = np.ones((len(vertices), 3), dtype=np.uint8) * 255
    
    optical_center = np.array([optical_center_x, optical_center_y, optical_center_z])
    optical_axis = np.array([optical_axis_x, optical_axis_y, optical_axis_z])
    optical_axis = optical_axis / np.linalg.norm(optical_axis)  # Normalize
    
    up = np.array([0, 1, 0])  # Assuming 'up' is along y-axis
    right = np.cross(optical_axis, up)
    up = np.cross(right, optical_axis)
    
    cam_to_world = np.column_stack((right, up, -optical_axis, optical_center))
    cam_to_world = np.vstack((cam_to_world, [0, 0, 0, 1]))
    
    world_to_cam = np.linalg.inv(cam_to_world)
    
    vertices_homogeneous = np.column_stack((vertices, np.ones(len(vertices))))
    vertices_cam = np.dot(world_to_cam, vertices_homogeneous.T).T[:, :3]
    
    # Project points
    vertices_proj = vertices_cam[:, :2] * focal_distance / vertices_cam[:, 2, np.newaxis]
    
    # Scale to image coordinates
    vertices_image = vertices_proj.copy()
    vertices_image[:, 0] = (vertices_image[:, 0] + output_width_in_pixels / 2).astype(int)
    vertices_image[:, 1] = (output_height_in_pixels / 2 - vertices_image[:, 1]).astype(int)
    
    # Create image and draw points
    image = np.zeros((output_height_in_pixels, output_width_in_pixels, 3), dtype=np.uint8)
    
    x = vertices_image[:, 0]
    y = vertices_image[:, 1]
    valid = (0 <= x) & (x < output_width_in_pixels) & (0 <= y) & (y < output_height_in_pixels)
    x = x[valid].astype(int)
    y = y[valid].astype(int)
    colors = np.array(colors)
    colors = colors[valid]
    image[y, x] = colors
    
        
    
    # Save the image
    cv2.imwrite(full_path_output, image)
    
if __name__ == "__main__":
    project_points(
        "meshes-for-exercises-1-2-3/bunny_mc.off",
        .0, 0.12, -.1,
        0, 0, -1.0,
        500,
        1920, 1080,
        "bunny.png"
    )