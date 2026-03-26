#!/usr/bin/env python3
"""Generate a Claude Desktop-inspired Terminal.app theme file.

The Claude desktop app uses a warm, cream-tinted aesthetic with terracotta
accents. This script generates a .terminal profile that captures that palette.

Usage:
    python3 generate.py

Output:
    Claude.terminal — double-click to install on any Mac
"""

import plistlib


def hex_to_rgb(hex_color: str) -> tuple[float, float, float]:
    """Convert hex color string to RGB floats (0.0–1.0)."""
    h = hex_color.lstrip("#")
    return (
        int(h[0:2], 16) / 255.0,
        int(h[2:4], 16) / 255.0,
        int(h[4:6], 16) / 255.0,
    )


def encode_nscolor(hex_color: str) -> bytes:
    """Encode a hex color as NSKeyedArchived NSColor data (calibrated RGB)."""
    r, g, b = hex_to_rgb(hex_color)
    color_data = f"{r:.10f} {g:.10f} {b:.10f}".encode("ascii")

    archive = {
        "$archiver": "NSKeyedArchiver",
        "$version": 100000,
        "$top": {"root": plistlib.UID(1)},
        "$objects": [
            "$null",
            {
                "$class": plistlib.UID(2),
                "NSRGB": color_data,
                "NSColorSpace": 1,
            },
            {
                "$classes": ["NSColor", "NSObject"],
                "$classname": "NSColor",
            },
        ],
    }

    return plistlib.dumps(archive, fmt=plistlib.FMT_BINARY)


def encode_nsfont(name: str, size: float) -> bytes:
    """Encode a font as NSKeyedArchived NSFont data."""
    archive = {
        "$archiver": "NSKeyedArchiver",
        "$version": 100000,
        "$top": {"root": plistlib.UID(1)},
        "$objects": [
            "$null",
            {
                "$class": plistlib.UID(3),
                "NSName": plistlib.UID(2),
                "NSSize": size,
                "NSfFlags": 16,
            },
            name,
            {
                "$classes": ["NSFont", "NSObject"],
                "$classname": "NSFont",
            },
        ],
    }

    return plistlib.dumps(archive, fmt=plistlib.FMT_BINARY)


# ---------------------------------------------------------------------------
# Claude Desktop color palette
# ---------------------------------------------------------------------------

PALETTE = {
    # Core colors
    "BackgroundColor": "#ffffff",       # Main content area — pure white
    "TextColor": "#3b3b3b",            # Input text — warm charcoal
    "BoldTextColor": "#2c2c2c",        # Emphasis — near-black
    "CursorColor": "#c4725a",          # Claude terracotta
    "CursorTextColor": "#ffffff",      # Text under cursor
    "SelectionColor": "#f0ddd7",       # Warm orange-tinted selection

    # ANSI normal (muted, warm-shifted)
    "ANSIBlackColor": "#3b3b3b",       # Warm charcoal
    "ANSIRedColor": "#c4725a",         # Claude terracotta
    "ANSIGreenColor": "#6b8f71",       # Warm muted green
    "ANSIYellowColor": "#c9a96e",      # Warm amber
    "ANSIBlueColor": "#6b7f99",        # Muted warm blue
    "ANSIMagentaColor": "#9b7291",     # Warm mauve
    "ANSICyanColor": "#6b9b9b",        # Warm teal
    "ANSIWhiteColor": "#eae9e4",       # Chrome beige

    # ANSI bright (lighter, slightly more saturated)
    "ANSIBrightBlackColor": "#6b6b65", # Sidebar icon grey
    "ANSIBrightRedColor": "#d4836b",   # Lighter terracotta
    "ANSIBrightGreenColor": "#7faa85", # Lighter warm green
    "ANSIBrightYellowColor": "#d9bc82",# Lighter amber
    "ANSIBrightBlueColor": "#8299b3",  # Lighter warm blue
    "ANSIBrightMagentaColor": "#b38aaa",# Lighter mauve
    "ANSIBrightCyanColor": "#85b3b3",  # Lighter warm teal
    "ANSIBrightWhiteColor": "#f5f4f0", # Lightest warm white
}


def main() -> None:
    profile: dict = {
        "name": "Claude",
        "type": "Window Settings",
        "ProfileCurrentVersion": 2.07,

        # Window
        "columnCount": 120,
        "rowCount": 35,

        # Scrollback
        "ShouldLimitScrollback": 0,

        # Cursor
        "CursorBlink": False,
        "CursorType": 0,  # 0=block, 1=underline, 2=bar

        # Text rendering
        "UseBoldFonts": True,
        "UseBrightBold": True,
        "DisableAnsiColor": False,

        # Title bar
        "ShowRepresentedURLInTitle": True,
        "ShowRepresentedURLPathInTitle": True,
        "ShowActiveProcessInTitle": True,
        "ShowShellCommandInTitle": False,
        "ShowDimensionsInTitle": False,
        "ShowCommandKeyInTitle": False,
        "ShowWindowSettingsNameInTitle": False,

        # Bell
        "VisualBellOnlyWhenMuted": True,
        "VisualBell": True,
        "BellIsEnabled": False,

        # Background
        "BackgroundAlphaInactive": 1.0,
        "BackgroundBlur": 0.0,
    }

    # Encode and add all colors
    for key, hex_color in PALETTE.items():
        profile[key] = encode_nscolor(hex_color)

    # Font — SF Mono ships with macOS, guaranteed available
    profile["Font"] = encode_nsfont("SFMono-Regular", 13.0)

    # Write the .terminal file (XML plist — human-readable)
    output = "Claude.terminal"
    with open(output, "wb") as f:
        plistlib.dump(profile, f, fmt=plistlib.FMT_XML)

    print(f"Generated {output}")
    print("Double-click to install, or import via Terminal > Settings > Profiles")


if __name__ == "__main__":
    main()
