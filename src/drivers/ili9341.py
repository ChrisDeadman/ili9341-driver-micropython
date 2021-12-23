# An efficient and extensible ILI934X display driver for micropython.
#
# "More or less" implements framebuf.FrameBuffer interface.
# Supports drawing text using fonts.
# Supports "font-to-py" compatible fonts out of the box (https://github.com/peterhinch/micropython-font-to-py; defaults to tt14.py)
# Tries to support auto-scrolling but has a few issues:
# - only works properly when rotation=0
# - when drawing off-screen first blit rows after scroll looks borked
# - if YOU find a fix for one of those please open issue or merge-request here https://github.com/ChrisDeadman/ili9341-driver-micropython
#   or post somewhere in case I'm gone.
#
# MIT License; Copyright (c) 2022 Christopher Hubmann
#
# Here are a few sources I took inspiration from (also MIT licensed to date):
# - https://github.com/rdagger/micropython-ili9341/blob/master/ili9341.py
# - https://github.com/jeffmer/micropython-ili9341/blob/master/ili934xnew.py
#


from time import sleep

import fonts
import ustruct
from ubinascii import hexlify
from ucollections import OrderedDict


def color565(r, g, b):
    """Return RGB565 color value.

    Args:
        r (int): Red value.
        g (int): Green value.
        b (int): Blue value.
    """
    return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3


