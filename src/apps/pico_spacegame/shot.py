import utime
from apps.pico_spacegame.constants import *
from drivers import color565
from extensions import fb


class Shot:

    def __init__(self, display, start_position, bg_color, color=color565(255, 255, 255)):
        self.display = display
        self.bg_color = bg_color
        self.x = start_position[0]
        self.y = start_position[1]
        self.color = color

    def update(self):
        self.y -= 6

    def draw(self):
        if self.y <= 0:
            return
        fb.fill_polygon(self.display, 3, int(self.x), int(self.y+6), 2, self.bg_color)
        fb.fill_polygon(self.display, 3, int(self.x), int(self.y), 2, self.color)

    def destroy(self):
        fb.fill_polygon(self.display, 3, int(self.x), int(self.y+6), 2, self.bg_color)
        self.y = -1
