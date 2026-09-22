"""
Main loop for the screen: on each button press, draw a random preloaded
image while the backlight is off, then flash the backlight on for
config.FLASH_DURATION_SECONDS before switching it back off. The screen
stays dark the rest of the time.
"""

import threading
import time

from gpiozero import Button

import config
from display import Display
from image_bank import ImageBank

busy_lock = threading.Lock()


def show_next_image(display, bank):
    if not busy_lock.acquire(blocking=False):
        return  # already mid-flash, ignore the extra press
    try:
        image_path = bank.next_image()
        print(f"Flashing: {image_path}")
        display.show_image(image_path)                     # drawn while dark
        display.set_brightness(config.DISPLAY_BRIGHTNESS)   # backlight on
        time.sleep(config.FLASH_DURATION_SECONDS)
        display.set_brightness(0)                           # backlight off
    finally:
        busy_lock.release()


def main():
    display = Display()
    bank = ImageBank(mode="random")

    display.clear()
    display.set_brightness(0)  # stay dark at idle

    button = Button(config.BUTTON_PIN, bounce_time=0.05)
    button.when_pressed = lambda: show_next_image(display, bank)

    print("Ready. Press the button to flash an image.")

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Shutting down.")
    finally:
        display.set_brightness(0)
        display.clear()


if __name__ == "__main__":
    main()
