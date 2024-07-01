def cube_with_square_faces(full_path_output_file):
    points = [
        [-1, -1, -1],
        [-1,  1, -1],
        [-1,  1,  1],
        [-1, -1,  1],
        [ 1, -1, -1],
        [ 1,  1, -1],
        [ 1,  1,  1],
        [ 1, -1,  1],
    ]
    
    faces = [
        [0, 3, 2, 1],
        [3, 7, 6, 2],
        [7, 4, 5, 6],
        [4, 0, 1, 5],
        [1, 2, 6, 5],
        [3, 0, 4, 7],
    ]

    def write(path, is_ply):
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
                    file.write(f"4 {' '.join(map(str, f))}\n")
        else:
            with open(path, 'w') as file:
                file.write("OFF\n")
                file.write(f"{len(points)} {len(faces)} 0\n")
                for point in points:
                    file.write(f"{' '.join(map(str, point))}\n")
                for face in faces:
                    file.write(f"4 {' '.join(map(str, face))}\n")
        
    
    write(full_path_output_file, (full_path_output_file.endswith('.ply') or full_path_output_file.endswith('.PLY')))


if __name__ == '__main__':
    cube_with_square_faces('cube.off')
    cube_with_square_faces('cube.ply')
