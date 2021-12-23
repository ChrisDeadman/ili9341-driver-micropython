import gc
import os

from extensions import input
from utils import COMMON_COLORS

from diagnostics.draw_test import DrawTest
from diagnostics.font_test import FontTest
from diagnostics.touch_test import TouchTest


class Diagnostics(object):

    def __init__(self, display, touch):
        self.display = display
        self.touch = touch
        self.bg_color_idx = 0

    def run(self):
        draw_test = DrawTest(self.display)
        font_test = FontTest(self.display)
        touch_test = TouchTest(self.display, self.touch)

        while True:
            print('Diagnostics menu:')
            tests = [
                ['Free RAM', self._get_free_ram],
                ['Free Disk Space', lambda: self._get_free_diskspace('/')],
                ['Display info', lambda: print(self.display.get_info())],
                ['Clear display', lambda: self.display.fill(COMMON_COLORS[self.bg_color_idx])],
                ['Change brightness', lambda: self.display.set_brightness(input.read_int('brightness>'))],
                ['Cycle background color', self._cylce_bg_color],
                ['Draw test', lambda: draw_test.execute(COMMON_COLORS[self.bg_color_idx])],
                ['Font test', lambda: font_test.execute(COMMON_COLORS[self.bg_color_idx])],
                ['Touch test', lambda: touch_test.execute(COMMON_COLORS[self.bg_color_idx])],
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

    def _get_free_ram(self):
        free_space_kb = gc.mem_free() // 1024
        print(f'Free RAM: {free_space_kb}kB')

    def _get_free_diskspace(self, path):
        fs_stats = os.statvfs(path)
        f_bsize = fs_stats[0]
        f_bavail = fs_stats[4]
        free_space_kb = (f_bsize * f_bavail) // 1024
        print(f'Free disk space: {free_space_kb}kB')
