import numpy as np
import cv2

def read(path):
    with open(path, 'r') as file:
        header = file.readline().strip()
        assert header in {"OFF", "COFF", "NOFF", "STOFF"}, "Invalid file format"
        
        n_vertices, n_faces, _ = map(int, file.readline().strip().split())

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
    vertices,
    optical_center_x,
    optical_center_y,
    optical_center_z,
    optical_axis_x,
    optical_axis_y,
    optical_axis_z,
    focal_distance,
    output_width_in_pixels,
    output_height_in_pixels
):
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
    
    vertices_proj = vertices_cam[:, :2] * focal_distance / vertices_cam[:, 2, np.newaxis]
    
    vertices_image = vertices_proj.copy()
    vertices_image[:, 0] = (vertices_image[:, 0] + output_width_in_pixels / 2).astype(int)
    vertices_image[:, 1] = (output_height_in_pixels / 2 - vertices_image[:, 1]).astype(int)
    
    image = np.zeros((output_height_in_pixels, output_width_in_pixels, 3), dtype=np.uint8)
    
    x = vertices_image[:, 0]
    y = vertices_image[:, 1]
    valid = (0 <= x) & (x < output_width_in_pixels) & (0 <= y) & (y < output_height_in_pixels)
    x = x[valid].astype(int)
    y = y[valid].astype(int)
    colors = np.array(colors)
    colors = colors[valid]
    image[y, x] = colors
    
    return image

def sequence_of_projections(
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
    prefix_output_files
):
    vertices, faces = read(full_path_input_mesh)
    
    for i, (oc_x, oc_y, oc_z, oa_x, oa_y, oa_z) in enumerate(zip(
        optical_center_x, optical_center_y, optical_center_z,
        optical_axis_x, optical_axis_y, optical_axis_z
    )):
        image = project_points(
            vertices,
            oc_x,
            oc_y,
            oc_z,
            oa_x,
            oa_y,
            oa_z,
            focal_distance,
            output_width_in_pixels,
            output_height_in_pixels
        )
        output_path = f"{prefix_output_files}-{i+1}.png"
        cv2.imwrite(output_path, image)

def create_gif(
    prefix_output_files,
    n_images,
    duration,
    output_path
):
    import imageio
    images = []
    for i in range(n_images):
        images.append(imageio.imread(f"{prefix_output_files}-{i+1}.png"))
    imageio.mimsave(output_path, images, duration=duration)

if __name__ == "__main__":
    sequence_of_projections(
        full_path_input_mesh="meshes-for-exercises-1-2-3/bunny_mc.off",
        optical_center_x=np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])/2,
        optical_center_y=np.array([0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.20, 0.21])/3,
        optical_center_z=[-.2, -.2, -.2, -.2, -.2, -.2, -.2, -.2, -.2, -.2],
        optical_axis_x=[0,0,0,0,0,0,0,0,0,0],
        optical_axis_y=[0,0,0,0,0,0,0,0,0,0],
        optical_axis_z=[-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0],
        focal_distance=1000,
        output_width_in_pixels=1920, output_height_in_pixels=1080,
        prefix_output_files="bunny_animation"
    )
    
    create_gif(
        prefix_output_files="bunny_animation",
        n_images=10,
        duration=0.5,
        output_path="bunny.gif"
    )
