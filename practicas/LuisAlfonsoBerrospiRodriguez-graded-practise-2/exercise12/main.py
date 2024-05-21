#Sutherland-Hodgman algorithm

def inside(p, cp1, cp2):
    # Return True if point p is inside the clip polygon
    return (cp2[0] - cp1[0]) * (p[1] - cp1[1]) > (cp2[1] - cp1[1]) * (p[0] - cp1[0])

def compute_intersection(cp1, cp2, s, e):
    dc = [cp1[0] - cp2[0], cp1[1] - cp2[1]]
    dp = [s[0] - e[0], s[1] - e[1]]
    n1 = cp1[0] * cp2[1] - cp1[1] * cp2[0]
    n2 = s[0] * e[1] - s[1] * e[0]
    n3 = 1.0 / (dc[0] * dp[1] - dc[1] * dp[0])
    # Return the intersection point
    return [(n1 * dp[0] - n2 * dc[0]) * n3, (n1 * dp[1] - n2 * dc[1]) * n3]

def clip_polygon_to_subject(subject_polygon, clip_polygon):
    output_list = subject_polygon
    cp1 = clip_polygon[-1]

    for clip_vertex in clip_polygon:
        cp2 = clip_vertex
        input_list = output_list
        output_list = []
        s = input_list[-1]

        for subject_vertex in input_list:
            e = subject_vertex
            if inside(e, cp1, cp2):
                # If the previous vertex was outside, add an intersection
                if not inside(s, cp1, cp2):
                    # Add the intersection point
                    output_list.append(compute_intersection(cp1, cp2, s, e))
                # Add the subject vertex
                output_list.append(e)
            elif inside(s, cp1, cp2):
                # Add an intersection point
                output_list.append(compute_intersection(cp1, cp2, s, e))
            s = e
        cp1 = cp2
    return output_list

#from exercise11
def areaOfConvexPolygon(points):
    determinant = 0
    for i in range(len(points)):
        determinant += points[i][0]*points[(i+1)%len(points)][1] - points[i][1]*points[(i+1)%len(points)][0]
    return 0.5*abs(determinant)

subjectp = [(50.0, 150.0), (200.0, 50.0), (350.0, 150.0)]
clipp = [(100.0, 100.0), (300.0, 100.0), (300.0, 300.0), (100.0, 300.0)]

result = clip_polygon_to_subject(subjectp, clipp)
area = areaOfConvexPolygon(result)

import matplotlib.pyplot as plt
for i in range(len(subjectp)):
    plt.plot([subjectp[i][0], subjectp[(i+1)%len(subjectp)][0]], [subjectp[i][1], subjectp[(i+1)%len(subjectp)][1]], 'r-')
for i in range(len(clipp)):
    plt.plot([clipp[i][0], clipp[(i+1)%len(clipp)][0]], [clipp[i][1], clipp[(i+1)%len(clipp)][1]], 'b-')
for i in range(len(result)):
    plt.plot([result[i][0], result[(i+1)%len(result)][0]], [result[i][1], result[(i+1)%len(result)][1]], 'g-')
plt.title(f'Area: {area:.2f}')
plt.show()