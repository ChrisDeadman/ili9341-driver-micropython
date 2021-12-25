import utime
from apps.pico_spacegame.constants import *
from drivers import color565


class Shot:

    def __init__(self, fbuf, start_position, color=color565(255, 255, 255)):
        self.fbuf = fbuf
        self.x = start_position[0]
        self.y = start_position[1]
        self.color = color

    def update(self):
        self.y -= 2

    def draw(self):
        if self.y <= 0:
            return
        self.fbuf.fill_polygon(3, int(self.x+1), int(self.y+1), 2, self.color)
