"""Ghostty theme emitter.

Generates Ghostty config theme files. Place in
~/.config/ghostty/themes/ or include via --config-file.
"""

from __future__ import annotations

from pathlib import Path

from palette import RGB, ThemePalette, rgb_to_hex


def _hex_bare(color: RGB) -> str:
    """Return hex without the '#' prefix (Ghostty convention)."""
    return rgb_to_hex(color).lstrip("#")


def emit(variant: str, palette: ThemePalette, output_dir: Path) -> Path:
    """Generate a Ghostty theme file for the given variant."""
    filename = f"claude-{variant.replace('_', '-')}"

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
        f"background = {_hex_bare(palette.background)}",
        f"foreground = {_hex_bare(palette.foreground)}",
        f"cursor-color = {_hex_bare(palette.cursor)}",
        f"cursor-text = {_hex_bare(palette.cursor_text)}",
        f"selection-background = {_hex_bare(palette.selection)}",
        f"selection-foreground = {_hex_bare(palette.foreground)}",
    ]

    for i, color in enumerate(ansi_colors):
        lines.append(f"palette = {i}=#{_hex_bare(color)}")

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename
    output_path.write_text("\n".join(lines) + "\n")
    return output_path
