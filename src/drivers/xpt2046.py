# A minimalistic but smart XPT2046 touch screen controller driver.
#
# Recalibrates automagically during usage.
#
# If YOU have improvements please open issue or merge-request here https://github.com/ChrisDeadman/ili9341-driver-micropython
# or post somewhere in case I'm gone.
#
# MIT License; Copyright (c) 2022 Christopher Hubmann
#

from machine import Pin


class Touch(object):
    """XPT2046 touch screen controller driver."""

    # Command constants from ILI9341 datasheet
    GET_X = const(0b11010000)  # X position
    GET_Y = const(0b10010000)  # Y position
    GET_Z1 = const(0b10110000)  # Z1 position
    GET_Z2 = const(0b11000000)  # Z2 position
    GET_TEMP0 = const(0b10000000)  # Temperature 0
    GET_TEMP1 = const(0b11110000)  # Temperature 1
    GET_BATTERY = const(0b10100000)  # Battery monitor
    GET_AUX = const(0b11100000)  # Auxiliary input to ADC

    def __init__(self, spi, cs, int_pin=None, int_handler=None,
                 width=240, height=320,
                 x_min=100, x_max=1962, y_min=1900, y_max=100):
        """Initialize XPT2046 touch screen controller.

        Args:
            spi (Class Spi):  SPI interface for OLED
            cs (Class Pin):  Chip select pin
            int_pin (Class Pin):  Touch controller interrupt pin
            int_handler (function): Handler for screen interrupt
            width (int): Width of LCD screen
            height (int): Height of LCD screen
            x_min (int): Minimum x coordinate
            x_max (int): Maximum x coordinate (exchange x_min and x_max if inverted)
            y_min (int): Minimum Y coordinate
            y_max (int): Maximum Y coordinate (exchange y_min and y_max if inverted)
        """
        self.spi = spi
        self.cs = cs
        self.cs.init(self.cs.OUT, value=1)
        self.rx_buf = bytearray(3)  # Receive buffer
        self.tx_buf = bytearray(3)  # Transmit buffer
        self.width = width
        self.height = height

        # initialize calibration
        self.x_inverted = x_min > x_max
        if self.x_inverted:
            self.x_min = x_max
            self.x_max = x_min
        else:
            self.x_min = x_min
            self.x_max = x_max

        self.y_inverted = y_min > y_max
        if self.y_inverted:
            self.y_min = y_max
            self.y_max = y_min
        else:
            self.y_min = y_min
            self.y_max = y_max

        self.recalibrate(self.x_min, self.y_max, force=True)

        # setup interrupt handling
        self.int_handler = int_handler
        if int_pin is not None:
            int_pin.init(Pin.IN, Pin.PULL_UP)
            int_pin.irq(trigger=Pin.IRQ_FALLING, handler=self._int_handler)

    def _int_handler(self, pin):
        """Touch interrupt handler."""
        if not pin.value():
            buff = self.raw_touch()
            if buff is not None and self.int_handler:
                x, y = self.normalize(*buff)
                self.int_handler(x, y)

    def raw_touch(self):
        """Read raw X,Y touch values."""
        x = self.send_command(self.GET_X)
        y = self.send_command(self.GET_Y)
        return (x, y)

    def send_command(self, command):
        """Write command to XT2046."""
        self.tx_buf[0] = command
        self.cs(0)
        self.spi.write_readinto(self.tx_buf, self.rx_buf)
        self.cs(1)
        return (self.rx_buf[1] << 4) | (self.rx_buf[2] >> 4)

    def normalize(self, x, y):
        """Normalize mean X,Y values to match LCD screen."""
        self.recalibrate(x, y)  # auto recalibration

        x = (x - self.x_min) * self.x_multiplier
        if self.x_inverted:
            x = self.width - x

        y = (y - self.y_min) * self.y_multiplier
        if self.y_inverted:
            y = self.height - y

        return int(x), int(y)

    def recalibrate(self, x, y, force=False):
        changed = force
        if x < self.x_min:
            self.x_min = x
            changed = True
        if x > self.x_max:
            self.x_max = x
            changed = True
        if y < self.y_min:
            self.y_min = y
            changed = True
        if y > self.y_max:
            self.y_max = y
            changed = True

        if changed:
            self.x_multiplier = self.width / (self.x_max - self.x_min)
            self.y_multiplier = self.height / (self.y_max - self.y_min)

        return changed
