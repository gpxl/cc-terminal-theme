"""Windows Terminal theme emitter.

Generates JSON color scheme fragments. Add the JSON object to the
"schemes" array in Windows Terminal's settings.json.
"""

from __future__ import annotations

import json
from pathlib import Path

from palette import RGB, ThemePalette


def _hex_upper(color: RGB) -> str:
    """Return uppercase hex string (Windows Terminal convention)."""
    return f"#{color[0]:02X}{color[1]:02X}{color[2]:02X}"


_DISPLAY_NAMES: dict[str, str] = {
    "light": "Claude Light",
    "dark": "Claude Dark",
    "light_daltonized": "Claude Light (Daltonized)",
    "dark_daltonized": "Claude Dark (Daltonized)",
}


def emit(variant: str, palette: ThemePalette, output_dir: Path) -> Path:
    """Generate a Windows Terminal JSON color scheme for the given variant."""
    display_name = _DISPLAY_NAMES.get(variant, f"Claude {variant.replace('_', ' ').title()}")
    filename = f"claude-{variant.replace('_', '-')}.json"

    scheme = {
        "name": display_name,
        "background": _hex_upper(palette.background),
        "foreground": _hex_upper(palette.foreground),
        "cursorColor": _hex_upper(palette.cursor),
        "selectionBackground": _hex_upper(palette.selection),
        # ANSI normal
        "black": _hex_upper(palette.ansi.black),
        "red": _hex_upper(palette.ansi.red),
        "green": _hex_upper(palette.ansi.green),
        "yellow": _hex_upper(palette.ansi.yellow),
        "blue": _hex_upper(palette.ansi.blue),
        "purple": _hex_upper(palette.ansi.magenta),
        "cyan": _hex_upper(palette.ansi.cyan),
        "white": _hex_upper(palette.ansi.white),
        # ANSI bright
        "brightBlack": _hex_upper(palette.ansi.bright_black),
        "brightRed": _hex_upper(palette.ansi.bright_red),
        "brightGreen": _hex_upper(palette.ansi.bright_green),
        "brightYellow": _hex_upper(palette.ansi.bright_yellow),
        "brightBlue": _hex_upper(palette.ansi.bright_blue),
        "brightPurple": _hex_upper(palette.ansi.bright_magenta),
        "brightCyan": _hex_upper(palette.ansi.bright_cyan),
        "brightWhite": _hex_upper(palette.ansi.bright_white),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename
    output_path.write_text(json.dumps(scheme, indent=2) + "\n")
    return output_path
