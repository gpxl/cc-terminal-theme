#!/usr/bin/env python3
"""Generate Claude terminal theme files for all supported emitters.

Reads the canonical palette from palette.py and generates theme files
for Terminal.app, iTerm2, Ghostty, Alacritty, Kitty, and Windows Terminal.

Usage:
    python3 generate.py

Output:
    themes/<emitter>/<variant> files for each supported terminal.
"""

from pathlib import Path

from emitters import alacritty, ghostty, iterm2, kitty, terminal_app, windows_terminal
from palette import CLAUDE_CODE_VERSION, THEMES

# Base output directory.
THEMES_DIR = Path(__file__).parent / "themes"

# Emitter registry: (module, subdirectory name).
EMITTERS = [
    (terminal_app, "terminal-app"),
    (iterm2, "iterm2"),
    (ghostty, "ghostty"),
    (alacritty, "alacritty"),
    (kitty, "kitty"),
    (windows_terminal, "windows-terminal"),
]


def main() -> None:
    print(f"Claude Terminal Theme (colors from Claude Code v{CLAUDE_CODE_VERSION})")
    print()

    total = 0
    for emitter_module, subdir in EMITTERS:
        output_dir = THEMES_DIR / subdir
        print(f"  {subdir}/")
        for variant, palette in THEMES.items():
            path = emitter_module.emit(variant, palette, output_dir)
            print(f"    {path.name}")
            total += 1

    print()
    print(f"Generated {total} theme files in {THEMES_DIR}/")


if __name__ == "__main__":
    main()
