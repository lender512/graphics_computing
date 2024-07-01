import numpy as np

def sphere_with_quadrilateral_faces(full_path_output_file, radius, center):
    def get_v(r, center):
        vertices = []
        for phi in range(360):
            for theta in range(181):
                phi_rad = np.radians(phi)
                theta_rad = np.radians(theta)
                vertices.append([center[0] + r * np.sin(theta_rad) * np.cos(phi_rad), 
                                 center[1] + r * np.sin(theta_rad) * np.sin(phi_rad), 
                                 center[2] + r * np.cos(theta_rad)])
        return vertices

    def get_f():
        faces = []
        for phi in range(360):
            for theta in range(180):
                p1 = phi * 181 + theta
                p2 = p1 + 1
                p3 = ((phi + 1) % 360) * 181 + theta + 1
                p4 = ((phi + 1) % 360) * 181 + theta
                faces.append([p1, p2, p3, p4])
        return faces

    def save(path, vertices, faces, is_ply=False):
        if is_ply:
            with open(path, 'w') as file:
                file.write("ply\n")
                file.write("format ascii 1.0\n")
                file.write(f"element vertex {len(vertices)}\n")
                file.write("property float x\n")
                file.write("property float y\n")
                file.write("property float z\n")
                file.write(f"element face {len(faces)}\n")
                file.write("property list uchar int vertex_indices\n")
                file.write("end_header\n")
                for v in vertices:
                    file.write(f"{' '.join(map(str, v))}\n")
                for f in faces:
                    file.write(f"4 {' '.join(map(str, f))}\n")
        else:
            with open(path, 'w') as file:
                file.write("OFF\n")
                file.write(f"{len(vertices)} {len(faces)} 0\n")
                for v in vertices:
                    file.write(f"{' '.join(map(str, v))}\n")
                for f in faces:
                    file.write(f"4 {' '.join(map(str, f))}\n")
        
    save(full_path_output_file,
         get_v(radius, center),
         get_f(),
         full_path_output_file.lower().endswith('.ply'))

if __name__ == '__main__':
    sphere_with_quadrilateral_faces('sphere_squares.off', 1, [0, 0, 0])
    sphere_with_quadrilateral_faces('sphere_squares.ply', 1, [0, 0, 0])
