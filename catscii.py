#!/usr/bin/env python3
"""Catscii - turn any image into ASCII art, with a playful cat theme.
Only dependency: Pillow (for reading image files).
"""
import argparse
import os
import re
import sys

from PIL import Image

from banner import print_banner
from styles import DEFAULT_STYLE, STYLES, get_ramp

# Characters are taller than they are wide, so we shrink the height
# to keep the final art looking proportional.
ASPECT_CORRECTION = 0.55


def load_image(path):
    if not os.path.isfile(path):
        sys.exit(f"File not found: {path}")
    try:
        return Image.open(path)
    except Exception as exc:
        sys.exit(f"Could not open image: {exc}")


def resize_image(image, width):
    original_w, original_h = image.size
    ratio = original_h / original_w
    height = max(1, round(width * ratio * ASPECT_CORRECTION))
    return image.resize((width, height), Image.Resampling.LANCZOS)


def pixel_to_char(brightness, ramp):
    """Map a 0-255 brightness value to a character in the ramp."""
    index = min(len(ramp) - 1, int(brightness / 256 * len(ramp)))
    return ramp[index]


def ansi_color(r, g, b):
    return f"\x1b[38;2;{r};{g};{b}m"


ANSI_RESET = "\x1b[0m"


def render_ascii(image, style, use_color, invert=False):
    ramp = get_ramp(style)
    if invert:
        ramp = ramp[::-1]

    grayscale = image.convert("L")
    width, height = image.size

    # Bulk pixel access is ~10x faster than calling getpixel() per pixel
    gray_pixels = list(grayscale.get_flattened_data())

    if use_color:
        rgb_pixels = list(image.convert("RGB").get_flattened_data())

    lines = []
    for y in range(height):
        row = []
        for x in range(width):
            idx = y * width + x
            brightness = gray_pixels[idx]
            char = pixel_to_char(brightness, ramp)
            if use_color:
                r, g, b = rgb_pixels[idx]
                row.append(f"{ansi_color(r, g, b)}{char}{ANSI_RESET}")
            else:
                row.append(char)
        lines.append("".join(row))
    return "\n".join(lines)


def strip_ansi(text):
    """Remove ANSI color codes, used when saving plain .txt output."""
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


def to_html(ascii_art, title="Catscii output"):
    """Wrap ASCII art into a standalone HTML page.

    Handles both colored output (ANSI -> <span> tags) and plain text.
    """
    has_ansi = "\x1b[" in ascii_art

    if has_ansi:
        pattern = re.compile(r"\x1b\[38;2;(\d+);(\d+);(\d+)m(.*?)\x1b\[0m", re.DOTALL)

        def repl(m):
            r, g, b, char = m.groups()
            char = (
                char.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
            )
            return f'<span style="color:rgb({r},{g},{b})">{char}</span>'

        body = pattern.sub(repl, ascii_art)
    else:
        body = (
            ascii_art.replace("&", "&amp;")
                     .replace("<", "&lt;")
                     .replace(">", "&gt;")
        )

    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<title>{title}</title>"
        "<style>body{background:#0d1117;margin:0;padding:16px;}"
        "pre{font-family:'Consolas','Courier New',monospace;font-size:8px;"
        "line-height:8px;color:#e6edf3;white-space:pre;}</style></head>"
        f"<body><pre>{body}</pre></body></html>"
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description="Turn an image into ASCII art.")
    parser.add_argument("image", nargs="?", help="Path to the input image (.png, .jpg, ...)")
    parser.add_argument("-o", "--output", help="Save output to a file (.txt or .html)")
    parser.add_argument(
        "--width", type=int, default=100,
        help="Output width in characters (default: 100)",
    )
    parser.add_argument(
        "--style",
        choices=sorted(STYLES),
        default=DEFAULT_STYLE,
        help=f"Character style (default: {DEFAULT_STYLE})",
    )
    parser.add_argument(
        "--color",
        action="store_true",
        help="Render in color using the image's original colors",
    )
    parser.add_argument(
        "--invert",
        action="store_true",
        help="Invert brightness mapping (useful for light backgrounds)",
    )
    parser.add_argument("--banner", action="store_true", help="Show the Catscii banner and exit")
    args = parser.parse_args(argv)

    if args.banner or not args.image:
        print_banner()
        if not args.image:
            parser.print_help()
        return

    image = load_image(args.image)
    resized = resize_image(image, args.width)
    art = render_ascii(resized, args.style, args.color, invert=args.invert)

    if args.output:
        ext = os.path.splitext(args.output)[1].lower()
        if ext == ".html":
            content = to_html(art)
        else:
            content = strip_ansi(art)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved to {args.output}")
    else:
        print(art)


if __name__ == "__main__":
    main()
