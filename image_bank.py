"""
Manages the bank of preloaded images that get shown on the screen.
"""

import os
import random

import config

VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp")


class ImageBank:
    def __init__(self, mode="random"):
        """
        mode:
          "random"     - picks a random image each press (default)
          "sequential" - cycles through images in folder order, wrapping around
        """
        self.mode = mode
        self.images = self._load_images()
        self._index = 0
        self._last_shown = None

    def _load_images(self):
        if not os.path.isdir(config.IMAGE_BANK_DIR):
            raise FileNotFoundError(
                f"Image bank folder not found: {config.IMAGE_BANK_DIR}. "
                "Create it and drop in the images you want to show."
            )
        files = sorted(
            f for f in os.listdir(config.IMAGE_BANK_DIR)
            if f.lower().endswith(VALID_EXTENSIONS)
        )
        if not files:
            raise FileNotFoundError(
                f"No images found in {config.IMAGE_BANK_DIR}. Add some first."
            )
        return [os.path.join(config.IMAGE_BANK_DIR, f) for f in files]

    def next_image(self):
        if self.mode == "sequential":
            image_path = self.images[self._index]
            self._index = (self._index + 1) % len(self.images)
            return image_path

        # random mode: avoid showing the same image twice in a row if possible
        if len(self.images) == 1:
            return self.images[0]
        choices = [i for i in self.images if i != self._last_shown]
        image_path = random.choice(choices)
        self._last_shown = image_path
        return image_path
