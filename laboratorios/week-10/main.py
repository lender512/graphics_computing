import numpy as np
import matplotlib.pyplot as plt


        

def marching_squares(f, output_filename, xmin, ymin, xmax, ymax, precision):
    def marching_squares_u(f, xmin, ymin, xmax, ymax, precision, lines):
        xmid = (xmin + xmax) / 2
        ymid = (ymin + ymax) / 2
        
        f00 = f(xmin, ymin)
        f10 = f(xmax, ymin)
        f01 = f(xmin, ymax)
        f11 = f(xmax, ymax)
                
        square = (f01 > 0, f11 > 0, f00 > 0, f10 > 0)
        
                    
        if square in [(True, True, True, True)]:
            if not check_if_function_changes_sign_in_square(f, xmin, ymin, xmax, ymax):
                return
        if square in [(False, False, False, False)]:    
            if not check_if_function_changes_sign_in_square(f, xmin, ymin, xmax, ymax):
                return
        if ((xmax - xmin )< precision) and (ymax - ymin < precision):
            if square in [(False, False, False, True), (True, True, True, False)]:
                lines.append(((xmid, ymin), (xmax, ymid)))
            if square in [(True, False, False, False), (False, True, True, True)]:
                lines.append(((xmin, ymid), (xmid, ymax)))
            if square in [(False, True, False, False), (True, False, True, True)]:
                lines.append(((xmid, ymax), (xmax, ymid)))
            if square in [(False, False, True, False), (True, True, False, True)]:
                lines.append(((xmin, ymid), (xmid, ymin)))
            if square in [(True, False, True, False), (False, True, False, True)]:
                lines.append(((xmid, ymin), (xmid, ymax)))
            if square in [(True, True, False, False),(False, False, True, True)]:
                lines.append(((xmin, ymid), (xmax, ymid)))
            if square in [(True, False, False, True)]:
                lines.append(((xmin, ymid), (xmid, ymin)))
                lines.append(((xmid, ymax), (xmax, ymid)))
            if square in [(False, True, True, False)]:
                lines.append(((xmin, ymid), (xmid, ymax)))
                lines.append(((xmid, ymin), (xmax, ymid)))
            return
                
        marching_squares_u(f, xmin, ymin, xmid, ymid, precision, lines)
        marching_squares_u(f, xmin, ymid, xmid, ymax, precision, lines)
        marching_squares_u(f, xmid, ymin, xmax, ymid, precision, lines)
        marching_squares_u(f, xmid, ymid, xmax, ymax, precision, lines)
    
    lines = []
    marching_squares_u(f, xmin, ymin, xmax, ymax, precision, lines)
    
    #save plt to eps
    
    plt.axis('equal')
    for line in lines:
        plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], 'k-')
    plt.axis('off')
    plt.savefig(output_filename, format='eps')
    # plt.show()        
                
def f(x, y):
    return float(x)**2 + float(y)**2 - 1000

def rotate_point(points_3d, pivot_3d, angle_3d):
    #use numpy
    points_3d = np.array(points_3d)
    pivot_3d = np.array(pivot_3d)
    angle_3d = np.array(angle_3d)
    
    # Translate the points so that the pivot is at the origin
    points_3d = points_3d - pivot_3d
    
    # Convert the angles to radians
    angle_3d = np.radians(angle_3d)
    angle_x = angle_3d[0]
    angle_y = angle_3d[1]
    angle_z = angle_3d[2]
    
    rotation_x = np.array([[1, 0, 0],
                           [0, np.cos(angle_x), -np.sin(angle_x)],
                           [0, np.sin(angle_x), np.cos(angle_x)]])
    
    rotation_y = np.array([[np.cos(angle_y), 0, np.sin(angle_y)],
                           [0, 1, 0],
                           [-np.sin(angle_y), 0, np.cos(angle_y)]])
    
    rotation_z = np.array([[np.cos(angle_z), -np.sin(angle_z), 0],
                           [np.sin(angle_z), np.cos(angle_z), 0],
                           [0, 0, 1]])
    
    # Combine the rotations
    rotation_matrix = np.dot(np.dot(rotation_x, rotation_y), rotation_z)
    
    # Rotate the points
    rotated_points = np.dot(points_3d, rotation_matrix.T)
    
    # Translate the points back
    rotated_points = rotated_points + pivot_3d
    
    return rotated_points.tolist()


    
def setup_case(case, midpoint ,rotation, color = 'k'):
    for i in range(len(case)):
        case[i] = rotate_point(case[i], midpoint, rotation)
    return case, color

def check_if_function_changes_sign_in_square(f, xmin, ymin, xmax, ymax):
    N = 500
    points = np.random.rand(N, 2)
    points = points * np.array([xmax - xmin, ymax - ymin]) + np.array([xmin, ymin])
    first_sign = f(points[0][0], points[0][1]) > 0
    for point in points:
        if (f(point[0], point[1]) > 0) != first_sign:
            return True
        

