from time import sleep

import framebuf
from extensions import fb, input
from utils import COMMON_COLORS


class DrawTest(object):

    def __init__(self, display):
        self.display = display

    def execute(self, bg_color):
        while True:
            print('Draw tests:')
            tests = [
                ['rectangles', lambda: self.test_rectangles(bg_color)],
                ['cirles', lambda: self.test_circles(bg_color)],
                ['polygons', lambda: self.test_polygons(bg_color)],
                ['blit', lambda: self.test_blit(bg_color)],
                ['blit_row', lambda: self.test_blit_row(bg_color)],
                ['scroll', lambda: self.test_scroll(bg_color)],
                ['Return', None]
            ]
            for idx, test in enumerate(tests):
                print(f'{idx}: {test[0]}')

            test_idx = input.read_int('test>')
            if test_idx >= len(tests) - 1:
                break

            tests[test_idx][1]()

    def test_rectangles(self, bg_color):
        self.display.fill(bg_color)

        x = 0
        y = 0
        width = self.display.width
        height = self.display.height // len(COMMON_COLORS) - 1
        for color in COMMON_COLORS:
            if y < self.display.height // 2:
                self.display.rect(x, y, width, height, color)
            else:
                self.display.fill_rect(x, y, width, height, color)
            y += height + 1

    def test_circles(self, bg_color):
        self.display.fill(bg_color)

        r = 1
        x = r
        y = int(self.display.height * 1 // 5)
        for color in COMMON_COLORS:
            if x+r*2 >= self.display.width:
                break
            fb.circle(self.display, x, y, r, color)
            r += 3
            x += r*2

        r = 1
        x = r
        y = int(self.display.height * 2 // 5)
        for color in COMMON_COLORS:
            if x+r*2 >= self.display.width:
                break
            fb.fill_circle(self.display, x, y, r, color)
            r += 3
            x += r*2

        r = 1
        x = 6
        y = int(self.display.height * 3 // 5)
        for color in reversed(COMMON_COLORS):
            if x+r*2 >= self.display.width:
                break
            fb.ellipse(self.display, x, y, r+4, r, color)
            r += 3
            x += r*2

        r = 1
        x = r
        y = int(self.display.height * 4 // 5)
        for color in reversed(COMMON_COLORS):
            if x+r*2 >= self.display.width:
                break
            fb.fill_ellipse(self.display, x, y, r, r+4, color)
            r += 3
            x += r*2

    def test_polygons(self, bg_color):
        self.display.fill(bg_color)

        r = 4
        x = r
        y = int(self.display.height * 1 // 3)
        sides = 3
        for color in COMMON_COLORS:
            if x+r*2 >= self.display.width:
                break
            fb.polygon(self.display, sides, x, y, r, color)
            r += 3
            x += r*2 + 1
            sides += 1

        r = 4
        x = r
        y = int(self.display.height * 2 // 3)
        sides = 3
        for color in reversed(COMMON_COLORS):
            if x+r*2 >= self.display.width:
                break
            fb.fill_polygon(self.display, sides, x, y, r, color)
            r += 3
            x += r*2 + 1
            sides += 1

    def test_blit(self, bg_color):
        self.display.fill(bg_color)

        x = 0
        y = 0
        width = self.display.width
        height = self.display.height // len(COMMON_COLORS)

        fb_data = bytearray(width * height * 2)
        fb = framebuf.FrameBuffer(fb_data, width, height, framebuf.RGB565)

        for color in COMMON_COLORS:
            fb.fill(color)
            self.display.blit(fb_data, x, y, width, height)
            y += height

        sleep(1)

        y = self.display.height - height
        for color in COMMON_COLORS:
            fb.fill(color)
            self.display.blit(fb_data, x, y, width, height)
            y -= height

    def test_blit_row(self, bg_color):
        self.display.fill(bg_color)

        def row_gen(row):
            while True:
                yield row

        x = 0
        y = 0
        width = self.display.width
        height = self.display.height // len(COMMON_COLORS)

        for color in COMMON_COLORS:
            row = color.to_bytes(2, 'big') * width
            self.display.blit_rows(row_gen(row), x, y, width, height)
            y += height

        sleep(1)

        y = self.display.height - height
        for color in COMMON_COLORS:
            row = color.to_bytes(2, 'big') * width
            self.display.blit_rows(row_gen(row), x, y, width, height)
            y -= height

    def test_scroll(self, bg_color):
        self.display.fill(bg_color)

        x = 0
        y = 0
        width = self.display.width
        height = self.display.height // len(COMMON_COLORS) - 3

        for _ in range(6):
            for color in COMMON_COLORS:
                self.display.fill_rect(x, y, width, height, color)
                y += height
                sleep(0.1)
