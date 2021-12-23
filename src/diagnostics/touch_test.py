from drivers import color565
from extensions import input
from utils import COMMON_COLORS


class TouchTest(object):

    def __init__(self, display, touch):
        self.display = display
        self.touch = touch
        self.pen_color_idx = 1

    def execute(self, bg_color):
        try:
            self.touch.int_handler = self.touch_handler
            while True:
                print('Options:')
                tests = [
                    ['Clear display', lambda: self.display.fill(bg_color)],
                    ['Cycle pen color', self.cylce_pen_color],
                    ['Return', None]
                ]
                for idx, test in enumerate(tests):
                    print(f'{idx}: {test[0]}')

                test_idx = input.read_int('option>')
                if test_idx >= len(tests) - 1:
                    break

                tests[test_idx][1]()
        finally:
            self.touch.int_handler = None

    def touch_handler(self, x, y):
        print(f'touch: {x}, {y}')
        self.display.pixel(x, y, COMMON_COLORS[self.pen_color_idx])

    def cylce_pen_color(self):
        self.pen_color_idx += 1
        if self.pen_color_idx >= len(COMMON_COLORS):
            self.pen_color_idx = 1