def check_if_function_changes_sign_in_box(f, xmin, ymin, zmin, xmax, ymax, zmax):

    N = 500
    points = np.random.rand(N, 3)
    points = points * np.array([xmax - xmin, ymax - ymin, zmax - zmin]) + np.array([xmin, ymin, zmin])
    first_sign = f(points[0][0], points[0][1], points[0][2]) > 0
    for point in points:
        if (f(point[0], point[1], point[2]) > 0) != first_sign:
            return True

def to_OFF(faces, filename):
    
    def get_index(vertex, vertices):
        for i in range(len(vertices)):
            if vertices[i][0] == vertex[0] and vertices[i][1] == vertex[1] and vertices[i][2] == vertex[2]:
                return i
        return -1
    
    #sort each vertex of each face by counter clockwise
    for i in range(len(faces)):
        face = faces[i]
        face = np.array(face)
        center = np.mean(face, axis = 0)
        angles = np.arctan2(face[:, 1] - center[1], face[:, 0] - center[0])
        face = face[np.argsort(angles)]
        faces[i] = face.tolist()
    
    vertices = []
    for face in faces:
        for vertex in face:
            if vertex not in vertices:
                vertices.append(vertex)
    vertices = np.array(vertices)
    faces = np.array(faces)
    with open(filename, 'w') as f:
        f.write('OFF\n')
        f.write(f'{len(vertices)} {len(faces)} 0\n')
        for vertex in vertices:
            f.write(f'{vertex[0]} {vertex[1]} {vertex[2]}\n')
        for face in faces:
            f.write(f'{len(face)} {" ".join([str(get_index(vertex, vertices)) for vertex in face])}\n')
            
def rotate_z_curve(cube, angle_x, angle_y, angle_z):

    
    # Define the original coordinates of the Z-order curve
    coords = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [0, 1, 0],
        [1, 1, 0],
        [0, 0, 1],
        [1, 0, 1],
        [0, 1, 1],
        [1, 1, 1]
    ])
    
    rotated_coords = rotate_point(coords, (0.5, 0.5, 0.5), (angle_x, angle_y, angle_z))
    
    # Move the boolean values to the new coordinates
    rotated_cube = np.zeros(8, dtype=bool)
    for i in range(8):
        x = int(rotated_coords[i][0] + 0.5)
        y = int(rotated_coords[i][1] + 0.5)
        z = int(rotated_coords[i][2] + 0.5)
        rotated_cube[i] = cube[x + 2*y + 4*z]
        
    
    return np.array(rotated_cube)

