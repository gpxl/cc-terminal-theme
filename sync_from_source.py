#!/usr/bin/env python3
"""Extract color values from Claude Code's theme.ts for palette updates.

Parses rgb(r,g,b) literals from the TypeScript theme definitions and
outputs them as Python-friendly data for updating palette.py.

Usage:
    python3 sync_from_source.py ~/projects/claude-code/utils/theme.ts

This is a maintenance tool, not a build dependency.
"""

from __future__ import annotations

import re
import sys

# Pattern to match rgb(r,g,b) with optional spaces.
_RGB_PATTERN = re.compile(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)")

# Pattern to match a theme key assignment: key: 'rgb(...)' or key: 'ansi:...'
_KEY_VALUE_PATTERN = re.compile(
    r"^\s*(\w+):\s*['\"]rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)['\"]"
)


def extract_rgb_values(line: str) -> list[tuple[int, int, int]]:
    """Extract all rgb(r,g,b) tuples from a line of text.

    Returns a list of (r, g, b) integer tuples.
    """
    return [(int(m[0]), int(m[1]), int(m[2])) for m in _RGB_PATTERN.findall(line)]


def parse_theme_block(block: str) -> dict[str, tuple[int, int, int]]:
    """Parse a theme definition block and extract named color assignments.

    Only extracts lines with rgb() values — skips ansi: references.

    Returns a dict mapping color names to (r, g, b) tuples.
    """
    result: dict[str, tuple[int, int, int]] = {}
    for line in block.splitlines():
        match = _KEY_VALUE_PATTERN.match(line)
        if match:
            name = match.group(1)
            r, g, b = int(match.group(2)), int(match.group(3)), int(match.group(4))
            result[name] = (r, g, b)
    return result


def find_theme_blocks(content: str) -> dict[str, str]:
    """Find named theme definition blocks in theme.ts content.

    Looks for patterns like `const lightTheme: Theme = {` and extracts
    the block until the closing `}`.

    Returns a dict mapping theme names to their block content.
    """
    # Match const <name>Theme: Theme = { ... }
    pattern = re.compile(
        r"const\s+(\w+Theme)\s*:\s*Theme\s*=\s*\{",
        re.MULTILINE,
    )

    blocks: dict[str, str] = {}

    for match in pattern.finditer(content):
        name = match.group(1)
        start = match.end()
        depth = 1
        pos = start

        while pos < len(content) and depth > 0:
            if content[pos] == "{":
                depth += 1
            elif content[pos] == "}":
                depth -= 1
            pos += 1

        blocks[name] = content[start : pos - 1]

    return blocks


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 sync_from_source.py <path/to/theme.ts>")
        sys.exit(1)

    theme_path = sys.argv[1]

    try:
        content = open(theme_path).read()
    except FileNotFoundError:
        print(f"Error: {theme_path} not found")
        sys.exit(1)

    blocks = find_theme_blocks(content)

    if not blocks:
        print("No theme blocks found in file.")
        sys.exit(1)

    for theme_name, block in sorted(blocks.items()):
        colors = parse_theme_block(block)
        if not colors:
            continue

        print(f"\n# {theme_name}")
        print(f"# {len(colors)} RGB colors found\n")

        for color_name, (r, g, b) in sorted(colors.items()):
            print(f'    "{color_name}": ({r}, {g}, {b}),')


if __name__ == "__main__":
    main()
