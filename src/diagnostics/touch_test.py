from extensions import fb, input
from utils import COMMON_COLORS


class TouchTest(object):

    def __init__(self, display, touch):
        self.display = display
        self.fbuf = fb.FrameBufferEx(None, self.display.width, self.display.height, fbuf=self.display)
        self.touch = touch
        self.pen_color_idx = 1

    def run(self, bg_color):
        try:
            self.touch.int_handler = self.touch_handler
            while True:
                print('Options:')
                tests = [
                    ['Clear display', lambda: self.fbuf.fill(bg_color)],
                    ['Cycle pen color', self.cylce_pen_color],
                    ['Return', None]
                ]
                for idx, test in enumerate(tests):
                    print(f'{idx}: {test[0]}')

                print('touch handler active, draw something...')
                test_idx = input.read_int('option>')
                if test_idx >= len(tests) - 1:
                    break

                tests[test_idx][1]()
        finally:
            self.touch.int_handler = None

    def touch_handler(self, x, y):
        print(f'touch: {x}, {y}')
        y += self.fbuf.scroll()[1]
        self.fbuf.fill_circle(x, y, 4, COMMON_COLORS[self.pen_color_idx])

    def cylce_pen_color(self):
        self.pen_color_idx += 1
        if self.pen_color_idx >= len(COMMON_COLORS):
            self.pen_color_idx = 1
