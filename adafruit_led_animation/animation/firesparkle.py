# SPDX-FileCopyrightText: 2020 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`firesparkle`
================================================================================

Fire sparkle for CircuitPython helper library for LED animations.

* Author(s): Matt Stec, based on RainbowSparkle by Kattni Rembor

Implementation Notes
--------------------

**Hardware:**

* `Adafruit NeoPixels <https://www.adafruit.com/category/168>`_
* `Adafruit DotStars <https://www.adafruit.com/category/885>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

"""

import random
from adafruit_led_animation.animation.rainbow import Rainbow

# Fire and Flames Color Palette from https://color-hex.com/color-palette/5111
FIRE = [(161, 0, 0), (234, 35, 0), (255, 129, 0), (242, 85, 0), (216, 0, 0)]

class FireSparkle(Rainbow):
    """Fire sparkle animation.

    :param pixel_object: The initialised LED object.
    :param float speed: Animation refresh rate in seconds, e.g. ``0.1``.
    :param float period: Period to cycle the fire over in seconds.  Default 5.
    :param int num_sparkles: The number of sparkles to display. Defaults to 1/20 of the pixel
                             object length.
    :param list colors: List of (R, G, B) colors to cycle through. Default ``FIRE``.
    :param str name: Name of animation (optional, useful for sequences and debugging).
    :param float background_brightness: The brightness of the background fire. Defaults to
                                        ``0.2`` or 20 percent.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        pixel_object,
        speed,
        period=5,
        num_sparkles=None,
        colors=FIRE,
        name=None,
        background_brightness=0.2,
    ):
        self._num_sparkles = num_sparkles
        if num_sparkles is None:
            self._num_sparkles = max(1, int(len(pixel_object) / 20))
        self._sparkle_duration = 2
        self._background_brightness = background_brightness
        self._bright_colors = None
        super().__init__(
            pixel_object=pixel_object,
            speed=speed,
            period=period,
            step=step,
            name=name,
            precompute_rainbow=False,
        )
        self.colors = colors

    def generate_rainbow(self):
        if self.colors is None:
            super().generate_rainbow()
        self._bright_colors = self.colors[:]
        for i, color in enumerate(self.colors):
            if isinstance(self.colors[i], int):
                self.colors[i] = (
                    int(self._background_brightness * ((color & 0xFF0000) >> 16)),
                    int(self._background_brightness * ((color & 0xFF00) >> 8)),
                    int(self._background_brightness * (color & 0xFF)),
                )
            else:
                self.colors[i] = (
                    int(self._background_brightness * color[0]),
                    int(self._background_brightness * color[1]),
                    int(self._background_brightness * color[2]),
                )

    def after_draw(self):
        self.show()
        pixels = [
            random.randint(0, len(self.pixel_object) - 1)
            for n in range(self._num_sparkles)
        ]
        for pixel in pixels:
            self.pixel_object[pixel] = self._bright_colors[
                (self._wheel_index + pixel) % len(self._bright_colors)
            ]
