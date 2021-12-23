import fonts
import utime
from apps.pico_spacegame.actor import Actor
from apps.pico_spacegame.constants import *
from apps.pico_spacegame.enemies import Enemies
from apps.pico_spacegame.player import Player
from apps.pico_spacegame.shot import Shot
from drivers import color565


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

    def __init__(self, display, touch, text_color=color565(255, 255, 255), bg_color=color565(0, 0, 0)):
        self.display = display
        self.width = display.width
        self.height = display.height

        self.touch = touch
        self.touch.int_handler = self.touch_handler
        self.touch_x = -1
        self.touch_y = -1

        self.text_color = text_color
        self.bg_color = bg_color

        self.spaceship = Actor(display, "/apps/pico_spacegame/spacecraftimg.spr", self.bg_color, (120, 200))
        self.enemies = Enemies(display, self.bg_color)

        self.timer = utime.time()

        # List to track self.shots
        self.shots = []
        # Prevent continuous self.shots
        self.shot_last_time = utime.time()
        # min. time between self.shots
        self.shot_delay = 1

        self.player1 = Player(display)

        self.game_status = GAME_READY

    def touch_handler(self, x, y):
        if x > 20 and x < self.width - 20 and y > 20 and y < self.height - 20:
            self.touch_x = x
            self.touch_y = y

    # similar to pgzero draw

    def draw(self):
        # Display game  over message
        if (self.game_status == GAME_READY):
            self.display.text("Space Game", 40, 90,  self.text_color, self.bg_color, fonts.tt32)
            self.display.text("Click to start", 50, 160,  self.text_color, self.bg_color, fonts.tt24)
        elif (self.game_status == GAME_OVER):
            self.display.text("Game Over", 45, 90,  self.text_color, self.bg_color, fonts.tt32)
            self.display.text("Score "+str(self.player1.score), 75, 160,  self.text_color, self.bg_color, fonts.tt24)
        elif (self.game_status == GAME_PLAY):
            self.spaceship.draw()
            self.enemies.draw()
            for this_shot in self.shots:
                this_shot.draw()
            # Display score and number of lives
            self.display.text(str(self.player1.score), 10, 10,  self.text_color, self.bg_color, fonts.tt24)
            self.display.text(self.player1.get_score_string(), 200, 10,
                              self.text_color, self.bg_color, fonts.tt24)

    # similar to pgzero update
    def update(self):
        if self.touch_x > 0 and self.touch_x < 50 and self.touch_y < 50:
            # exit on touch of upper left corner
            return False
        if (self.game_status == GAME_READY):
            # wait for button press then start game
            if (self.touch_x >= 0):
                self.game_status = GAME_PLAY
                self.player1.reset()
                self.display.fill(self.bg_color)
        elif self.game_status == GAME_OVER:
            if ((utime.time() > self.timer + 4) and self.touch_x >= 0):
                self.game_status = GAME_PLAY
                self.player1.reset()
                self.display.fill(self.bg_color)
        elif (self.game_status == GAME_PLAY):
            self.enemies.update()
            # check for end of level
            if (self.enemies.check_crash((self.spaceship.x, self.spaceship.y), self.spacecraft_hit_pos)):
                self.timer = utime.time()
                self.player1.lives -= 1
                if (self.player1.lives <= 0):
                    self.game_status = GAME_OVER
            if (self.touch_x >= 0):
                self.spaceship.x = self.touch_x
                if ((self.shot_last_time + self.shot_delay) < utime.time()):
                    self.shots.append(Shot(self.display, (self.spaceship.x, self.spaceship.y-25), self.bg_color))
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
        return True

    # This is based on a binary image file (RGB565) with the same dimensions as the screen
    def blit_image_file(self, filename):
        def row_gen():
            with open(filename, "rb") as file:
                position = 0
                eof = 0
                while position < (self.width * self.height * 2):
                    if not eof:
                        current_row = file.read(self.width*2)
                        eof = len(current_row) == 0
                    if eof:
                        yield self.bg_color.to_bytes(2, 'big') * width
                    position += width*2
                    yield current_row
        self.display.blit_rows(row_gen(), 0, 0, self.width, self.height)

    def run(self):
        self.display.fill(self.bg_color)
        # Do nothing - but continue to display the image
        while True:
            self.draw()
            if not self.update():
                break
