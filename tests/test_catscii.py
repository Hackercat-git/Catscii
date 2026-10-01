import os
import sys
import unittest

from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import catscii  # noqa: E402
from styles import get_ramp  # noqa: E402


def make_gradient_image(size=(20, 10)):
    """A simple left-to-right black-to-white gradient for predictable tests."""
    img = Image.new("RGB", size)
    w, h = size
    for x in range(w):
        value = int(255 * x / (w - 1))
        for y in range(h):
            img.putpixel((x, y), (value, value, value))
    return img


class TestCatscii(unittest.TestCase):
    def test_resize_keeps_aspect_correction(self):
        img = make_gradient_image((40, 40))
        resized = catscii.resize_image(img, width=20)
        self.assertEqual(resized.width, 20)
        self.assertEqual(resized.height, round(20 * 1.0 * catscii.ASPECT_CORRECTION))

    def test_pixel_to_char_dark_and_light(self):
        ramp = get_ramp("standard")
        self.assertEqual(catscii.pixel_to_char(0, ramp), ramp[0])
        self.assertEqual(catscii.pixel_to_char(255, ramp), ramp[-1])

    def test_render_ascii_shape(self):
        img = make_gradient_image((10, 5))
        art = catscii.render_ascii(img, "standard", use_color=False)
        lines = art.split("\n")
        self.assertEqual(len(lines), 5)
        self.assertEqual(len(lines[0]), 10)

    def test_render_ascii_with_color_contains_ansi(self):
        img = make_gradient_image((5, 3))
        art = catscii.render_ascii(img, "standard", use_color=True)
        self.assertIn("\x1b[38;2;", art)
        self.assertIn(catscii.ANSI_RESET, art)

    def test_strip_ansi_removes_codes(self):
        colored = f"{catscii.ansi_color(1, 2, 3)}X{catscii.ANSI_RESET}"
        self.assertEqual(catscii.strip_ansi(colored), "X")

    def test_unknown_style_raises(self):
        with self.assertRaises(ValueError):
            get_ramp("not-a-real-style")

    def test_missing_file_exits(self):
        with self.assertRaises(SystemExit):
            catscii.load_image("does-not-exist.png")

    def test_to_html_wraps_colored_output(self):
        img = make_gradient_image((4, 2))
        art = catscii.render_ascii(img, "standard", use_color=True)
        html = catscii.to_html(art)
        self.assertIn("<span style=", html)
        self.assertIn("<pre>", html)


if __name__ == "__main__":
    unittest.main()
