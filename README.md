# 🐾 Catscii

Turn any image into ASCII art from the command line — with a playful cat theme. One dependency: [Pillow](https://pypi.org/project/Pillow/).

```
   /\_/\
  ( o.o )   Catscii
   > ^ <    turn any image into ASCII art
```

## Example

**Input**

![Sample input](examples/input-sample.jpg)

**Output** (`--style blocks`)

```
████████████████████████████████████████████████████████████
█████████████████▓▒██████████████████████▓▒█████████████████
████████████████▒░░░▓██████████████████▓▒░░▒▓███████████████
██████████████▓░░░░░░░▓███████████████▒░░░░░░▓██████████████
██████████████▒░░░░░░░▒▓▒▒▒▒░░░░▒▒▒▒▓▒░░░░░░░░▓█████████████
████████████▓░▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒░▒████████████
████████████▒░░░░░░░▒▓██▓▒░░░░░░░░░▒▓██▓▒░░░░░░░████████████
████████████▒░░░░░░░▒▓▓▓▒░░░░░░░░░░▒▓▓▓▒░░░░░░░▒████████████
███████████████▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓██████████████
```

Try it yourself in the browser: **[live demo](https://hackercat-git.github.io/Catscii/)** (runs entirely client-side — nothing is uploaded).

## Installation

```bash
git clone https://github.com/Hackercat-git/Catscii.git
cd Catscii
pip install pillow
```

## Usage

```bash
python catscii.py photo.jpg
python catscii.py photo.jpg --width 160 --style blocks
python catscii.py photo.jpg --style paws --color
python catscii.py photo.jpg -o art.txt
python catscii.py photo.jpg -o art.html --color
python catscii.py --banner
```

| Flag | Description | Default |
|---|---|---|
| `--width` | Output width in characters | `100` |
| `--style` | `standard`, `blocks`, `paws`, or `binary` | `standard` |
| `--color` | Render using the image's original colors (ANSI in terminal, inline styles in HTML) | off |
| `-o`, `--output` | Save to a `.txt` or `.html` file instead of printing | — |
| `--banner` | Show the Catscii banner | — |

## Styles

- **standard** — the classic `@%#*+=-:. ` density ramp
- **blocks** — Unicode block shades (`█▓▒░`) for a sharper look
- **paws** — a playful cat-themed ramp using paw and whisker-like characters
- **binary** — `01` only, for a "matrix" effect

## Tests

```bash
python -m unittest discover tests
```

## License

MIT
