
from extensions import input


class AppLauncher(object):

    def __init__(self, display, touch):
        self.display = display
        self.touch = touch

    def run(self, bg_color):
        while True:
            print('Apps:')
            tests = [
                ['pico-spacegame', lambda: self._run_pico_spacegame(bg_color)],
                ['Return', None],
            ]
            for idx, test in enumerate(tests):
                print(f'{idx}: {test[0]}')

            test_idx = input.read_int('option>')
            if test_idx >= len(tests) - 1:
                break

            tests[test_idx][1]()

    def _run_pico_spacegame(self, bg_color):
        from apps.pico_spacegame.spacegame import SpaceGame
        self.display.set_brightness(0xCFFF)
        print('touch top-left corner to exit...')
        SpaceGame(self.display, self.touch, bg_color=bg_color).run()
