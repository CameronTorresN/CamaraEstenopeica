"""ST7789 display driver (hardware SPI). Backlight is off except during a flash."""

import time

import board
import busio
import digitalio
from adafruit_rgb_display import st7789
from PIL import Image, ImageOps

import config


class Display:
    def __init__(self):
        self._backlight = digitalio.DigitalInOut(getattr(board, f"D{config.DISPLAY_BL_PIN}"))
        self._backlight.direction = digitalio.Direction.OUTPUT
        self._backlight.value = False  # dark at idle

        spi = busio.SPI(board.SCLK, MOSI=board.MOSI)
        self._panel = st7789.ST7789(
            spi,
            cs=digitalio.DigitalInOut(getattr(board, f"D{config.DISPLAY_CS_PIN}")),
            dc=digitalio.DigitalInOut(getattr(board, f"D{config.DISPLAY_DC_PIN}")),
            rst=digitalio.DigitalInOut(getattr(board, f"D{config.DISPLAY_RST_PIN}")),
            width=config.DISPLAY_WIDTH,
            height=config.DISPLAY_HEIGHT,
            baudrate=config.DISPLAY_BAUDRATE,
            rotation=config.DISPLAY_ROTATION,
        )
        self.width = self._panel.width
        self.height = self._panel.height
        self.clear()

    def _prepare(self, path):
        img = Image.open(path).convert("RGB")
        # Scale to cover the screen, then center-crop.
        scale = max(self.width / img.width, self.height / img.height)
        new_size = (round(img.width * scale), round(img.height * scale))
        img = img.resize(new_size, Image.LANCZOS)
        left = (img.width - self.width) // 2
        top = (img.height - self.height) // 2
        img = img.crop((left, top, left + self.width, top + self.height))
        if config.INVERT_IMAGES:
            img = ImageOps.invert(img)
        return img

    def clear(self):
        self._backlight.value = False
        self._panel.image(Image.new("RGB", (self.width, self.height), (0, 0, 0)))

    def flash(self, path, duration=None):
        """Draw the image while dark, light the backlight, then go dark again."""
        duration = config.FLASH_DURATION_SECONDS if duration is None else duration
        img = self._prepare(path)
        self._panel.image(img)
        self._backlight.value = True
        time.sleep(duration)
        self._backlight.value = False
        self.clear()
