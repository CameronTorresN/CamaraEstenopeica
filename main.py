"""Button press -> screen flashes a random preloaded image -> dark again."""

import time

import board
import digitalio

import config
from display import Display
from image_bank import ImageBank


def main():
    bank = ImageBank()
    display = Display()

    button = digitalio.DigitalInOut(getattr(board, f"D{config.BUTTON_PIN}"))
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP  # pressed = False (shorted to GND)

    print(f"Ready. {len(bank.files)} images loaded. Press the shutter. Ctrl+C to quit.")
    try:
        while True:
            if not button.value:
                time.sleep(config.DEBOUNCE_SECONDS)
                if not button.value:
                    path = bank.random_image()
                    print(f"Flashing {path}")
                    display.flash(path)
                    while not button.value:  # wait for release
                        time.sleep(0.01)
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass
    finally:
        display.clear()


if __name__ == "__main__":
    main()
