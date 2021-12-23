"""Main entry point."""
from machine import PWM, SPI, Pin

from diagnostics import Diagnostics
from drivers import Display, Touch, color565
from extensions import input
from utils import COMMON_COLORS


def main():
    spi1 = SPI(0, baudrate=1000000, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
    spi2 = SPI(1, baudrate=51200000, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
    pwm = PWM(Pin(15))

    display = Display(spi2, pwm, cs=Pin(13), dc=Pin(14))
    touch = Touch(spi1, cs=Pin(9), int_pin=Pin(8))

    try:
        Diagnostics(display, touch).run()
    finally:
        display.cleanup()


main()
