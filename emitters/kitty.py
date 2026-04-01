"""Kitty theme emitter.

Generates .conf files. Include via `include` directive in
~/.config/kitty/kitty.conf.
"""

from __future__ import annotations

from pathlib import Path

from palette import ThemePalette, rgb_to_hex


def emit(variant: str, palette: ThemePalette, output_dir: Path) -> Path:
    """Generate a Kitty .conf theme file for the given variant."""
    filename = f"claude-{variant.replace('_', '-')}.conf"

    ansi_colors = [
        palette.ansi.black, palette.ansi.red, palette.ansi.green,
        palette.ansi.yellow, palette.ansi.blue, palette.ansi.magenta,
        palette.ansi.cyan, palette.ansi.white,
        palette.ansi.bright_black, palette.ansi.bright_red,
        palette.ansi.bright_green, palette.ansi.bright_yellow,
        palette.ansi.bright_blue, palette.ansi.bright_magenta,
        palette.ansi.bright_cyan, palette.ansi.bright_white,
    ]

    lines = [
        f"background {rgb_to_hex(palette.background)}",
        f"foreground {rgb_to_hex(palette.foreground)}",
        f"cursor {rgb_to_hex(palette.cursor)}",
        f"cursor_text_color {rgb_to_hex(palette.cursor_text)}",
        f"selection_background {rgb_to_hex(palette.selection)}",
        f"selection_foreground {rgb_to_hex(palette.foreground)}",
    ]

    for i, color in enumerate(ansi_colors):
        lines.append(f"color{i} {rgb_to_hex(color)}")

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename
    output_path.write_text("\n".join(lines) + "\n")
    return output_path
