import fonts
import utime
from apps.pico_spacegame.actor import Actor
from apps.pico_spacegame.constants import *
from apps.pico_spacegame.enemies import Enemies
from apps.pico_spacegame.player import Player
from apps.pico_spacegame.shot import Shot
from drivers import color565
from extensions import fb


class SpaceGame(object):
    # positions relative to pos where crash would be hit
    spacecraft_hit_pos = [
        (-15, 5),
        (-10, 0),
        (-5, -5),
        (-3, -10),
        (0, -15),
        (-3, -10),
        (-5, -5),
        (10, 0),
        (15, 5)
    ]

    def __init__(self, display, touch, text_color=color565(0xff, 0xff, 0xff), bg_color=color565(0, 0, 0)):
        self.display = display
        self.width = min(display.width, 140)  # limit width (memory limit)
        self.height = min(display.height, 140)  # limit height (memory limit)
        fbdata = bytearray(self.width*self.height*2)
        self.fbuf = fb.FrameBufferEx(fbdata, self.width, self.height)
        self.display_x = (self.display.width-self.width)//2
        self.display_y = (self.display.height-self.height)//2

        self.touch = touch
        self.touch.int_handler = self.touch_handler
        self.touch_x = -1
        self.touch_y = -1

        self.text_color = text_color
        self.bg_color = bg_color

        self.spaceship = Actor(self.fbuf, "/apps/pico_spacegame/spacecraftimg.spr", (self.width//2, self.height-20))
        self.enemies = Enemies(self.fbuf)

        self.timer = utime.time()

        # List to track self.shots
        self.shots = []
        # Prevent continuous self.shots
        self.shot_last_time = utime.time()
        # min. time between self.shots
        self.shot_delay = 1

        self.player1 = Player(self.fbuf)

        self.game_status = GAME_READY

    def touch_handler(self, x, y):
        if x > 20 and x <= self.display.width - 20 and y > 20 and y <= self.display.height - 20:
            self.touch_x = x - self.display_x
            self.touch_y = y - self.display_y

    # similar to pgzero draw

    def draw(self):
        self.fbuf.fill(self.bg_color)
        # Display game over message
        if (self.game_status == GAME_READY):
            self.fbuf.text("Space Game", 0, self.height*1//3, self.text_color, self.bg_color, fonts.tt24)
            self.fbuf.text("Click to start", 30, self.height*2//3, self.text_color, self.bg_color, fonts.tt14)
        elif (self.game_status == GAME_OVER):
            self.fbuf.text("Game Over", 10, self.height*1//3, self.text_color, self.bg_color, fonts.tt24)
            self.fbuf.text("Score "+str(self.player1.score), 40, self.height*2//3,
                           self.text_color, self.bg_color, fonts.tt14)
        elif (self.game_status == GAME_PLAY):
            self.spaceship.draw()
            self.enemies.draw()
            for this_shot in self.shots:
                this_shot.draw()
            # Display score and number of lives
            self.fbuf.text(str(self.player1.score), 10, 10, self.text_color, self.bg_color, fonts.tt14)
            self.fbuf.text(self.player1.get_score_string(), self.width-20, 10,
                           self.text_color, self.bg_color, fonts.tt14)
        # update the display with the framebuffer
        self.display.blit(self.fbuf, self.display_x, self.display_y)

    # similar to pgzero update
    def update(self):
        if (self.game_status == GAME_READY):
            # wait for button press then start game
            if (self.touch_x >= 0):
                self.game_status = GAME_PLAY
                self.player1.reset()
        elif self.game_status == GAME_OVER:
            if ((utime.time() > self.timer + 4) and self.touch_x >= 0):
                self.game_status = GAME_PLAY
                self.player1.reset()
        elif (self.game_status == GAME_PLAY):
            self.enemies.update()
            # check for end of level
            if (self.enemies.check_crash((self.spaceship.x, self.spaceship.y), self.spacecraft_hit_pos)):
                self.timer = utime.time()
                self.player1.lives -= 1
                if (self.player1.lives <= 0):
                    self.game_status = GAME_OVER
            if (self.touch_x >= 0 and self.touch_x < self.width):
                self.spaceship.x = self.touch_x
                if ((self.shot_last_time + self.shot_delay) < utime.time()):
                    self.shots.append(Shot(self.fbuf, (self.spaceship.x, self.spaceship.y-25)))
                    self.shot_last_time = utime.time()
            # Update existing self.shots
            for this_shot in self.shots:
                # Update position of shot
                this_shot.update()
                if this_shot.y <= 0:
                    self.shots.remove(this_shot)
                # Check if hit asteroid or enemy
                elif self.enemies.check_shot(this_shot.x, this_shot.y):
                    self.player1.score += 10
                    # remove shot (otherwise it continues to hit others)
                    self.shots.remove(this_shot)

        # clear touch input
        self.touch_x = -1
        self.touch_y = -1

    def run(self):
        # Do nothing - but continue to display the image
        while True:
            self.draw()
            self.update()
