#!/usr/bin/env python3
"""Generate Claude Code Terminal.app theme files (light + dark).

Colors extracted from the Claude Code CLI source (v2.1.86).
Maps the actual Claude Code semantic colors to ANSI terminal slots.

Usage:
    python3 generate.py

Output:
    Claude Light.terminal — light variant
    Claude Dark.terminal  — dark variant
    Double-click to install, or import via Terminal > Settings > Profiles
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
# Claude Code themes — extracted from claude-code v2.1.86 source
# ---------------------------------------------------------------------------

LIGHT_PALETTE = {
    # Core colors
    "BackgroundColor": "#ffffff",       # Main content area
    "TextColor": "#000000",            # text: rgb(0,0,0)
    "BoldTextColor": "#000000",        # Same as text
    "CursorColor": "#D77757",          # claude: rgb(215,119,87)
    "CursorTextColor": "#ffffff",      # inverseText: rgb(255,255,255)
    "SelectionColor": "#B4D5FF",       # selectionBg: rgb(180,213,255)

    # ANSI normal
    "ANSIBlackColor": "#000000",       # text
    "ANSIRedColor": "#D77757",         # claude: rgb(215,119,87)
    "ANSIGreenColor": "#2C7A39",       # success: rgb(44,122,57)
    "ANSIYellowColor": "#966C1E",      # warning: rgb(150,108,30)
    "ANSIBlueColor": "#5769F7",        # suggestion/permission: rgb(87,105,247)
    "ANSIMagentaColor": "#8700FF",     # autoAccept/merged: rgb(135,0,255)
    "ANSICyanColor": "#006666",        # planMode: rgb(0,102,102)
    "ANSIWhiteColor": "#AFAFAF",       # subtle: rgb(175,175,175)

    # ANSI bright (shimmer variants + brighter functional colors)
    "ANSIBrightBlackColor": "#666666", # inactive: rgb(102,102,102)
    "ANSIBrightRedColor": "#F59575",   # claudeShimmer: rgb(245,149,117)
    "ANSIBrightGreenColor": "#69DB7C", # diffAdded: rgb(105,219,124)
    "ANSIBrightYellowColor": "#C89E50",# warningShimmer: rgb(200,158,80)
    "ANSIBrightBlueColor": "#7587FF",  # claudeBlueShimmer: rgb(117,135,255)
    "ANSIBrightMagentaColor": "#FF0087",# bashBorder: rgb(255,0,135)
    "ANSIBrightCyanColor": "#0891B2",  # cyan subagent: rgb(8,145,178)
    "ANSIBrightWhiteColor": "#FFFFFF", # inverseText: rgb(255,255,255)
}

DARK_PALETTE = {
    # Core colors
    "BackgroundColor": "#1a1a1a",       # Dark background
    "TextColor": "#FFFFFF",            # text: rgb(255,255,255)
    "BoldTextColor": "#FFFFFF",        # Same as text
    "CursorColor": "#D77757",          # claude: rgb(215,119,87)
    "CursorTextColor": "#000000",      # inverseText: rgb(0,0,0)
    "SelectionColor": "#264F78",       # selectionBg: rgb(38,79,120)

    # ANSI normal
    "ANSIBlackColor": "#000000",       # inverseText
    "ANSIRedColor": "#D77757",         # claude: rgb(215,119,87)
    "ANSIGreenColor": "#4EBA65",       # success: rgb(78,186,101)
    "ANSIYellowColor": "#FFC107",      # warning: rgb(255,193,7)
    "ANSIBlueColor": "#B1B9F9",        # suggestion/permission: rgb(177,185,249)
    "ANSIMagentaColor": "#AF87FF",     # autoAccept/merged: rgb(175,135,255)
    "ANSICyanColor": "#48968C",        # planMode: rgb(72,150,140)
    "ANSIWhiteColor": "#999999",       # inactive: rgb(153,153,153)

    # ANSI bright (shimmer variants + brighter functional colors)
    "ANSIBrightBlackColor": "#505050", # subtle: rgb(80,80,80)
    "ANSIBrightRedColor": "#EB9F7F",   # claudeShimmer: rgb(235,159,127)
    "ANSIBrightGreenColor": "#38A660", # diffAddedWord: rgb(56,166,96)
    "ANSIBrightYellowColor": "#FFDF39",# warningShimmer: rgb(255,223,57)
    "ANSIBrightBlueColor": "#CFD7FF",  # permissionShimmer: rgb(207,215,255)
    "ANSIBrightMagentaColor": "#FD5DB1",# bashBorder: rgb(253,93,177)
    "ANSIBrightCyanColor": "#0891B2",  # cyan subagent: rgb(8,145,178)
    "ANSIBrightWhiteColor": "#C1C1C1", # inactiveShimmer: rgb(193,193,193)
}


def build_profile(name: str, palette: dict) -> dict:
    """Build a Terminal.app profile dict from a name and color palette."""
    profile: dict = {
        "name": name,
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

    for key, hex_color in palette.items():
        profile[key] = encode_nscolor(hex_color)

    return profile


def write_profile(profile: dict, output: str) -> None:
    """Write a profile dict to an XML plist .terminal file."""
    with open(output, "wb") as f:
        plistlib.dump(profile, f, fmt=plistlib.FMT_XML)
    print(f"  {output}")


def main() -> None:
    print("Generated:")
    write_profile(build_profile("Claude Light", LIGHT_PALETTE), "Claude Light.terminal")
    write_profile(build_profile("Claude Dark", DARK_PALETTE), "Claude Dark.terminal")
    print("Double-click to install, or import via Terminal > Settings > Profiles")


if __name__ == "__main__":
    main()
