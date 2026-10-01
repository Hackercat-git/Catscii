# Changelog

All notable changes to Catscii are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- `--invert` flag — reverses the brightness ramp, useful for images with light backgrounds
- `--grayscale` flag — converts the image to grayscale before rendering
- `--height` flag — set a fixed output height in lines (default: auto from aspect ratio)
- `--resize` flag — choose between `smooth` (LANCZOS, default) and `pixel` (NEAREST, for pixel art)
- `shade` style — smooth block-shade ramp using box-drawing characters (`■▪▫◾◽□`)
- `CatsciiError` exception — `load_image` now raises a typed exception instead of calling `sys.exit()` directly, making it usable as a library
- `pyproject.toml` — project is now installable via `pip install .`; `catscii` becomes a proper CLI command; `pip install ".[fast]"` pulls in numpy
- Optional numpy backend — if numpy is available, pixel mapping and ANSI string building are fully vectorised (~10× faster on large images)
- CI matrix now tests Python 3.10, 3.11, and 3.12 in parallel
- Test suite expanded from 8 to 14 tests (invert, all styles, `to_html` plain text, `.txt`/`.html` output saving, `CatsciiError`)
- Live demo (`docs/index.html`) now includes the `shade` style, Invert and Grayscale checkboxes, and a `.txt` download button

### Changed
- `resize_image` now uses `Image.Resampling.LANCZOS` for sharper results
- `render_ascii` uses `get_flattened_data()` for bulk pixel access instead of per-pixel `getpixel()` calls
- `import re` moved to module level (was deferred inside `strip_ansi` and `to_html`)
- `to_html` now handles plain (no-color) ASCII art correctly — HTML-escapes characters even without ANSI codes
- `paws` style replaced emoji (`🐾`) with terminal-safe characters (`WM@#&8*o+=-:,.`) to fix alignment in all terminals
- Colored banner using ANSI cyan

## [0.1.0] — 2026-10-01

### Added
- Initial release: `catscii.py`, `banner.py`, `styles.py`
- Styles: `standard`, `blocks`, `paws`, `binary`
- Flags: `--width`, `--style`, `--color`, `--output`, `--banner`
- `to_html` output with ANSI → `<span>` conversion
- Basic test suite (8 tests)
- GitHub Actions CI on Python 3.12
- Live browser demo at `docs/index.html`
