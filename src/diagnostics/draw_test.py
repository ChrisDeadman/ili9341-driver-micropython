import os

from drivers import color565
from extensions import input, re
from fonts import FONTS
from utils import COMMON_COLORS


class DrawTest(object):

    WIDTH = 150

    def __init__(self, display):
        self.display = display

    def execute(self, bg_color):
        while True:
            print('Draw tests:')
            tests = [
                ['fill_rect', lambda: self.test_fill_rect(bg_color)],
                ['blit', lambda: self.test_blit(bg_color)],
                ['Return', None]
            ]
            for idx, test in enumerate(tests):
                print(f'{idx}: {test[0]}')

            test_idx = input.read_int('test>')
            if test_idx >= len(tests) - 1:
                break

            tests[test_idx][1]()

    def test_fill_rect(self, bg_color):
        x = 0
        y = 0
        height = self.display.height // len(COMMON_COLORS)
        self.display.fill(bg_color)
        for color in COMMON_COLORS:
            self.display.fill_rect(x, y, self.WIDTH, height, color)
            y += height

    def test_blit(self, bg_color):
        def row_gen(row):
            while True:
                yield row

        x = 0
        y = 0
        height = self.display.height // len(COMMON_COLORS)
        self.display.fill(bg_color)

        for color in COMMON_COLORS:
            row = color.to_bytes(2, 'big') * self.WIDTH

            self.display.blit(row_gen(row), x, y, self.WIDTH, height)
            y += height

        y = self.display.height - height
        for color in COMMON_COLORS:
            row = color.to_bytes(2, 'big') * self.WIDTH

            self.display.blit(row_gen(row), x, y, self.WIDTH, height)
            y -= height
