"""Alacritty theme emitter.

Generates TOML config files. Import via [general] > import in
~/.config/alacritty/alacritty.toml.
"""

from __future__ import annotations

from pathlib import Path

from palette import RGB, ThemePalette, rgb_to_hex


def _quoted_hex(color: RGB) -> str:
    """Return quoted hex string for TOML: '"#d77757"'."""
    return f'"{rgb_to_hex(color)}"'


def emit(variant: str, palette: ThemePalette, output_dir: Path) -> Path:
    """Generate an Alacritty TOML theme file for the given variant."""
    filename = f"claude-{variant.replace('_', '-')}.toml"

    lines = [
        "[colors.primary]",
        f"background = {_quoted_hex(palette.background)}",
        f"foreground = {_quoted_hex(palette.foreground)}",
        "",
        "[colors.cursor]",
        f"cursor = {_quoted_hex(palette.cursor)}",
        f"text = {_quoted_hex(palette.cursor_text)}",
        "",
        "[colors.selection]",
        f"background = {_quoted_hex(palette.selection)}",
        f"text = {_quoted_hex(palette.foreground)}",
        "",
        "[colors.normal]",
        f"black = {_quoted_hex(palette.ansi.black)}",
        f"red = {_quoted_hex(palette.ansi.red)}",
        f"green = {_quoted_hex(palette.ansi.green)}",
        f"yellow = {_quoted_hex(palette.ansi.yellow)}",
        f"blue = {_quoted_hex(palette.ansi.blue)}",
        f"magenta = {_quoted_hex(palette.ansi.magenta)}",
        f"cyan = {_quoted_hex(palette.ansi.cyan)}",
        f"white = {_quoted_hex(palette.ansi.white)}",
        "",
        "[colors.bright]",
        f"black = {_quoted_hex(palette.ansi.bright_black)}",
        f"red = {_quoted_hex(palette.ansi.bright_red)}",
        f"green = {_quoted_hex(palette.ansi.bright_green)}",
        f"yellow = {_quoted_hex(palette.ansi.bright_yellow)}",
        f"blue = {_quoted_hex(palette.ansi.bright_blue)}",
        f"magenta = {_quoted_hex(palette.ansi.bright_magenta)}",
        f"cyan = {_quoted_hex(palette.ansi.bright_cyan)}",
        f"white = {_quoted_hex(palette.ansi.bright_white)}",
    ]

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename
    output_path.write_text("\n".join(lines) + "\n")
    return output_path
