import numpy as np


def draw_curve(f, output_filename, xmin, ymin, xmax, ymax, precision):
    def marching_squares(f, xmin, ymin, xmax, ymax, precision, lines):

        if (xmax - xmin < precision) and (ymax - ymin < precision):
            return

        xmid = (xmin + xmax) / 2
        ymid = (ymin + ymax) / 2

        f00 = f(xmin, ymin)
        f10 = f(xmax, ymin)
        f01 = f(xmin, ymax)
        f11 = f(xmax, ymax)


        # check if it is bewteen a threshold
        square = (f00 > -precision and f00 < precision, f10 > -precision and f10 < precision,
                  f01 > -precision and f01 < precision, f11 > -precision and f11 < precision)

        if square in [(False, False, False, True), (True, True, True, False)]:
            lines.append(((xmid, ymax), (xmax, ymid)))
        if square in [(True, False, False, False), (False, True, True, True)]:
            lines.append(((xmin, ymid), (xmid, ymin)))
        if square in [(False, True, False, False), (True, False, True, True)]:
            lines.append(((xmid, ymin), (xmax, ymid)))
        if square in [(False, False, True, False), (True, True, False, True)]:
            lines.append(((xmin, ymid), (xmid, ymax)))
        if square in [(True, False, True, False), (False, True, False, True)]:
            lines.append(((xmid, ymin), (xmid, ymax)))
        if square in [(True, True, False, False), (False, False, True, True)]:
            lines.append(((xmin, ymid), (xmax, ymid)))
        if square in [(True, False, False, True)]:
            lines.append(((xmin, ymid), (xmid, ymin)))
            lines.append(((xmid, ymax), (xmax, ymid)))
        if square in [(False, True, True, False)]:
            lines.append(((xmin, ymid), (xmid, ymax)))
            lines.append(((xmid, ymin), (xmax, ymid)))

        if square in [(True, True, True, True)]:
            pass  # No lines needed
        if square in [(False, False, False, False)]:
            pass  # No lines needed

        # Recursively divide into four sub-squares
        marching_squares(f, xmin, ymin, xmid, ymid, precision, lines)
        marching_squares(f, xmid, ymin, xmax, ymid, precision, lines)
        marching_squares(f, xmin, ymid, xmid, ymax, precision, lines)
        marching_squares(f, xmid, ymid, xmax, ymax, precision, lines)

    lines = []
    marching_squares(f, xmin, ymin, xmax, ymax, precision, lines)

    with open(output_filename, 'w') as file:
        file.write("%!PS-Adobe-3.0 EPSF-3.0\n")
        file.write("%%BoundingBox: {} {} {} {}\n".format(
            xmin, ymin, xmax, ymax))
        file.write("newpath\n")

        for line in lines:
            (x0, y0), (x1, y1) = line
            file.write("{} {} moveto\n".format(x0, y0))
            file.write("{} {} lineto\n".format(x1, y1))

        file.write("stroke\n")
        file.write("showpage\n")

# Example implicit function: circle of radius 1 centered at (0,0)


def f(x, y):
    return x*x + y*y - 1000


# Drawing the implicit curve for f(x, y) = 0
draw_curve(f, "output.eps", -100, -100, 100, 100, 0.01)
