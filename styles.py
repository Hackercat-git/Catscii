"""Character ramps used to map pixel brightness to characters.
Each ramp goes from darkest (index 0) to lightest (last index).
"""

STYLES = {
    # Classic dense-to-sparse ASCII ramp.
    "standard": "@%#*+=-:. ",
    # Unicode block shades: crisp, high-contrast result.
    "blocks": "█▓▒░ ",
    # Playful cat-themed ramp: paws and whisker-like characters.
    "paws": "WM@#&8*o+=-:,. ",  # cat-themed ramp, terminal-safe (no emoji)
    # Binary / "matrix" look.
    "binary": "10 ",
    # Smooth shade ramp using box-drawing and shade characters.
    "shade": "■▪▫◾◽□  ",
}

DEFAULT_STYLE = "standard"


def get_ramp(style_name):
    try:
        return STYLES[style_name]
    except KeyError:
        valid = ", ".join(sorted(STYLES))
        raise ValueError(f"Unknown style '{style_name}'. Valid styles: {valid}")
