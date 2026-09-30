"""Picks a random image from the preloaded folder."""

import os
import random

import config


class ImageBank:
    def __init__(self, directory=None):
        self.directory = directory or config.IMAGE_BANK_DIR
        self.files = self._scan()
        self._last = None

    def _scan(self):
        if not os.path.isdir(self.directory):
            raise FileNotFoundError(f"Image folder not found: {self.directory}")
        files = [
            os.path.join(self.directory, f)
            for f in sorted(os.listdir(self.directory))
            if f.lower().endswith(config.IMAGE_EXTENSIONS)
        ]
        if not files:
            raise FileNotFoundError(f"No images found in {self.directory}")
        return files

    def random_image(self):
        """Random pick, avoiding an immediate repeat when there's more than one."""
        choices = [f for f in self.files if f != self._last] or self.files
        self._last = random.choice(choices)
        return self._last