def marching_cubes_u(f, xmin, ymin, zmin, xmax, ymax, zmax, precision, faces, colors):
        xmid = (xmin + xmax) / 2
        ymid = (ymin + ymax) / 2
        zmid = (zmin + zmax) / 2
        
        f000 = f(xmin, ymin, zmin)
        f100 = f(xmax, ymin, zmin)
        f010 = f(xmin, ymax, zmin)
        f110 = f(xmax, ymax, zmin)
        f001 = f(xmin, ymin, zmax)
        f101 = f(xmax, ymin, zmax)
        f011 = f(xmin, ymax, zmax)
        f111 = f(xmax, ymax, zmax)
        
        #check if the function changes sign in the box
        
        
        #cube is a list of 8 boolean values
        # front face:
        # f001----f101
        #  |       |
        #  |       |
        # f000----f100
        # back face:
        # f011----f111
        #  |       |
        #  |       |
        # f010----f110
        
        
    
        #create cube in z space filling curve
        cube = np.array([f000 > 0, f100 > 0, f010 > 0, f110 > 0, f001 > 0, f101 > 0, f011 > 0, f111 > 0])
        cube_str = ''.join([str(int(i)) for i in cube])
        cube_str = cube_str[:4] + '_' + cube_str[4:]
        cube_n_str = ''.join([str(int(not i)) for i in cube])
        cube_n_str = cube_n_str[:4] + '_' + cube_n_str[4:]
        #check if is less than precision
        
        if np.all(cube) or np.all(~cube):
            if not check_if_function_changes_sign_in_box(f, xmin, ymin, zmin, xmax, ymax, zmax):
                return
        
        if ((xmax - xmin )< precision) and (ymax - ymin < precision) and (zmax - zmin < precision):
            # i just solved the case 1, 2, 4, 5, 8 because they are the more common cases and the most used
            # for a sphere
            case_1 = [[(xmin, ymin, zmid), (xmid, ymin, zmin), (xmin, ymid, zmin)]]
            case_1_base = np.array([True, False, False, False, False, False, False, False])
            case_2 = [[(xmin, ymin, zmid), (xmax, ymin, zmid), (xmin, ymid, zmin)],
                      [(xmax, ymid, zmin), (xmax, ymin, zmid), (xmin, ymid, zmin)]]
            case_2_base = np.array([True, True, False, False, False, False, False, False])
            # case_3 = [case_1,
            #           rotate_point(case_1, (xmid, ymid, zmid), (0, 0, 180))]
            case_4 = [[(xmid, ymin, zmin), (xmin, ymin, zmid), (xmax, ymid, zmin)],
                      [(xmin, ymin, zmid), (xmin, ymid, zmax), (xmax, ymid, zmin)],
                      [(xmin, ymid, zmax), (xmax, ymid, zmin), (xmax, ymid, zmax)]]
            case_4_base = np.array([False, True, False, False, True, True, False, False])
            case_5 = [[(xmin, ymid, zmin), (xmax, ymid, zmax), (xmax, ymid, zmin)],
                      [(xmin, ymid, zmin), (xmax, ymid, zmax), (xmin, ymid, zmax)]]
            case_5_base = np.array([True, True, False, False, True, True, False, False])
            case_8 = [[(xmin, ymid, zmin), (xmin, ymax, zmid), (xmid, ymax, zmax)],
                      [(xmin, ymid, zmin), (xmid, ymin, zmin), (xmid, ymax, zmax)],
                        [(xmid, ymin, zmin), (xmid, ymax, zmax), (xmax, ymid, zmax)],
                        [(xmax, ymid, zmax), (xmid, ymin, zmin), (xmax, ymin, zmid)]]
            case_8_base = np.array([True, False, False, False, True, True, True, False])
            
            local_faces = []            
            # case 1 and its rotations
            found = False
            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        x = i * 90
                        y = j * 90
                        z = k * 90
                        rotated_cube = rotate_z_curve(cube, x, y, z)
                        # check if the rotated cube matches the case
                        if (rotated_cube == case_1_base).all() or (rotated_cube == ~case_1_base).all():
                            local_faces = setup_case(case_1, (xmid, ymid, zmid), (x, y, z))
                            found = True
                            break
                        if (rotated_cube == case_2_base).all() or (rotated_cube == ~case_2_base).all():
                            local_faces = setup_case(case_2, (xmid, ymid, zmid), (x, y, z))
                            found = True
                            break
                        if (rotated_cube == case_4_base).all() or (rotated_cube == ~case_4_base).all():
                            local_faces = setup_case(case_4, (xmid, ymid, zmid), (x, y, z))
                            found = True
                            break
                        if (rotated_cube == case_5_base).all() or (rotated_cube == ~case_5_base).all():
                            local_faces = setup_case(case_5, (xmid, ymid, zmid), (x, y, z))
                            found = True
                            break
                        if (rotated_cube == case_8_base).all() or (rotated_cube == ~case_8_base).all():
                            local_faces = setup_case(case_8, (xmid, ymid, zmid), (x, y, z))
                            found = True
                            break
                    if found:
                        break
                if found:
                    break
            
            if local_faces != []:
                for face in local_faces[0]:
                    faces.append(face)
                colors.append(local_faces[1])
            
            
            return
           
        
        marching_cubes_u(f, xmin, ymin, zmin, xmid, ymid, zmid, precision, faces, colors)
        marching_cubes_u(f, xmid, ymin, zmin, xmax, ymid, zmid, precision, faces, colors)
        marching_cubes_u(f, xmin, ymid, zmin, xmid, ymax, zmid, precision, faces, colors)
        marching_cubes_u(f, xmid, ymid, zmin, xmax, ymax, zmid, precision, faces, colors)
        marching_cubes_u(f, xmin, ymin, zmid, xmid, ymid, zmax, precision, faces, colors)
        marching_cubes_u(f, xmid, ymin, zmid, xmax, ymid, zmax, precision, faces, colors)
        marching_cubes_u(f, xmin, ymid, zmid, xmid, ymax, zmax, precision, faces, colors)
        marching_cubes_u(f, xmid, ymid, zmid, xmax, ymax, zmax, precision, faces, colors)


def marching_cubes(f, output_filename, xmin, ymin, zmin, xmax, ymax, zmax, precision):
    
    faces = []
    colors = []
    marching_cubes_u(f, xmin, ymin, zmin, xmax, ymax, zmax, precision, faces, colors)

    to_OFF(faces, output_filename)

    
def f_3d(x, y, z):
    return float(x)**2 + float(y)**2 + float(z)**2 - 1000
# 3d heart

def f_2d(x, y):
    return float(x)**2 + float(y)**2 - 1000

if __name__ == '__main__':

    marching_squares(f_2d, "output.eps", -100, -100, 100, 100, 0.5)
    marching_cubes(f_3d, "output.OFF", -100, -100, -100, 100, 100, 100, 4)

# Drawing the implicit curve for f(x, y) = 0
# marching_squares(f, "output.eps", -100, -100, 100, 100, 0.5)



