"""iTerm2 theme emitter.

Generates .itermcolors files (XML plist format). These can be imported
via iTerm2 > Settings > Profiles > Colors > Color Presets > Import.
"""

from __future__ import annotations

import plistlib
from pathlib import Path

from palette import RGB, ThemePalette

_DISPLAY_NAMES: dict[str, str] = {
    "light": "Claude Light",
    "dark": "Claude Dark",
    "light_daltonized": "Claude Light (Daltonized)",
    "dark_daltonized": "Claude Dark (Daltonized)",
}


def _color_dict(color: RGB) -> dict:
    """Build an iTerm2 color dictionary from an RGB tuple."""
    return {
        "Red Component": color[0] / 255.0,
        "Green Component": color[1] / 255.0,
        "Blue Component": color[2] / 255.0,
        "Alpha Component": 1.0,
        "Color Space": "sRGB",
    }


def emit(variant: str, palette: ThemePalette, output_dir: Path) -> Path:
    """Generate an iTerm2 .itermcolors file for the given theme variant.

    Args:
        variant: Theme variant key (e.g. "light", "dark_daltonized").
        palette: The ThemePalette to render.
        output_dir: Directory to write the .itermcolors file into.

    Returns:
        Path to the generated file.
    """
    display_name = _DISPLAY_NAMES.get(variant, f"Claude {variant.replace('_', ' ').title()}")

    # ANSI color slots: iTerm2 uses "Ansi N Color" keys (0-15).
    ansi_order = [
        palette.ansi.black,          # 0
        palette.ansi.red,            # 1
        palette.ansi.green,          # 2
        palette.ansi.yellow,         # 3
        palette.ansi.blue,           # 4
        palette.ansi.magenta,        # 5
        palette.ansi.cyan,           # 6
        palette.ansi.white,          # 7
        palette.ansi.bright_black,   # 8
        palette.ansi.bright_red,     # 9
        palette.ansi.bright_green,   # 10
        palette.ansi.bright_yellow,  # 11
        palette.ansi.bright_blue,    # 12
        palette.ansi.bright_magenta, # 13
        palette.ansi.bright_cyan,    # 14
        palette.ansi.bright_white,   # 15
    ]

    data: dict = {}

    # ANSI slots.
    for i, color in enumerate(ansi_order):
        data[f"Ansi {i} Color"] = _color_dict(color)

    # Core colors.
    data["Background Color"] = _color_dict(palette.background)
    data["Foreground Color"] = _color_dict(palette.foreground)
    data["Cursor Color"] = _color_dict(palette.cursor)
    data["Cursor Text Color"] = _color_dict(palette.cursor_text)
    data["Selection Color"] = _color_dict(palette.selection)
    data["Selected Text Color"] = _color_dict(palette.foreground)
    data["Bold Color"] = _color_dict(palette.foreground)

    # Write the profile.
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{display_name}.itermcolors"
    with open(output_path, "wb") as f:
        plistlib.dump(data, f, fmt=plistlib.FMT_XML)

    return output_path
