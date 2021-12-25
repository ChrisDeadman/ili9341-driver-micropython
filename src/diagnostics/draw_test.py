from time import sleep

from extensions import fb, input
from utils import COMMON_COLORS


class DrawTest(object):

    def __init__(self, display):
        self.display = display
        self.fbuf = fb.FrameBufferEx(None, self.display.width, self.display.height, fbuf=self.display)

    def run(self, bg_color):
        while True:
            print('Draw tests:')
            tests = [
                ['rectangles', lambda: self.test_rectangles(bg_color)],
                ['cirles', lambda: self.test_circles(bg_color)],
                ['polygons', lambda: self.test_polygons(bg_color)],
                ['blit', lambda: self.test_blit(bg_color)],
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
        self.fbuf.fill(bg_color)

        x = 0
        y = 0
        width = self.fbuf.width
        height = self.fbuf.height // len(COMMON_COLORS) - 1
        for color in COMMON_COLORS:
            if y < self.fbuf.height // 2:
                self.fbuf.rect(x, y, width, height, color)
            else:
                self.fbuf.fill_rect(x, y, width, height, color)
            y += height + 1

    def test_circles(self, bg_color):
        self.fbuf.fill(bg_color)

        r = 1
        x = r
        y = int(self.fbuf.height * 1 // 5)
        for color in COMMON_COLORS:
            if x+r*2 >= self.fbuf.width:
                break
            self.fbuf.circle(x, y, r, color)
            r += 3
            x += r*2

        r = 1
        x = r
        y = int(self.fbuf.height * 2 // 5)
        for color in COMMON_COLORS:
            if x+r*2 >= self.fbuf.width:
                break
            self.fbuf.fill_circle(x, y, r, color)
            r += 3
            x += r*2

        r = 1
        x = 6
        y = int(self.fbuf.height * 3 // 5)
        for color in reversed(COMMON_COLORS):
            if x+r*2 >= self.fbuf.width:
                break
            self.fbuf.ellipse(x, y, r+4, r, color)
            r += 3
            x += r*2

        r = 1
        x = r
        y = int(self.fbuf.height * 4 // 5)
        for color in reversed(COMMON_COLORS):
            if x+r*2 >= self.fbuf.width:
                break
            self.fbuf.fill_ellipse(x, y, r, r+4, color)
            r += 3
            x += r*2

    def test_polygons(self, bg_color):
        self.fbuf.fill(bg_color)

        r = 4
        x = r
        y = int(self.fbuf.height * 1 // 3)
        sides = 3
        for color in COMMON_COLORS:
            if x+r*2 >= self.fbuf.width:
                break
            self.fbuf.polygon(sides, x, y, r, color)
            r += 3
            x += r*2 + 1
            sides += 1

        r = 4
        x = r
        y = int(self.fbuf.height * 2 // 3)
        sides = 3
        for color in reversed(COMMON_COLORS):
            if x+r*2 >= self.fbuf.width:
                break
            self.fbuf.fill_polygon(sides, x, y, r, color)
            r += 3
            x += r*2 + 1
            sides += 1

    def test_blit(self, bg_color):
        x = 0
        y = 0
        width = self.fbuf.width
        height = self.fbuf.height // len(COMMON_COLORS)

        fbuf = fb.FrameBufferEx(bytearray(width * height * 2), width, height)

        for color in COMMON_COLORS:
            fbuf.fill(color)
            self.fbuf.blit(fbuf, x, y)
            y += height

        sleep(1)

        y = self.fbuf.height - height
        for color in COMMON_COLORS:
            fbuf.fill(color)
            self.fbuf.blit(fbuf, x, y)
            y -= height

    def test_scroll(self, bg_color):
        self.display.scroll_abs(0, 0)
        self.fbuf.fill(bg_color)

        x = 0
        y = 0
        width = self.fbuf.width
        height = self.fbuf.height // len(COMMON_COLORS) - 3

        for _ in range(6):
            for color in COMMON_COLORS:
                self.fbuf.fill_rect(x, y, width, height, color)
                y += height
                sleep(0.1)
