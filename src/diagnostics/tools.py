import gc
import os

from extensions import input


class Tools(object):

    def __init__(self, display):
        self.display = display

    def execute(self):
        while True:
            print('Tools:')
            tools = [
                ['Show free RAM', self._get_free_ram],
                ['Show free disk space', lambda: self._get_free_diskspace('/')],
                ['Show display info', lambda: print(self.display.get_info())],
                ['Change brightness', lambda: self.display.set_brightness(input.read_int('brightness>'))],
                ['Return', None]
            ]
            for idx, tool in enumerate(tools):
                print(f'{idx}: {tool[0]}')

            tool_idx = input.read_int('tool>')
            if tool_idx >= len(tools) - 1:
                break

            tools[tool_idx][1]()

    def _get_free_ram(self):
        free_space_kb = gc.mem_free() // 1024
        print(f'Free RAM: {free_space_kb}kB')

    def _get_free_diskspace(self, path):
        fs_stats = os.statvfs(path)
        f_bsize = fs_stats[0]
        f_bavail = fs_stats[4]
        free_space_kb = (f_bsize * f_bavail) // 1024
        print(f'Free disk space: {free_space_kb}kB')
