# Framebuffer with extension functions.
#
# Circle/ellipse/polygon functions are from:
# https://github.com/rdagger/micropython-ili9341/blob/master/ili9341.py
# (MIT License; Copyright (c) 2022 rdagger)
#
# Rest is MIT License; Copyright (c) 2022 Christopher Hubmann
#

from math import cos, pi, radians, sin

import fonts
import framebuf


class FrameBufferEx(object):

    def __init__(self, buffer, width, height, format=framebuf.RGB565, stride=None, fbuf=None):
        self.buffer = buffer
        self.width = width
        self.height = height
        self.format = format
        if stride == None:
            self.stride = width
        else:
            self.stride = stride

        if fbuf:
            self.fbuf = fbuf
        else:
            self.fbuf = framebuf.FrameBuffer(self.buffer, self.width, self.height, self.format, self.stride)

    def fill(self, c):
        """Fill display with the specified color."""
        self.fbuf.fill(c)

    def pixel(self, x, y, c=None):
        """Draw a single pixel with the specified color or return pixel color if c is not provided."""
        self.fbuf.pixel(x, y, c)

    def hline(self, x, y, w, c):
        """Draw a horizontal line."""
        self.fbuf.hline(x, y, w, c)

    def vline(self, x, y, h, c):
        """Draw a vertical line."""
        self.fbuf.vline(x, y, h, c)

    def line(self, x1, y1, x2, y2, c):
        """Draw a line."""
        self.fbuf.line(x1, y1, x2, y2, c)

    def rect(self, x, y, w, h, c):
        """Draw a rectangle."""
        self.fbuf.rect(x, y, w, h, c)

    def fill_rect(self, x, y, w, h, c):
        """Draw a filled rectangle."""
        self.fbuf.fill_rect(x, y, w, h, c)

    def scroll(self, xstep=None, ystep=None):
        """Set the shift of the contents of the framebuffer to the given vector."""
        return self.fbuf.scroll(xstep, ystep)

    def blit(self, fbuf, x, y, key=-1, palette=framebuf.RGB565):
        """Draw the contents of a framebuffer at the given coordinates."""
        if isinstance(self.fbuf, framebuf.FrameBuffer):
            fbuf = fbuf.fbuf
        self.fbuf.blit(fbuf, x, y, key, palette)

    def lines(self, coords, color):
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
            self.line(x1, y1, x2, y2, color)
            x1, y1 = x2, y2

    def circle(self, x0, y0, r, color):
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
        self.pixel(x0, y0 + r, color)
        self.pixel(x0, y0 - r, color)
        self.pixel(x0 + r, y0, color)
        self.pixel(x0 - r, y0, color)
        while x < y:
            if f >= 0:
                y -= 1
                dy += 2
                f += dy
            x += 1
            dx += 2
            f += dx
            self.pixel(x0 + x, y0 + y, color)
            self.pixel(x0 - x, y0 + y, color)
            self.pixel(x0 + x, y0 - y, color)
            self.pixel(x0 - x, y0 - y, color)
            self.pixel(x0 + y, y0 + x, color)
            self.pixel(x0 - y, y0 + x, color)
            self.pixel(x0 + y, y0 - x, color)
            self.pixel(x0 - y, y0 - x, color)

    def ellipse(self, x0, y0, a, b, color):
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
        self.pixel(x0 + x, y0 + y, color)
        self.pixel(x0 - x, y0 + y, color)
        self.pixel(x0 + x, y0 - y, color)
        self.pixel(x0 - x, y0 - y, color)
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
            self.pixel(x0 + x, y0 + y, color)
            self.pixel(x0 - x, y0 + y, color)
            self.pixel(x0 + x, y0 - y, color)
            self.pixel(x0 - x, y0 - y, color)
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
            self.pixel(x0 + x, y0 + y, color)
            self.pixel(x0 - x, y0 + y, color)
            self.pixel(x0 + x, y0 - y, color)
            self.pixel(x0 - x, y0 - y, color)

    def polygon(self, sides, x0, y0, r, color, rotate=0):
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
        self.lines(coords, color=color)

    def fill_circle(self, x0, y0, r, color):
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
        self.vline(x0, y0 - r, 2 * r + 1, color)
        while x < y:
            if f >= 0:
                y -= 1
                dy += 2
                f += dy
            x += 1
            dx += 2
            f += dx
            self.vline(x0 + x, y0 - y, 2 * y + 1, color)
            self.vline(x0 - x, y0 - y, 2 * y + 1, color)
            self.vline(x0 - y, y0 - x, 2 * x + 1, color)
            self.vline(x0 + y, y0 - x, 2 * x + 1, color)

    def fill_ellipse(self, x0, y0, a, b, color):
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
        self.line(x0, y0 - y, x0, y0 + y, color)
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
            self.line(x0 + x, y0 - y, x0 + x, y0 + y, color)
            self.line(x0 - x, y0 - y, x0 - x, y0 + y, color)
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
            self.line(x0 + x, y0 - y, x0 + x, y0 + y, color)
            self.line(x0 - x, y0 - y, x0 - x, y0 + y, color)

    def fill_polygon(self, sides, x0, y0, r, color, rotate=0):
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
            self.hline(x[0], y, x[1] - x[0] + 2, color)

    def text(self, s, x, y, c=1, bg=-1, font=fonts.tt14):
        """Draw some text."""
        bg = bg if bg >= 0 else 1 if c == 0 else 0
        key = -1 if bg >= 0 else bg
        width = min(font.get_width(s), self.width)  # don't draw past width
        height = font.height()

        c_bytes = c.to_bytes(2, 'big')
        bg_bytes = bg.to_bytes(2, 'big')

        fbdata = bytearray(bg_bytes * height * width)
        fbuf = FrameBufferEx(fbdata, width, height, framebuf.RGB565)

        div, remainder = divmod(height, 8)
        num_glyph_rows = div+1 if remainder else div
        text_x = 0
        for ch in s:
            glyph, char_width = font.get_ch(ch)
            for char_y in range(height):
                glyph_row_idx, glyph_row_y = divmod(char_y, 8)
                fb_offset = char_y*width*2
                for char_x in range(char_width):
                    if text_x+char_x < width:  # don't draw past width
                        glyph_idx = (char_x*num_glyph_rows)+glyph_row_idx
                        glyph_row = glyph[glyph_idx]
                        if (glyph_row >> glyph_row_y) & 1:
                            pixel_idx = fb_offset+(text_x+char_x)*2
                            fbdata[pixel_idx] = c_bytes[0]
                            fbdata[pixel_idx+1] = c_bytes[1]
            text_x += char_width
            if text_x >= width:  # don't draw past width
                break

        self.blit(fbuf, x, y, key, framebuf.RGB565)
        return width
