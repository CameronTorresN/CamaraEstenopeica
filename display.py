"""
Wrapper around the 2.8" ST7789 SPI display.

This wiring puts SCL/CS on GPIOs that aren't the Pi's hardware SPI0
clock/CS lines, so it talks over software (bit-banged) SPI via bitbangio
rather than board.SPI().

Requires: adafruit-circuitpython-rgb-display, adafruit-blinka, Pillow
    pip install adafruit-circuitpython-rgb-display adafruit-blinka Pillow
"""

import bitbangio
import board
import digitalio
from PIL import Image
from adafruit_rgb_display import st7789

import config


class Display:
    def __init__(self):
        clock_pin = getattr(board, f"D{config.DISPLAY_CLOCK_PIN}")
        mosi_pin = getattr(board, f"D{config.DISPLAY_MOSI_PIN}")
        spi = bitbangio.SPI(clock=clock_pin, MOSI=mosi_pin)  # no MISO wired

        cs_pin = digitalio.DigitalInOut(getattr(board, f"D{config.DISPLAY_CS_PIN}"))
        dc_pin = digitalio.DigitalInOut(getattr(board, f"D{config.DISPLAY_DC_PIN}"))
        rst_pin = digitalio.DigitalInOut(getattr(board, f"D{config.DISPLAY_RST_PIN}"))

        self.panel = st7789.ST7789(
            spi,
            cs=cs_pin,
            dc=dc_pin,
            rst=rst_pin,
            width=config.DISPLAY_WIDTH,
            height=config.DISPLAY_HEIGHT,
            rotation=config.DISPLAY_ROTATION,
        )
        self.width = self.panel.width
        self.height = self.panel.height

        # Optional PWM backlight, driven separately from the SPI panel itself.
        self._backlight = None
        if config.DISPLAY_BL_PIN is not None:
            import RPi.GPIO as GPIO

            GPIO.setmode(GPIO.BCM)
            GPIO.setup(config.DISPLAY_BL_PIN, GPIO.OUT)
            self._backlight = GPIO.PWM(config.DISPLAY_BL_PIN, 1000)
            self._backlight.start(config.DISPLAY_BRIGHTNESS * 100)

    def set_brightness(self, fraction):
        """fraction: 0.0 (off) to 1.0 (full brightness)."""
        if self._backlight is not None:
            fraction = max(0.0, min(1.0, fraction))
            self._backlight.ChangeDutyCycle(fraction * 100)

    def show_image(self, image_path):
        """Fit a preloaded image to the screen and display it."""
        image = Image.open(image_path).convert("RGB")
        image = self._fit_to_screen(image)
        self.panel.image(image)

    def clear(self):
        self.panel.image(Image.new("RGB", (self.width, self.height), (0, 0, 0)))

    def _fit_to_screen(self, image):
        img_ratio = image.width / image.height
        screen_ratio = self.width / self.height
        if img_ratio > screen_ratio:
            new_height = self.height
            new_width = int(new_height * img_ratio)
        else:
            new_width = self.width
            new_height = int(new_width / img_ratio)
        image = image.resize((new_width, new_height))
        left = (new_width - self.width) / 2
        top = (new_height - self.height) / 2
        return image.crop((left, top, left + self.width, top + self.height))