class Display(object):
    """IL9341 Display driver (serial interface).

    Only supports 16-bit color (RGB565)
    """

    # Command constants from ILI9341 datasheet
    NOP = const(0x00)  # No-op
    SWRESET = const(0x01)  # Software reset
    RDDID = const(0x04)  # Read display ID info
    RDDST = const(0x09)  # Read display status
    SLPIN = const(0x10)  # Enter sleep mode
    SLPOUT = const(0x11)  # Exit sleep mode
    PTLON = const(0x12)  # Partial mode on
    NORON = const(0x13)  # Normal display mode on
    RDMODE = const(0x0A)  # Read display power mode
    RDMADCTL = const(0x0B)  # Read display MADCTL
    RDPIXFMT = const(0x0C)  # Read display pixel format
    RDIMGFMT = const(0x0D)  # Read display image format
    RDSIGMODE = const(0x0E)  # Read display signal mode
    RDSELFDIAG = const(0x0F)  # Read display self-diagnostic
    INVOFF = const(0x20)  # Display inversion off
    INVON = const(0x21)  # Display inversion on
    GAMMASET = const(0x26)  # Gamma set
    DISPLAY_OFF = const(0x28)  # Display off
    DISPLAY_ON = const(0x29)  # Display on
    SET_COLUMN = const(0x2A)  # Column address set
    SET_PAGE = const(0x2B)  # Page address set
    WRITE_RAM = const(0x2C)  # Memory write
    READ_RAM = const(0x2E)  # Memory read
    PTLAR = const(0x30)  # Partial area
    VSCRDEF = const(0x33)  # Vertical scrolling definition
    MADCTL = const(0x36)  # Memory access control
    VSCRSADD = const(0x37)  # Vertical scrolling start address
    PIXFMT = const(0x3A)  # COLMOD: Pixel format set
    WRITE_DISPLAY_BRIGHTNESS = const(0x51)  # Brightness hardware dependent!
    READ_DISPLAY_BRIGHTNESS = const(0x52)
    WRITE_CTRL_DISPLAY = const(0x53)
    READ_CTRL_DISPLAY = const(0x54)
    WRITE_CABC = const(0x55)  # Write Content Adaptive Brightness Control
    READ_CABC = const(0x56)  # Read Content Adaptive Brightness Control
    WRITE_CABC_MINIMUM = const(0x5E)  # Write CABC Minimum Brightness
    READ_CABC_MINIMUM = const(0x5F)  # Read CABC Minimum Brightness
    FRMCTR1 = const(0xB1)  # Frame rate control (In normal mode/full colors)
    FRMCTR2 = const(0xB2)  # Frame rate control (In idle mode/8 colors)
    FRMCTR3 = const(0xB3)  # Frame rate control (In partial mode/full colors)
    INVCTR = const(0xB4)  # Display inversion control
    DFUNCTR = const(0xB6)  # Display function control
    PWCTR1 = const(0xC0)  # Power control 1
    PWCTR2 = const(0xC1)  # Power control 2
    PWCTRA = const(0xCB)  # Power control A
    PWCTRB = const(0xCF)  # Power control B
    VMCTR1 = const(0xC5)  # VCOM control 1
    VMCTR2 = const(0xC7)  # VCOM control 2
    RDID1 = const(0xDA)  # Read ID 1
    RDID2 = const(0xDB)  # Read ID 2
    RDID3 = const(0xDC)  # Read ID 3
    RDID4 = const(0xD3)  # Read ID 4
    GMCTRP1 = const(0xE0)  # Positive gamma correction
    GMCTRN1 = const(0xE1)  # Negative gamma correction
    DTCA = const(0xE8)  # Driver timing control A
    DTCB = const(0xEA)  # Driver timing control B
    POSC = const(0xED)  # Power on sequence control
    ENABLE3G = const(0xF2)  # Enable 3 gamma control
    PUMPRC = const(0xF7)  # Pump ratio control

    ROTATE = {
        0: 0x48,
        90: 0x28,
        180: 0x88,
        270: 0xE8
    }

    def __init__(self, spi, pwm, cs, dc, width=240, height=320, rotation=0):
        """Initialize IL9341 Display.

        Args:
            spi (Class Spi):  SPI interface for OLED
            pwm (Class PWM):  PWM for controlling the backlight
            cs (Class Pin):  Chip select pin
            dc (Class Pin):  Data/Command pin
            width (Optional int): Screen width (default 240)
            height (Optional int): Screen height (default 320)
            rotation (Optional int): Rotation must be 0 (default), 90, 180 or 270
        """
        self.spi = spi
        self.pwm = pwm
        self.cs = cs
        self.dc = dc
        self.width = width
        self.height = height
        self.scroll_pos = 0
        if rotation not in self.ROTATE.keys():
            raise ValueError('Rotation must be 0, 90, 180 or 270.')
        else:
            self.rotation = self.ROTATE[rotation]

        # 4 rows blit buffer
        self.blit_buf = bytearray(width*4*2)

        # Initialize GPIO pins
        self.pwm.freq(500)
        self.pwm.duty_u16(16384)
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)

        # Send initialization commands
        self.write_cmd(self.SWRESET)  # Software reset
        sleep(.1)
        self.write_cmd(self.PWCTRB, 0x00, 0xC1, 0x30)  # Pwr ctrl B
        self.write_cmd(self.POSC, 0x64, 0x03, 0x12, 0x81)  # Pwr on seq. ctrl
        self.write_cmd(self.DTCA, 0x85, 0x00, 0x78)  # Driver timing ctrl A
        self.write_cmd(self.PWCTRA, 0x39, 0x2C, 0x00, 0x34, 0x02)  # Pwr ctrl A
        self.write_cmd(self.PUMPRC, 0x20)  # Pump ratio control
        self.write_cmd(self.DTCB, 0x00, 0x00)  # Driver timing ctrl B
        self.write_cmd(self.PWCTR1, 0x23)  # Pwr ctrl 1
        self.write_cmd(self.PWCTR2, 0x10)  # Pwr ctrl 2
        self.write_cmd(self.VMCTR1, 0x3E, 0x28)  # VCOM ctrl 1
        self.write_cmd(self.VMCTR2, 0x86)  # VCOM ctrl 2
        self.write_cmd(self.MADCTL, self.rotation)  # Memory access ctrl
        self.write_cmd(self.VSCRSADD, 0x00)  # Vertical scrolling start address
        self.write_cmd(self.PIXFMT, 0x55)  # COLMOD: Pixel format
        self.write_cmd(self.FRMCTR1, 0x00, 0x18)  # Frame rate ctrl
        self.write_cmd(self.DFUNCTR, 0x08, 0x82, 0x27)
        self.write_cmd(self.ENABLE3G, 0x00)  # Enable 3 gamma ctrl
        self.write_cmd(self.GAMMASET, 0x01)  # Gamma curve selected
        self.write_cmd(self.GMCTRP1,
                       0x0F, 0x31, 0x2B, 0x0C, 0x0E, 0x08, 0x4E,
                       0xF1, 0x37, 0x07, 0x10, 0x03, 0x0E, 0x09, 0x00)
        self.write_cmd(self.GMCTRN1,
                       0x00, 0x0E, 0x14, 0x03, 0x11, 0x07, 0x31,
                       0xC1, 0x48, 0x08, 0x0F, 0x0C, 0x31, 0x36, 0x0F)
        self.write_cmd(self.SLPOUT)  # Exit sleep
        sleep(.1)
        self.write_cmd(self.DISPLAY_ON)  # Display on
        sleep(.1)
        self.fill(0)

    def cleanup(self):
        """Clean up resources."""
        self.set_brightness(0)
        self.fill(0)
        self.pwm.deinit()
        self.display_off()
        self.spi.deinit()
        print('display off')

    def display_off(self):
        """Turn display off."""
        self.write_cmd(self.DISPLAY_OFF)

    def display_on(self):
        """Turn display on."""
        self.write_cmd(self.DISPLAY_ON)

    def fill(self, c):
        """Fill display with the specified color."""
        self.scroll_pos = 0
        self.scroll(0)
        self.fill_rect(0, 0, self.width, self.height, c)

    def pixel(self, x, y, c=None):
        """Draw a single pixel with the specified color or return pixel color if c is not provided."""
        if c:
            self.draw_chunk(c.to_bytes(2, 'big'), x, y, x, y)
        else:
            return 1  # TODO

    def hline(self, x, y, w, c):
        """Draw a horizontal line."""
        self.draw_chunk(c.to_bytes(2, 'big') * w, x, y, x+w-1, y)

    def vline(self, x, y, h, c):
        """Draw a vertical line."""
        self.draw_chunk(c.to_bytes(2, 'big') * h, x, y, x, y+h-1)

    def line(self, x1, y1, x2, y2, c):
        """Draw a line."""
        # Check for horizontal line
        if y1 == y2:
            if x1 > x2:
                x1, x2 = x2, x1
            self.hline(x1, y1, x2 - x1 + 1, c)
            return
        # Check for vertical line
        if x1 == x2:
            if y1 > y2:
                y1, y2 = y2, y1
            self.vline(x1, y1, y2 - y1 + 1, c)
            return
        # Changes in x, y
        dx = x2 - x1
        dy = y2 - y1
        # Determine how steep the line is
        is_steep = abs(dy) > abs(dx)
        # Rotate line
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        # Swap start and end points if necessary
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        # Recalculate differentials
        dx = x2 - x1
        dy = y2 - y1
        # Calculate error
        error = dx >> 1
        ystep = 1 if y1 < y2 else -1
        y = y1
        for x in range(x1, x2 + 1):
            # Had to reverse HW ????
            if not is_steep:
                self.pixel(x, y, c)
            else:
                self.pixel(y, x, c)
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx

    def rect(self, x, y, w, h, c):
        """Draw a rectangle."""
        x2 = x + w - 1
        y2 = y + h - 1
        self.hline(x, y, w, c)
        self.hline(x, y2, w, c)
        self.vline(x, y, h, c)
        self.vline(x2, y, h, c)

    def fill_rect(self, x, y, w, h, c):
        """Draw a filled rectangle."""
        row = c.to_bytes(2, 'big') * w

        def row_gen():
            while True:
                yield row

        self.blit(row_gen(), x, y, w, h)

    def text(self, s, x, y, c=1, bg=-1, font=fonts.tt14):
        """Draw some text."""
        bg = bg if bg >= 0 else 1 if c == 0 else 0
        key = -1 if bg >= 0 else bg
        text_width = font.get_width(s)

        c_bytes = c.to_bytes(2, 'big')
        bg_bytes = bg.to_bytes(2, 'big')

        # generates text horizontally, line by line
        def row_gen():
            div, remainder = divmod(font.height(), 8)
            num_glyph_rows = div+1 if remainder else div
            for char_y in range(font.height()):
                row = bytearray(bg_bytes * text_width)
                pixel_idx = 0
                for ch in s:
                    glyph, char_width = font.get_ch(ch)
                    glyph_row_idx, glyph_row_y = divmod(char_y, 8)
                    for glyph_column_idx in range(char_width):
                        glyph_row = glyph[(glyph_column_idx*num_glyph_rows)+glyph_row_idx]
                        if (glyph_row >> glyph_row_y) & 1:
                            row[pixel_idx] = c_bytes[0]
                            row[pixel_idx+1] = c_bytes[1]
                        pixel_idx += 2
                yield row

        self.blit(row_gen(), x, y, text_width, font.height(), key)
        return text_width

    def blit(self, row_gen, x, y, w, h, key=- 1):
        """Draw a number of rows from row generator."""
        chunk_height = len(self.blit_buf) // 2 // w
        chunk_count, remainder = divmod(h, chunk_height)

        for c in range(0, chunk_count):
            self.blit_chunk_row(row_gen, x, y, w, chunk_height, key)
            y += chunk_height

        if remainder:
            self.blit_chunk_row(row_gen, x, y, w, remainder, key)

    def blit_chunk_row(self, row_gen, x, y, w, h, key=- 1):
        """Draw a number of rows from row generator."""
        draw_w = min(self.width, w)
        pixel_w = draw_w*2
        draw_bytes = pixel_w*h
        if draw_bytes > len(self.blit_buf):
            raise ValueError('{draw_w}*{h} is too big for blit buffer')

        x2 = x+draw_w-1
        y2 = y+h-1
        buf_idx = 0
        for _ in range(h):
            row = next(row_gen)
            # only draw up to display width
            self.blit_buf[buf_idx:buf_idx+pixel_w] = row[:pixel_w]
            buf_idx += pixel_w
        self.draw_chunk(self.blit_buf[:draw_bytes], x, y, x2, y2, key)

    def draw_chunk(self, data, x1, y1, x2, y2, key=- 1):
        """Write a chunk of data to display.
            TODO: transparency with key
        """
        w = x2 - x1 + 1
        h = y2 - y1 + 1

        # check if coordinates extend past display boundaries
        # (ignore y because autoscrolling)
        if x1 < 0:
            print(f'x-coordinate: {x1} below minimum of 0.')
            return True
        if y1 < 0:
            print(f'y-coordinate: {y1} below minimum of 0.')
            return True
        if x2 >= self.width:
            print(f'x-coordinate: {x2} above maximum of {self.width-1}.')
            return True
        if self.scroll_pos - y1 >= self.height:
            print(f'ignoring chunk, y1 is on previous page ({self.scroll_pos}-{y1} >= {self.height})')
            return
        if h >= self.height:
            print(f'chunk too big to fit on display ({y2}-{y1} >= {self.height})')
            return

        #
        # auto-scrolling
        # First junk looks broken, no fix found so far :(
        # Code looks alright as far as I can still tell since in the end this was all just trial-and-error tbh :D
        #
        data_idx = 0
        if y2 - self.height >= self.scroll_pos:
            y2 %= self.height
            scroll_y = (y2 - self.scroll_pos + 1) % self.height
            remainder = scroll_y - h
            if remainder:
                data_idx = remainder*w*2
                self.write_ram(data[:data_idx], x1, y1 % self.height, x2, self.height-1)
            y1 = 0
            y2 = y1+h-remainder-1
            self.scroll(scroll_y)
        elif self.scroll_pos:
            y1 = (y1 + self.scroll_pos) % self.height
            y2 = (y2 + self.scroll_pos) % self.height

        self.write_ram(data[data_idx:], x1, y1, x2, y2)

    def scroll(self, y):
        """Scroll display vertically by y pixels."""
        self.scroll_pos += y
        self.write_cmd(self.VSCRSADD, *ustruct.pack('>H', self.scroll_pos % self.height))

    def set_scroll_margins(self, top, bottom):
        """Set the height of the top and bottom scroll margins."""
        if top + bottom <= self.height:
            middle = self.height - (top + bottom)
            print(f'scroll_margins: top={top}, middle={middle}, bottom={bottom}')
            self.write_cmd(self.VSCRDEF, *ustruct.pack('>HHH', top, middle, bottom))

    def get_info(self):
        """Get device information."""
        info = []
        info.append(f'ID: {hexlify(self.read_cmd(self.RDDID, 3))}')
        info.append(f'ID4: {hexlify(self.read_cmd(self.RDID4, 3))}')
        info.append(f'Status: {hexlify(self.read_cmd(self.RDDST, 4))}')
        info.append(f'Power Mode: {hexlify(self.read_cmd(self.RDMODE, 1))}')
        info.append(f'MADCTL: {hexlify(self.read_cmd(self.RDMADCTL, 1))}')
        info.append(f'Pixel format: {hexlify(self.read_cmd(self.RDPIXFMT, 1))}')
        info.append(f'Image format: {hexlify(self.read_cmd(self.RDIMGFMT, 1))}')
        info.append(f'Signal mode: {hexlify(self.read_cmd(self.RDSIGMODE, 1))}')
        info.append(f'Self-diagnostic: {hexlify(self.read_cmd(self.RDSELFDIAG, 1))}')
        return '\n'.join(info)

    def set_brightness(self, brightness):
        """Set backlight intensity.

        Args:
            brightness (int): Brightness between 0 and 0xFFFF.
        """
        self.pwm.duty_u16(brightness)

    def write_ram(self, data, x1, y1, x2, y2):
        """Write data to ram at column/page area defined by x/y coords."""
        self.write_cmd(self.SET_COLUMN, *ustruct.pack('>HH', x1, x2))
        self.write_cmd(self.SET_PAGE, *ustruct.pack('>HH', y1, y2))
        self.write_cmd(self.WRITE_RAM)
        self.write_data(data)

    def read_cmd(self, command, num_bytes):
        """Write command to OLED and read response.

        Args:
            command (byte): ILI9341 command code.
            num_bytes (int): Number of bytes to read.
        """
        self.dc(0)
        self.cs(0)
        buffer = bytearray(2 + num_bytes)
        buffer[0] = command
        self.spi.write_readinto(buffer, buffer)
        self.cs(1)
        return self._discard_bits(buffer[1:], 1)[:-1]

    def write_cmd(self, command, *args):
        """Write command to OLED.

        Args:
            command (byte): ILI9341 command code.
            *args (optional bytes): Data to transmit.
        """
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([command]))
        self.cs(1)
        # handle any passed data
        if len(args) > 0:
            self.write_data(bytearray(args))

    def write_data(self, data):
        """Write data to OLED."""
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)

    def _discard_bits(self, data, num_bits):
        """Discard the first num_bits bits and shift the rest accordingly."""
        for idx in range(len(data)):
            data[idx] = data[idx] << num_bits
            if idx + 1 < len(data):
                data[idx] |= data[idx + 1] >> (8 - num_bits)
        return data
