from extensions import fb, input
from fonts import FONTS
from utils import COMMON_COLORS


class FontTest(object):

    def __init__(self, display):
        self.display = display
        self.fbuf = fb.FrameBufferEx(None, self.display.width, self.display.height, fbuf=self.display)
        self.font = None

    def run(self, bg_color):
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
        self.fbuf.fill(bg_color)

        x = 0
        y = 0
        for color in COMMON_COLORS:
            self.fbuf.text('Colored text', x, y, color, font=self.font)
            y += self.font.height() + 1

    def test_background(self, bg_color):
        self.fbuf.fill(bg_color)

        x = 0
        y = 0
        for color_idx, bg_color in enumerate(COMMON_COLORS):
            color = COMMON_COLORS[len(COMMON_COLORS)-color_idx-1]
            self.fbuf.text('Text with background', x, y, color, bg=bg_color, font=self.font)
            y += self.font.height() + 1
            color_idx -= 1

    def load_font(self):
        print('Select font:')
        for idx, name in enumerate(FONTS.keys()):
            print(f'{idx}: {name}')

        font_idx = input.read_int('font>')
        if font_idx < len(FONTS):
            self.font = list(FONTS.values())[font_idx]
