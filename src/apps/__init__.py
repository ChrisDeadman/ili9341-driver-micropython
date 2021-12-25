
import gc

from drivers import color565
from extensions import input


class AppLauncher(object):

    def __init__(self, display, touch):
        self.display = display
        self.touch = touch

    def run(self, bg_color):
        while True:
            print('Apps:')
            tests = [
                ['pico-spacegame', self._run_pico_spacegame],
                ['Return', None],
            ]
            for idx, test in enumerate(tests):
                print(f'{idx}: {test[0]}')

            test_idx = input.read_int('option>')
            if test_idx >= len(tests) - 1:
                break

            self.display.scroll_abs(0, 0)
            gc.collect()
            tests[test_idx][1]()
            gc.collect()

    def _run_pico_spacegame(self):
        from apps.pico_spacegame.spacegame import SpaceGame
        self.display.set_brightness(0xCFFF)
        self.display.fill(color565(0x15, 0xb0, 0x1a))
        SpaceGame(self.display, self.touch).run()
