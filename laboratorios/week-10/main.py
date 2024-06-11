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
    
    #rotate every point in points_3d around pivot_3d by angle_3d convert to radian
    angle_3d = angle_3d * np.pi / 180
    #use the rotation matrix
    points_3d = points_3d - pivot_3d
    x = points_3d[:,0]
    y = points_3d[:,1]
    z = points_3d[:,2]
    angle_x = angle_3d[0]
    angle_y = angle_3d[1]
    angle_z = angle_3d[2]
    #rotate around x
    x_rotated = x
    y_rotated = y*np.cos(angle_x) - z*np.sin(angle_x)
    z_rotated = y*np.sin(angle_x) + z*np.cos(angle_x)
    #rotate around y
    x = x_rotated
    y = y_rotated
    z = z_rotated
    x_rotated = x*np.cos(angle_y) + z*np.sin(angle_y)
    y_rotated = y
    z_rotated = -x*np.sin(angle_y) + z*np.cos(angle_y)
    #rotate around z
    x = x_rotated
    y = y_rotated
    z = z_rotated
    x_rotated = x*np.cos(angle_z) - y*np.sin(angle_z)
    y_rotated = x*np.sin(angle_z) + y*np.cos(angle_z)
    z_rotated = z
    #add the pivot back
    points_3d = np.array([x_rotated, y_rotated, z_rotated]).T + pivot_3d
    return points_3d.tolist()

def mirror_point(points_3d, pivot_3d, axis):
    points_3d = np.array(points_3d)
    pivot_3d = np.array(pivot_3d)
    axis = np.array(axis)
    #mirror every point in points_3d around pivot_3d by axis
    points_3d = points_3d - pivot_3d
    x = points_3d[:,0]
    y = points_3d[:,1]
    z = points_3d[:,2]
    a = axis[0]
    b = axis[1]
    c = axis[2]
    #mirror around the plane a*x + b*y + c*z = 0
    x_mirrored = x - 2*(a*x + b*y + c*z)/(a**2 + b**2 + c**2)*a
    y_mirrored = y - 2*(a*x + b*y + c*z)/(a**2 + b**2 + c**2)*b
    z_mirrored = z - 2*(a*x + b*y + c*z)/(a**2 + b**2 + c**2)*c
    #add the pivot back
    points_3d = np.array([x_mirrored, y_mirrored, z_mirrored]).T + pivot_3d
    return points_3d.tolist()
    
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
            
            

