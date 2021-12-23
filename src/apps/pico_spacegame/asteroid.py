import utime
from apps.pico_spacegame.constants import *
from extensions import fb


class Asteroid:

    def __init__(self, display, start_time, image_size, start_pos, velocity, color, bg_color):
        self.display = display
        if (image_size == "asteroid_sml"):
            self.size = 5
        elif (image_size == "asteroid_med"):
            self.size = 8
        else:
            self.size = 12
        self.start_pos = start_pos
        #self.x = start_pos[0]
        #self.y = start_pos[1]
        # start position is off screen
        self.x = -20
        self.y = -20
        self.start_time = start_time
        self.velocity = velocity
        self.color = color
        self.bg_color = bg_color
        self.status = STATUS_WAITING
        self.needs_draw = True

    def draw(self):
        if self.needs_draw:
            if self.status == STATUS_VISIBLE:
                fb.fill_circle(self.display, int(self.x), int(self.y-self.velocity), self.size, self.bg_color)
                fb.fill_circle(self.display, int(self.x), int(self.y), self.size, self.color)
            elif self.status == STATUS_DESTROYED:
                fb.fill_circle(self.display, int(self.x), int(self.y-self.velocity), self.size, self.bg_color)
                self.needs_draw = False

    def update(self, level_time):
        if self.status == STATUS_WAITING:
            # Check if time reached
            if (utime.time() > level_time + self.start_time):
                #print ("Starting new asteroid")
                # Reset to start position
                self.x = self.start_pos[0]
                self.y = self.start_pos[1]
                self.status = STATUS_VISIBLE
        elif self.status == STATUS_VISIBLE:
            self.y += self.velocity

    def reset(self):
        self.status = STATUS_WAITING
        self.needs_draw = True

    def hit(self):
        self.status = STATUS_DESTROYED

    def collidepoint(self, point_x, point_y):
        # simplified check based on rect around centre of asteroid
        if (point_x > (self.x - self.size) and point_x < (self.x + self.size) and point_y > (self.y - self.size) and point_y < (self.y + self.size)):
            return True
        return False
