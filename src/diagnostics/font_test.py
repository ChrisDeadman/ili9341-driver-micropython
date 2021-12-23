import os

from drivers import color565
from extensions import input, re
from fonts import FONTS
from utils import COMMON_COLORS


class FontTest(object):

    def __init__(self, display):
        self.display = display
        self.font = None

    def execute(self, bg_color):
        if not self.font:
            self.load_font()

        if not self.font:
            print('no font selected, test aborted.')
            return

        while self.font:
            print('Font tests:')
            tests = [
                ['Normal test', lambda: self.test_normal(bg_color)],
                ['Background test', lambda: self.test_background(bg_color)],
                ['Change font', self.load_font],
                ['Return', None]
            ]
            for idx, test in enumerate(tests):
                print(f'{idx}: {test[0]}')

            test_idx = input.read_int('test>')
            if test_idx >= len(tests) - 1:
                break

            tests[test_idx][1]()

    def test_normal(self, bg_color):
        self.display.fill(bg_color)
        x = 0
        y = 0
        for color_idx in range(len(COMMON_COLORS)):
            color = COMMON_COLORS[color_idx]
            self.display.text('Colored text', x, y, color, font=self.font)
            y += self.font.height() + 1

    def test_background(self, bg_color):
        self.display.fill(bg_color)
        x = 0
        y = 0
        for color_idx in range(len(COMMON_COLORS)):
            bg_color_idx = len(COMMON_COLORS) - color_idx - 1
            color = COMMON_COLORS[color_idx]
            bg_color = COMMON_COLORS[bg_color_idx]
            self.display.text('Text with background', x, y, color, bg=bg_color, font=self.font)
            y += self.font.height() + 1

    def load_font(self):
        print('Select font:')
        for idx, name in enumerate(FONTS.keys()):
            print(f'{idx}: {name}')

        font_idx = input.read_int('font>')
        if font_idx < len(FONTS):
            self.font = list(FONTS.values())[font_idx]