def marching_cubes(f, output_filename, xmin, ymin, zmin, xmax, ymax, zmax, precision):
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
        
        
        
        cube = np.array((f000 > 0, f100 > 0, f010 > 0, f110 > 0, f001 > 0, f101 > 0, f011 > 0, f111 > 0))
        cube_str = ''.join([str(int(i)) for i in cube])
        cube_str = cube_str[:4] + '_' + cube_str[4:]
        cube_n_str = ''.join([str(int(not i)) for i in cube])
        cube_n_str = cube_n_str[:4] + '_' + cube_n_str[4:]
        #check if is less than precision
        
        if np.all(cube):
            if not check_if_function_changes_sign_in_box(f, xmin, ymin, zmin, xmax, ymax, zmax):
                return
        
        if ((xmax - xmin )< precision) and (ymax - ymin < precision) and (zmax - zmin < precision):
            case_1 = [[(xmin, ymin, zmid), (xmid, ymin, zmin), (xmin, ymid, zmin)]]
            case_2 = [[(xmin, ymin, zmid), (xmax, ymin, zmid), (xmin, ymid, zmin)],
                      [(xmax, ymid, zmin), (xmax, ymin, zmid), (xmin, ymid, zmin)]]
            case_3 = [case_1,
                      rotate_point(case_1, (xmid, ymid, zmid), (0, 0, 180))]
            case_4 = [[(xmid, ymin, zmin), (xmin, ymin, zmid), (xmax, ymid, zmin)],
                      [(xmin, ymin, zmid), (xmin, ymid, zmax), (xmax, ymid, zmin)],
                      [(xmin, ymid, zmax), (xmax, ymid, zmin), (xmax, ymid, zmax)]]
            case_5 = [[(xmin, ymid, zmin), (xmax, ymid, zmax), (xmax, ymid, zmin)],
                      [(xmin, ymid, zmin), (xmax, ymid, zmax), (xmin, ymid, zmax)]]
            local_faces = []            
            if '0000_0000' in [cube_str, cube_n_str]:
                pass
            elif '0000_0001' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_1, (xmid, ymid, zmid), (180, 90, 0))
            elif '0000_0010' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_1, (xmid, ymid, zmid), (180, 0, 0))
            elif '0000_0011' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_2, (xmid, ymid, zmid), (-90, 0, 180))
            elif '0000_0100' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_1, (xmid, ymid, zmid), (0, 180, 0))
            elif '0000_0101' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_2, (xmid, ymid, zmid), (-90, 0, 90))
            elif '0000_0110' in [cube_str, cube_n_str]:
                pass # case 3
            elif '0000_0111' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_4, (xmid, ymid, zmid), (-90, 0, 0))
            elif '0000_1000' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_1, (xmid, ymid, zmid), (-90, 0, 0))
            elif '0000_1001' in [cube_str, cube_n_str]:
                pass # case 3
            elif '0000_1010' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_2, (xmid, ymid, zmid), (-90, 0, -90))
            elif '0000_1011' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_4, (xmid, ymid, zmid), (-90, 0, 90))
            elif '0000_1100' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_2, (xmid, ymid, zmid), (0, 180, 0))
            elif '0000_1101' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_4, (xmid, ymid, zmid), (-90, 0, -90)) #bug?
            elif '0000_1110' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_4, (xmid, ymid, zmid), (-90, 0, 90)) #bug?
            elif '0000_1111' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_5, (xmid, ymid, zmid), (-90, 0, 0))
            elif '0001_0000' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_1, (xmid, ymid, zmid), (0, 0, 180))
            #ignore weird cases
            
            elif '0100_1100' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_4, (xmid, ymid, zmid), (0, 0, 0))
            elif '1100_1100' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_5, (xmid, ymid, zmid), (0, 0, 0))
            elif '0101_0101' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_5, (xmid, ymid, zmid), (0, 0, 90))
            
            #################
            elif '0010_0000' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_1, (xmid, ymid, zmid), (90, 0, 0))
            elif '0011_0000' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_2, (xmid, ymid, zmid), (0, 0, 180))
                
            elif '0100_0000' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_1, (xmid, ymid, zmid), (0, 0, 90))
            elif '0101_0000' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_2, (xmid, ymid, zmid), (0, 0, 90))
            elif '0110_0000' in [cube_str, cube_n_str]:
                pass #case 3
            elif '0111_0000' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_4, (xmid, ymid, zmid), (90, 0, -90))
            elif '1000_0000' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_1, (xmid, ymid, zmid), (0, 0, 0))
            elif '1001_0000' in [cube_str, cube_n_str]:
                pass #case 3
            elif '1010_0000' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_2, (xmid, ymid, zmid), (0, 0, -90))
            elif '1011_0000' in [cube_str, cube_n_str]:
                local_faces =  setup_case(case_4, (xmid, ymid, zmid), (90, 0, 180))
            elif '1100_0000' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_2, (xmid, ymid, zmid), (0, 0, 0))
            elif '1101_0000' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_4, (xmid, ymid, zmid), (90, 0, 0))
            elif '1110_0000' in [cube_str, cube_n_str]:
                local_faces = setup_case(case_4, (xmid, ymid, zmid), (-90, 180, 0))
                
            
                
            
            
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
        
    faces = []
    colors = []
    marching_cubes_u(f, xmin, ymin, zmin, xmax, ymax, zmax, precision, faces, colors)
    
    #show as 3d in matplotlib and rotate
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # for face in faces:
    #     n = len(face)
    #     for i in range(n):
    #         ax.plot([face[i][0], face[(i+1)%n][0]], [face[i][1], face[(i+1)%n][1]], [face[i][2], face[(i+1)%n][2]], f'{colors[i]}-', linewidth=0.3)
    #         #fill polygon
    # plt.axis('off')
    # ax.set_aspect('equal')
    
    #show axis labels
    # ax.set_xlabel('X')
    # ax.set_ylabel('Y')
    # ax.set_zlabel('Z')
    
    to_OFF(faces, output_filename)
    
    
    #rotate the plot
    # for angle in range(0, 360):
    #     ax.view_init(30, angle)
    #     plt.draw()
    #     plt.pause(.001)
    
    
def f_3d(x, y, z):
    return float(x)**2 + float(y)**2 + float(z)**2 - 1000

def f_2d(x, y):
    return float(x)**2 + float(y)**2 - 1000

if __name__ == '__main__':

    marching_squares(f_2d, "output.eps", -100, -100, 100, 100, 0.5)
    marching_cubes(f_3d, "output.OFF", -100, -100, -100, 100, 100, 100, 5)    

# Drawing the implicit curve for f(x, y) = 0
# marching_squares(f, "output.eps", -100, -100, 100, 100, 0.5)



