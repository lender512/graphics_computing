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
            pass  # No lines needed
        if square in [(False, False, False, False)]:    
            pass  # No lines needed
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

# Drawing the implicit curve for f(x, y) = 0
marching_squares(f, "output.eps", -100, -100, 100, 100, 0.5)



