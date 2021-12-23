from extensions import input
from utils import COMMON_COLORS

from diagnostics.draw_test import DrawTest
from diagnostics.font_test import FontTest
from diagnostics.tools import Tools
from diagnostics.touch_test import TouchTest


class Diagnostics(object):

    def __init__(self, display, touch):
        self.display = display
        self.touch = touch
        self.bg_color_idx = 0

    def run(self):
        tools = Tools(self.display)
        draw_test = DrawTest(self.display)
        font_test = FontTest(self.display)
        touch_test = TouchTest(self.display, self.touch)

        while True:
            bg_color = COMMON_COLORS[self.bg_color_idx]
            print('Diagnostics menu:')
            tests = [
                ['Clear display', lambda: self.display.fill(bg_color)],
                ['Cycle background color', self._cylce_bg_color],
                ['Tools', lambda: tools.execute()],
                ['Draw tests', lambda: draw_test.execute(bg_color)],
                ['Font tests', lambda: font_test.execute(bg_color)],
                ['Touch tests', lambda: touch_test.execute(bg_color)],
                ['Exit', None],
            ]
            for idx, test in enumerate(tests):
                print(f'{idx}: {test[0]}')

            test_idx = input.read_int('option>')
            if test_idx >= len(tests) - 1:
                break

            tests[test_idx][1]()

    def _cylce_bg_color(self):
        self.bg_color_idx += 1
        if self.bg_color_idx >= len(COMMON_COLORS):
            self.bg_color_idx = 0
        self.display.fill(COMMON_COLORS[self.bg_color_idx])
