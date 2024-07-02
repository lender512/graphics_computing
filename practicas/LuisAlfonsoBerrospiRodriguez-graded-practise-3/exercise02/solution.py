def cube_with_triangular_faces(full_path_output_file):
    points = [
        [-1, -1, -1],
        [-1, 1, -1],
        [-1, 1, 1],
        [-1, -1, 1],
        [1, -1, -1],
        [1, 1, -1],
        [1, 1, 1],
        [1, -1, 1]
    ]
    
    faces = [
        [0, 3, 1],
        [3, 2, 1],
        [3, 7, 2],
        [7, 6, 2],
        [7, 4, 6],
        [4, 5, 6],
        [4, 0, 5],
        [0, 1, 5],
        [1, 2, 5],
        [2, 6, 5],
        [3, 0, 7],
        [0, 4, 7]
    ]

    def save(path, is_ply):
        if is_ply:
            with open(path, 'w') as file:
                file.write("ply\n")
                file.write("format ascii 1.0\n")
                file.write(f"element vertex {len(points)}\n")
                file.write("property float x\n")
                file.write("property float y\n")
                file.write("property float z\n")
                file.write(f"element face {len(faces)}\n")
                file.write("property list uchar int vertex_indices\n")
                file.write("end_header\n")
                for p in points:
                    file.write(f"{' '.join(map(str, p))}\n")
                for f in faces:
                    file.write(f"{len(f)} {' '.join(map(str, f))}\n")
        else:
            with open(path, 'w') as file:
                file.write("OFF\n")
                file.write(f"{len(points)} {len(faces)} 0\n")
                for p in points:
                    file.write(f"{' '.join(map(str, p))}\n")
                for f in faces:
                    file.write(f"{len(f)} {' '.join(map(str, f))}\n")
    
    save(full_path_output_file, (full_path_output_file.endswith('.ply') or full_path_output_file.endswith('.PLY')))

if __name__ == '__main__':
    cube_with_triangular_faces('cube_triangular.off')
    cube_with_triangular_faces('cube_triangular.ply')
