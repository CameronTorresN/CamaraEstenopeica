"""
Pin assignments and settings.
Adjust these to match your actual wiring.
"""

# --- Display (2.8" ST7789 SPI, 240x320) ---
# SCL and CS are NOT on the Pi's hardware SPI0 clock/CS pins (GPIO11 / GPIO8),
# so the display talks over software (bit-banged) SPI instead of board.SPI().
DISPLAY_CLOCK_PIN = 24     # GPIO24 (physical pin 18) - SCL
DISPLAY_MOSI_PIN = 10      # GPIO10 (physical pin 19) - SDA
DISPLAY_CS_PIN = 17        # GPIO17 (physical pin 11) - CS
DISPLAY_DC_PIN = 27        # GPIO27 (physical pin 13) - DC
DISPLAY_RST_PIN = 22       # GPIO22 (physical pin 15) - RST
DISPLAY_BL_PIN = 18        # GPIO18 (physical pin 12) - BL, PWM backlight
DISPLAY_BRIGHTNESS = 1.0   # backlight level while flashing, 0.0 to 1.0
DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 320
DISPLAY_ROTATION = 90      # rotate 0/90/180/270 depending on how it's mounted
# SDA-O (MISO) is not wired - this display is write-only, which bitbangio.SPI allows.

# --- Shutter button ---
BUTTON_PIN = 4              # GPIO4 (physical pin 7), other leg to GND (physical pin 9)

# --- Flash timing ---
# The screen stays dark (backlight off) at idle and only lights up for this
# long when a button press shows an image.
FLASH_DURATION_SECONDS = 0.3

# --- Preloaded images ---
IMAGE_BANK_DIR = "/home/ctorres/stenopeic_images"   # images you import onto the Pi
