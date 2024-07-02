import numpy as np
import cv2

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

def detect_qr_code(image):
    # Simple edge detection
    edges = cv2.Canny(image, 100, 200)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # If the polygon has 4 vertices, we assume it's our QR code
        if len(approx) == 4:
            # set float32
            return approx.reshape(4, 2).astype(np.float32)
        
        

    raise ValueError("No QR code detected in the image")




def draw_mesh_on_top_of_marker(full_path_input_image, full_path_mesh, full_path_output_image):
    image = cv2.imread(full_path_input_image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    corners = detect_qr_code(gray)

    # Find the rotation and translation vectors.
    ret, rvecs, tvecs = cv2.solvePnP(
        objectPoints=np.float32([[0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 0, 0]]),
        imagePoints=corners.reshape(-1, 1, 2),
        cameraMatrix=np.eye(3),
        distCoeffs=np.zeros(4)
    )
    
    # project 3D points to image plane
    axis = np.float32([[1,0,0], [0,1,0], [0,0,-1]]).reshape(-1,3)
    imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, np.eye(3), np.zeros(5))
    imgpts = imgpts.astype(np.int32)
    print(imgpts[0])
    for i in range(2):
        cv2.line(image, tuple(imgpts[0].ravel()), tuple(imgpts[i].ravel()), (0,0,255), 3)
    
   # Load the image
    image = cv2.imread(full_path_input_image)
    if image is None:
        raise ValueError(f"Image at {full_path_input_image} could not be loaded.")
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    try:
        qr_corners = detect_qr_code(gray_image)
    except ValueError as e:
        print(e)
        return
    qr_code_size = 1.0
    # Define the 3D coordinates of the QR code corners in the real world
    qr_code_3d_points = np.array([
        [0, 0, 0],
        [qr_code_size, 0, 0],
        [qr_code_size, qr_code_size, 0],
        [0, qr_code_size, 0]
    ], dtype=np.float32)

    # Camera intrinsic parameters (these should be calibrated for your specific camera)
    # fx, fy, cx, cy
    camera_matrix = np.array([
        [800, 0, 320],
        [0, 800, 240],
        [0, 0, 1]
    ], dtype=np.float32)

    # Assume no lens distortion
    dist_coeffs = np.zeros((4, 1)) 

    # Solve PnP to find the rotation and translation vectors
    success, rvec, tvec = cv2.solvePnP(qr_code_3d_points, qr_corners, camera_matrix, dist_coeffs)

    if not success:
        raise ValueError("Could not solve PnP")

    # Project the 3D points to 2D image points to verify the pose estimation
    projected_points, _ = cv2.projectPoints(qr_code_3d_points, rvec, tvec, camera_matrix, dist_coeffs)

    # Draw the projected points on the image
    # for point in projected_points:
    #     cv2.circle(image, tuple(point[0].astype(int)), 5, (0, 255, 0), -1)

    # Draw the detected QR code corners on the image
    for corner in qr_corners:
        cv2.circle(image, tuple(corner.astype(int)), 5, (0, 0, 255), -1)
        
    # draw cube on top of the marker
    
    # Define the 3D coordinates of the cube vertices in the real world
    cube_3d_points = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 1, 1]
    ], dtype=np.float32)
    
    # Define the 3D coordinates of the cube edges
    cube_edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]
    
    # Project the cube vertices to 2D image points
    projected_points, _ = cv2.projectPoints(cube_3d_points, rvec, tvec, camera_matrix, dist_coeffs)
    
    # Draw the cube edges on the image
    for edge in cube_edges:
        cv2.line(image, tuple(projected_points[edge[0]][0].astype(int)), tuple(projected_points[edge[1]][0].astype(int)), (255, 0, 0), 2)
        
        


    cv2.imwrite(full_path_output_image, image)


if __name__ == "__main__":
    draw_mesh_on_top_of_marker(
        full_path_input_image="photo.jpg",
        full_path_mesh="meshes-for-exercises-1-2-3/cubo.off",
        full_path_output_image="output.jpg"
    )
