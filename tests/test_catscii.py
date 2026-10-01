import os
import sys
import tempfile
import unittest

from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import catscii  # noqa: E402
from styles import STYLES, get_ramp  # noqa: E402


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

    def test_render_ascii_invert_flips_chars(self):
        """With invert=True the darkest pixel should map to the lightest char."""
        img = make_gradient_image((10, 2))
        art_normal = catscii.render_ascii(img, "standard", use_color=False, invert=False)
        art_inverted = catscii.render_ascii(img, "standard", use_color=False, invert=True)
        # First character (darkest pixel) should differ between normal and inverted
        self.assertNotEqual(art_normal[0], art_inverted[0])
        # Last character of first row (lightest pixel) should also differ
        first_line_normal = art_normal.split("\n")[0]
        first_line_inverted = art_inverted.split("\n")[0]
        self.assertNotEqual(first_line_normal[-1], first_line_inverted[-1])

    def test_all_styles_render(self):
        """Every style in STYLES should produce output without errors."""
        img = make_gradient_image((8, 4))
        for style_name in STYLES:
            with self.subTest(style=style_name):
                art = catscii.render_ascii(img, style_name, use_color=False)
                self.assertTrue(len(art) > 0)

    def test_strip_ansi_removes_codes(self):
        colored = f"{catscii.ansi_color(1, 2, 3)}X{catscii.ANSI_RESET}"
        self.assertEqual(catscii.strip_ansi(colored), "X")

    def test_unknown_style_raises(self):
        with self.assertRaises(ValueError):
            get_ramp("not-a-real-style")

    def test_missing_file_raises_catscii_error(self):
        with self.assertRaises(catscii.CatsciiError):
            catscii.load_image("does-not-exist.png")

    def test_missing_file_exits_via_main(self):
        with self.assertRaises(SystemExit):
            catscii.main(["does-not-exist.png"])

    def test_to_html_wraps_colored_output(self):
        img = make_gradient_image((4, 2))
        art = catscii.render_ascii(img, "standard", use_color=True)
        html = catscii.to_html(art)
        self.assertIn("<span style=", html)
        self.assertIn("<pre>", html)

    def test_to_html_plain_text_escapes_html(self):
        """to_html on plain (no-color) art should still produce valid HTML."""
        img = make_gradient_image((4, 2))
        art = catscii.render_ascii(img, "standard", use_color=False)
        html = catscii.to_html(art)
        self.assertIn("<pre>", html)
        self.assertNotIn("\x1b[", html)

    def test_output_txt_saves_plain_text(self):
        img = make_gradient_image((10, 5))
        art = catscii.render_ascii(img, "standard", use_color=True)
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w") as f:
            tmp = f.name
        try:
            catscii.main(["examples/input-sample.jpg", "-o", tmp, "--width", "10"])
            with open(tmp, encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn("\x1b[", content)
        finally:
            os.unlink(tmp)

    def test_output_html_saves_html_file(self):
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
            tmp = f.name
        try:
            catscii.main(["examples/input-sample.jpg", "-o", tmp, "--width", "10", "--color"])
            with open(tmp, encoding="utf-8") as f:
                content = f.read()
            self.assertIn("<!DOCTYPE html>", content)
            self.assertIn("<pre>", content)
        finally:
            os.unlink(tmp)


if __name__ == "__main__":
    unittest.main()
