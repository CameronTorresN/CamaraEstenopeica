# Stenopeic camera screen — image flash controller

Button press → screen flashes a random image from a folder you preload
onto the Pi, for about 0.3 seconds, then goes dark again.

## 1. Enable SPI

```bash
sudo raspi-config
# Interface Options -> SPI -> Enable
sudo reboot
```

## 2. Install dependencies

```bash
sudo apt update
sudo apt install -y python3-pip
pip3 install adafruit-circuitpython-rgb-display adafruit-blinka gpiozero Pillow
```

## 3. Wiring (matches the defaults in config.py)

| Display pin | Pi physical pin | BCM GPIO |
|-------------|------------------|----------|
| GND         | 6                | —        |
| VCC         | 4                | —        |
| SCL         | 18               | GPIO24   |
| SDA         | 19               | GPIO10   |
| RST         | 15               | GPIO22   |
| DC          | 13               | GPIO27   |
| CS          | 11               | GPIO17   |
| BL          | 12               | GPIO18   |
| SDA-O       | not connected    | —        |

SCL/CS aren't on the Pi's hardware SPI0 clock/CS pins, so the display runs
over software (bit-banged) SPI — see the `bitbangio` note in `display.py`.

The shutter button is on GPIO4 (physical pin 7) → GND (physical pin 9).
Everything pin-related lives in `config.py`, including the fixed backlight
level (`DISPLAY_BRIGHTNESS`) and flash duration (`FLASH_DURATION_SECONDS`).

## 4. Load your images

```bash
mkdir -p /home/pi/stenopeic_images
# copy in the images you want shown (.jpg/.jpeg/.png/.bmp)
```

By default `main.py` picks a random image on each press (won't repeat the
same one twice in a row). Pass `mode="sequential"` to `ImageBank(...)` if
you'd rather it cycle through them in folder order instead.

## 5. Run it

```bash
python3 main.py
```

Press Ctrl+C to stop.

## Files

- `config.py` — every pin number and the fixed brightness level, in one place
- `display.py` — ST7789 driver: shows an image, clears the screen
- `image_bank.py` — picks the next image from your preloaded folder
- `main.py` — ties it together: button → show image

## Notes

- `DISPLAY_ROTATION` in `config.py` — 0/90/180/270, depending on how the
  screen ends up mounted in the housing.
- `DISPLAY_BRIGHTNESS` in `config.py` — backlight level during the flash,
  0.0 to 1.0. The backlight sits at 0 the rest of the time.
- `FLASH_DURATION_SECONDS` in `config.py` — how long the backlight stays on
  per press. Defaults to 0.3s.
