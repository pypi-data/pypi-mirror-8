# -*- coding: utf-8 -*-
import colorsys

# noinspection PyAugmentAssignment
# import hashlib


def name2rgb(name, basename, hue):
    r, g, b = colorsys.hsv_to_rgb(hue / 360.0, .8, .7)
    return tuple(int(x * 256) for x in [r, g, b])


def brightness(r, g, b):
    """From w3c (range 0..255).
    """
    return (r * 299 + g * 587 + b * 114) / 1000


def brightnessdiff(a, b):
    """greater than 125 is good.
    """
    return abs(brightness(*a) - brightness(*b))


def colordiff((r, g, b), (r2, g2, b2)):
    """From w3c (greater than 500 is good).
       (range [0..765])
    """
    return (
        max(r, r2) - min(r, r2) +
        max(g, g2) - min(g, g2) +
        max(b, b2) - min(b, b2)
    )


def foreground(background, *options):
    """Find the best foreground color from `options` based on `background`
       color.
    """
    def absdiff(a, b):
        return brightnessdiff(a, b)
        # return 3 * brightnessdiff(a, b) + colordiff(a, b)
    diffs = [(absdiff(background, color), color) for color in options]
    diffs.sort(reverse=True)
    return diffs[0][1]


def rgb2css((r, g, b)):
    """Convert rgb to hex.
    """
    return '#%02x%02x%02x' % (r, g, b)

#
# def color_from_name(name):
#     """Convert `name` to a hex color.
#     """
#     r, g, b = name2rgb(name)
#     return '#%02x%02x%02x' % (r, g, b)
#
