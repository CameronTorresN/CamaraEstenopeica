"""
Pin assignments and settings for the stenopeic camera.
Edit the pins here to match your wiring. Nothing else needs to change.
"""

# --- Display (2.8" ST7789 SPI, 240x320) ---
# Hardware SPI0:
#   SCL -> physical pin 23 (GPIO11, SCLK)  <- moved from pin 18
#   SDA -> physical pin 19 (GPIO10, MOSI)
# These two are fixed by the Pi. The pins below can be any free GPIO.
DISPLAY_CS_PIN = 17        # physical pin 11 - CS
DISPLAY_DC_PIN = 27        # physical pin 13 - DC
DISPLAY_RST_PIN = 22       # physical pin 15 - RST
DISPLAY_BL_PIN = 18        # physical pin 12 - BL (backlight, on/off)
DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 320
DISPLAY_ROTATION = 90      # 0 / 90 / 180 / 270 depending on how it's mounted
DISPLAY_BAUDRATE = 4000000 # 4 MHz is safe. Try 24000000 for faster draws.
INVERT_IMAGES = True       # show images as negatives

# --- Shutter button ---
# One leg -> physical pin 7 (GPIO4), other leg -> physical pin 9 (GND)
BUTTON_PIN = 4

# --- Image bank ---
IMAGE_BANK_DIR = "/home/ctorres/stenopeic_images"
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp")

# --- Timing ---
FLASH_DURATION_SECONDS = 0.3
DEBOUNCE_SECONDS = 0.05
