#!/usr/bin/env python3
"""Validate that a font supports all Unicode glyphs used by Claude Code.

Inspects the font's cmap table to check for glyph coverage of the
specific Unicode characters that Claude Code renders in its TUI.

Usage:
    python3 validate_font.py /path/to/font.ttf
    python3 validate_font.py /path/to/font.otf

Requires: fonttools (pip install fonttools)
"""

from __future__ import annotations

import sys

# Claude Code UI glyphs — extracted from constants/figures.ts.
CLAUDE_GLYPHS = [
    {"char": "\u23FA", "codepoint": 0x23FA, "name": "Black Circle for Record (bullet)"},
    {"char": "\u25CF", "codepoint": 0x25CF, "name": "Black Circle (bullet, non-macOS)"},
    {"char": "\u2219", "codepoint": 0x2219, "name": "Bullet Operator"},
    {"char": "\u273B", "codepoint": 0x273B, "name": "Teardrop-Spoked Asterisk (spinner)"},
    {"char": "\u21AF", "codepoint": 0x21AF, "name": "Downwards Zigzag Arrow (fast mode)"},
    {"char": "\u25CB", "codepoint": 0x25CB, "name": "White Circle (effort low)"},
    {"char": "\u25D0", "codepoint": 0x25D0, "name": "Circle with Left Half Black (effort medium)"},
    {"char": "\u25C9", "codepoint": 0x25C9, "name": "Fisheye (effort max)"},
    {"char": "\u25B6", "codepoint": 0x25B6, "name": "Black Right-Pointing Triangle (play)"},
    {"char": "\u23F8", "codepoint": 0x23F8, "name": "Double Vertical Bar (pause)"},
    {"char": "\u21BB", "codepoint": 0x21BB, "name": "Clockwise Open Circle Arrow (refresh)"},
    {"char": "\u2190", "codepoint": 0x2190, "name": "Leftwards Arrow (channel)"},
    {"char": "\u2192", "codepoint": 0x2192, "name": "Rightwards Arrow (injected)"},
    {"char": "\u2442", "codepoint": 0x2442, "name": "OCR Fork (fork directive)"},
    {"char": "\u25C7", "codepoint": 0x25C7, "name": "White Diamond (running)"},
    {"char": "\u25C6", "codepoint": 0x25C6, "name": "Black Diamond (completed)"},
    {"char": "\u203B", "codepoint": 0x203B, "name": "Reference Mark (recap marker)"},
    {"char": "\u2691", "codepoint": 0x2691, "name": "Black Flag (issue indicator)"},
    {"char": "\u258E", "codepoint": 0x258E, "name": "Left One Quarter Block (blockquote)"},
    {"char": "\u2501", "codepoint": 0x2501, "name": "Box Drawings Heavy Horizontal (divider)"},
    {"char": "\u2191", "codepoint": 0x2191, "name": "Upwards Arrow"},
    {"char": "\u2193", "codepoint": 0x2193, "name": "Downwards Arrow (scroll hint)"},
]


def check_glyphs_in_font(font_path: str) -> dict:
    """Check which Claude Code glyphs a font supports.

    Args:
        font_path: Path to a .ttf or .otf font file.

    Returns:
        Dict with keys: font_path, supported, missing, total, coverage_pct.
        On error: dict with font_path and error keys.
    """
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        return {
            "font_path": font_path,
            "error": "fonttools not installed — run: pip install fonttools",
        }

    try:
        font = TTFont(font_path)
    except Exception as e:
        return {
            "font_path": font_path,
            "error": str(e),
        }

    # Build a set of all codepoints the font supports.
    cmap = font.getBestCmap()
    if cmap is None:
        return {
            "font_path": font_path,
            "error": "Font has no cmap table",
        }

    supported_codepoints = set(cmap.keys())
    font.close()

    supported = []
    missing = []

    for glyph in CLAUDE_GLYPHS:
        entry = {
            "char": glyph["char"],
            "codepoint": f"U+{glyph['codepoint']:04X}",
            "name": glyph["name"],
        }
        if glyph["codepoint"] in supported_codepoints:
            supported.append(entry)
        else:
            missing.append(entry)

    total = len(CLAUDE_GLYPHS)
    return {
        "font_path": font_path,
        "supported": supported,
        "missing": missing,
        "total": total,
        "supported_count": len(supported),
        "missing_count": len(missing),
        "coverage_pct": round(len(supported) / total * 100, 1) if total else 0,
    }


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 validate_font.py <font-path>")
        print()
        print("Claude Code uses these glyphs in its UI:")
        for g in CLAUDE_GLYPHS:
            print(f"  {g['char']}  U+{g['codepoint']:04X}  {g['name']}")
        sys.exit(1)

    result = check_glyphs_in_font(sys.argv[1])

    if "error" in result:
        print(f"Error: {result['error']}")
        sys.exit(1)

    print(f"Font: {result['font_path']}")
    print(f"Coverage: {result['supported_count']}/{result['total']} ({result['coverage_pct']}%)")
    print()

    if result["missing"]:
        print("Missing glyphs:")
        for g in result["missing"]:
            print(f"  {g['char']}  {g['codepoint']}  {g['name']}")
        print()
        print("Recommended fonts with full coverage: SF Mono, JetBrains Mono, Fira Code")
    else:
        print("All Claude Code glyphs are supported.")


if __name__ == "__main__":
    main()
