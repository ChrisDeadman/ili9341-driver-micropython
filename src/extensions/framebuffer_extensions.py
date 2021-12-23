# Extension functions for framebuffers.
#
# Copied from:
# - https://github.com/rdagger/micropython-ili9341/blob/master/ili9341.py
#
# MIT License; Copyright (c) 2022 rdagger
#

from math import cos, pi, radians, sin


def lines(fb, coords, color):
    """Draw multiple lines.
    Args:
        coords ([[int, int],...]): Line coordinate X, Y pairs
        color (int): RGB565 color value.
    """
    # Starting point
    x1, y1 = coords[0]
    # Iterate through coordinates
    for i in range(1, len(coords)):
        x2, y2 = coords[i]
        fb.line(x1, y1, x2, y2, color)
        x1, y1 = x2, y2


def circle(fb, x0, y0, r, color):
    """Draw a circle.
    Args:
        x0 (int): X coordinate of center point.
        y0 (int): Y coordinate of center point.
        r (int): Radius.
        color (int): RGB565 color value.
    """
    f = 1 - r
    dx = 1
    dy = -r - r
    x = 0
    y = r
    fb.pixel(x0, y0 + r, color)
    fb.pixel(x0, y0 - r, color)
    fb.pixel(x0 + r, y0, color)
    fb.pixel(x0 - r, y0, color)
    while x < y:
        if f >= 0:
            y -= 1
            dy += 2
            f += dy
        x += 1
        dx += 2
        f += dx
        fb.pixel(x0 + x, y0 + y, color)
        fb.pixel(x0 - x, y0 + y, color)
        fb.pixel(x0 + x, y0 - y, color)
        fb.pixel(x0 - x, y0 - y, color)
        fb.pixel(x0 + y, y0 + x, color)
        fb.pixel(x0 - y, y0 + x, color)
        fb.pixel(x0 + y, y0 - x, color)
        fb.pixel(x0 - y, y0 - x, color)


def ellipse(fb, x0, y0, a, b, color):
    """Draw an ellipse.
    Args:
        x0, y0 (int): Coordinates of center point.
        a (int): Semi axis horizontal.
        b (int): Semi axis vertical.
        color (int): RGB565 color value.
    Note:
        The center point is the center of the x0,y0 pixel.
        Since pixels are not divisible, the axes are integer rounded
        up to complete on a full pixel.  Therefore the major and
        minor axes are increased by 1.
    """
    a2 = a * a
    b2 = b * b
    twoa2 = a2 + a2
    twob2 = b2 + b2
    x = 0
    y = b
    px = 0
    py = twoa2 * y
    # Plot initial points
    fb.pixel(x0 + x, y0 + y, color)
    fb.pixel(x0 - x, y0 + y, color)
    fb.pixel(x0 + x, y0 - y, color)
    fb.pixel(x0 - x, y0 - y, color)
    # Region 1
    p = round(b2 - (a2 * b) + (0.25 * a2))
    while px < py:
        x += 1
        px += twob2
        if p < 0:
            p += b2 + px
        else:
            y -= 1
            py -= twoa2
            p += b2 + px - py
        fb.pixel(x0 + x, y0 + y, color)
        fb.pixel(x0 - x, y0 + y, color)
        fb.pixel(x0 + x, y0 - y, color)
        fb.pixel(x0 - x, y0 - y, color)
    # Region 2
    p = round(b2 * (x + 0.5) * (x + 0.5) +
              a2 * (y - 1) * (y - 1) - a2 * b2)
    while y > 0:
        y -= 1
        py -= twoa2
        if p > 0:
            p += a2 - py
        else:
            x += 1
            px += twob2
            p += a2 - py + px
        fb.pixel(x0 + x, y0 + y, color)
        fb.pixel(x0 - x, y0 + y, color)
        fb.pixel(x0 + x, y0 - y, color)
        fb.pixel(x0 - x, y0 - y, color)


def polygon(fb, sides, x0, y0, r, color, rotate=0):
    """Draw an n-sided regular polygon.
    Args:
        sides (int): Number of polygon sides.
        x0, y0 (int): Coordinates of center point.
        r (int): Radius.
        color (int): RGB565 color value.
        rotate (Optional float): Rotation in degrees relative to origin.
    Note:
        The center point is the center of the x0,y0 pixel.
        Since pixels are not divisible, the radius is integer rounded
        up to complete on a full pixel.  Therefore diameter = 2 x r + 1.
    """
    coords = []
    theta = radians(rotate)
    n = sides + 1
    for s in range(n):
        t = 2.0 * pi * s / sides + theta
        coords.append([int(r * cos(t) + x0), int(r * sin(t) + y0)])

    # Cast to python float first to fix rounding errors
    lines(fb, coords, color=color)


def fill_circle(fb, x0, y0, r, color):
    """Draw a filled circle.
    Args:
        x0 (int): X coordinate of center point.
        y0 (int): Y coordinate of center point.
        r (int): Radius.
        color (int): RGB565 color value.
    """
    f = 1 - r
    dx = 1
    dy = -r - r
    x = 0
    y = r
    fb.vline(x0, y0 - r, 2 * r + 1, color)
    while x < y:
        if f >= 0:
            y -= 1
            dy += 2
            f += dy
        x += 1
        dx += 2
        f += dx
        fb.vline(x0 + x, y0 - y, 2 * y + 1, color)
        fb.vline(x0 - x, y0 - y, 2 * y + 1, color)
        fb.vline(x0 - y, y0 - x, 2 * x + 1, color)
        fb.vline(x0 + y, y0 - x, 2 * x + 1, color)


def fill_ellipse(fb, x0, y0, a, b, color):
    """Draw a filled ellipse.
    Args:
        x0, y0 (int): Coordinates of center point.
        a (int): Semi axis horizontal.
        b (int): Semi axis vertical.
        color (int): RGB565 color value.
    Note:
        The center point is the center of the x0,y0 pixel.
        Since pixels are not divisible, the axes are integer rounded
        up to complete on a full pixel.  Therefore the major and
        minor axes are increased by 1.
    """
    a2 = a * a
    b2 = b * b
    twoa2 = a2 + a2
    twob2 = b2 + b2
    x = 0
    y = b
    px = 0
    py = twoa2 * y
    # Plot initial points
    fb.line(x0, y0 - y, x0, y0 + y, color)
    # Region 1
    p = round(b2 - (a2 * b) + (0.25 * a2))
    while px < py:
        x += 1
        px += twob2
        if p < 0:
            p += b2 + px
        else:
            y -= 1
            py -= twoa2
            p += b2 + px - py
        fb.line(x0 + x, y0 - y, x0 + x, y0 + y, color)
        fb.line(x0 - x, y0 - y, x0 - x, y0 + y, color)
    # Region 2
    p = round(b2 * (x + 0.5) * (x + 0.5) +
              a2 * (y - 1) * (y - 1) - a2 * b2)
    while y > 0:
        y -= 1
        py -= twoa2
        if p > 0:
            p += a2 - py
        else:
            x += 1
            px += twob2
            p += a2 - py + px
        fb.line(x0 + x, y0 - y, x0 + x, y0 + y, color)
        fb.line(x0 - x, y0 - y, x0 - x, y0 + y, color)


def fill_polygon(fb, sides, x0, y0, r, color, rotate=0):
    """Draw a filled n-sided regular polygon.
    Args:
        sides (int): Number of polygon sides.
        x0, y0 (int): Coordinates of center point.
        r (int): Radius.
        color (int): RGB565 color value.
        rotate (Optional float): Rotation in degrees relative to origin.
    Note:
        The center point is the center of the x0,y0 pixel.
        Since pixels are not divisible, the radius is integer rounded
        up to complete on a full pixel.  Therefore diameter = 2 x r + 1.
    """
    # Determine side coordinates
    coords = []
    theta = radians(rotate)
    n = sides + 1
    for s in range(n):
        t = 2.0 * pi * s / sides + theta
        coords.append([int(r * cos(t) + x0), int(r * sin(t) + y0)])
    # Starting point
    x1, y1 = coords[0]
    # Minimum Maximum X dict
    xdict = {y1: [x1, x1]}
    # Iterate through coordinates
    for row in coords[1:]:
        x2, y2 = row
        xprev, yprev = x2, y2
        # Calculate perimeter
        # Check for horizontal side
        if y1 == y2:
            if x1 > x2:
                x1, x2 = x2, x1
            if y1 in xdict:
                xdict[y1] = [min(x1, xdict[y1][0]), max(x2, xdict[y1][1])]
            else:
                xdict[y1] = [x1, x2]
            x1, y1 = xprev, yprev
            continue
        # Non horizontal side
        # Changes in x, y
        dx = x2 - x1
        dy = y2 - y1
        # Determine how steep the line is
        is_steep = abs(dy) > abs(dx)
        # Rotate line
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        # Swap start and end points if necessary
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        # Recalculate differentials
        dx = x2 - x1
        dy = y2 - y1
        # Calculate error
        error = dx >> 1
        ystep = 1 if y1 < y2 else -1
        y = y1
        # Calcualte minimum and maximum x values
        for x in range(x1, x2 + 1):
            if is_steep:
                if x in xdict:
                    xdict[x] = [min(y, xdict[x][0]), max(y, xdict[x][1])]
                else:
                    xdict[x] = [y, y]
            else:
                if y in xdict:
                    xdict[y] = [min(x, xdict[y][0]), max(x, xdict[y][1])]
                else:
                    xdict[y] = [x, x]
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx
        x1, y1 = xprev, yprev
    # Fill polygon
    for y, x in xdict.items():
        fb.hline(x[0], y, x[1] - x[0] + 2, color)
