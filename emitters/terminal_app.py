"""macOS Terminal.app theme emitter.

Generates .terminal profile files (XML plist with NSKeyedArchiver-encoded
colors and fonts). These can be imported via double-click or through
Terminal > Settings > Profiles.
"""

from __future__ import annotations

import plistlib
from pathlib import Path

from palette import RGB, ThemePalette

# Human-readable theme names for each variant.
_DISPLAY_NAMES: dict[str, str] = {
    "light": "Claude Light",
    "dark": "Claude Dark",
    "light_daltonized": "Claude Light (Daltonized)",
    "dark_daltonized": "Claude Dark (Daltonized)",
}


def _encode_nscolor(color: RGB) -> bytes:
    """Encode an RGB tuple as NSKeyedArchiver NSColor binary plist data."""
    r = color[0] / 255.0
    g = color[1] / 255.0
    b = color[2] / 255.0
    color_string = f"{r:.10f} {g:.10f} {b:.10f}".encode("ascii")

    archive = {
        "$archiver": "NSKeyedArchiver",
        "$version": 100000,
        "$top": {"root": plistlib.UID(1)},
        "$objects": [
            "$null",
            {
                "$class": plistlib.UID(2),
                "NSRGB": color_string,
                "NSColorSpace": 1,  # Calibrated RGB
            },
            {
                "$classes": ["NSColor", "NSObject"],
                "$classname": "NSColor",
            },
        ],
    }
    return plistlib.dumps(archive, fmt=plistlib.FMT_BINARY)


def _encode_nsfont(name: str, size: float) -> bytes:
    """Encode a font as NSKeyedArchiver NSFont binary plist data."""
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


def decode_nscolor(color: RGB) -> tuple[float, float, float]:
    """Encode then decode an NSColor to verify the roundtrip.

    Returns the (r, g, b) float values extracted from the archived data.
    """
    data = _encode_nscolor(color)
    archive = plistlib.loads(data)
    objects = archive["$objects"]
    color_obj = objects[1]
    parts = color_obj["NSRGB"].decode("ascii").split()
    return float(parts[0]), float(parts[1]), float(parts[2])


def decode_nsfont(name: str, size: float) -> tuple[str, float]:
    """Encode then decode an NSFont to verify the roundtrip.

    Returns the (name, size) extracted from the archived data.
    """
    data = _encode_nsfont(name, size)
    archive = plistlib.loads(data)
    objects = archive["$objects"]
    font_obj = objects[1]
    font_name = objects[font_obj["NSName"].data]
    return font_name, font_obj["NSSize"]


def emit(variant: str, palette: ThemePalette, output_dir: Path) -> Path:
    """Generate a Terminal.app .terminal file for the given theme variant.

    Args:
        variant: Theme variant key (e.g. "light", "dark_daltonized").
        palette: The ThemePalette to render.
        output_dir: Directory to write the .terminal file into.

    Returns:
        Path to the generated file.
    """
    display_name = _DISPLAY_NAMES.get(variant, f"Claude {variant.replace('_', ' ').title()}")
    meta = palette.meta

    # Map palette fields to Terminal.app plist color keys.
    color_map: dict[str, RGB] = {
        "BackgroundColor": palette.background,
        "TextColor": palette.foreground,
        "BoldTextColor": palette.foreground,
        "CursorColor": palette.cursor,
        "CursorTextColor": palette.cursor_text,
        "SelectionColor": palette.selection,
        # ANSI normal
        "ANSIBlackColor": palette.ansi.black,
        "ANSIRedColor": palette.ansi.red,
        "ANSIGreenColor": palette.ansi.green,
        "ANSIYellowColor": palette.ansi.yellow,
        "ANSIBlueColor": palette.ansi.blue,
        "ANSIMagentaColor": palette.ansi.magenta,
        "ANSICyanColor": palette.ansi.cyan,
        "ANSIWhiteColor": palette.ansi.white,
        # ANSI bright
        "ANSIBrightBlackColor": palette.ansi.bright_black,
        "ANSIBrightRedColor": palette.ansi.bright_red,
        "ANSIBrightGreenColor": palette.ansi.bright_green,
        "ANSIBrightYellowColor": palette.ansi.bright_yellow,
        "ANSIBrightBlueColor": palette.ansi.bright_blue,
        "ANSIBrightMagentaColor": palette.ansi.bright_magenta,
        "ANSIBrightCyanColor": palette.ansi.bright_cyan,
        "ANSIBrightWhiteColor": palette.ansi.bright_white,
    }

    # Cursor style: 0=block, 1=underline, 2=bar.
    cursor_type = {"block": 0, "underline": 1, "bar": 2}.get(meta.cursor_style, 0)

    profile: dict = {
        "name": display_name,
        "type": "Window Settings",
        "ProfileCurrentVersion": 2.07,
        # Window
        "columnCount": meta.columns,
        "rowCount": meta.rows,
        # Font
        "Font": _encode_nsfont(meta.font_name, meta.font_size),
        # Scrollback
        "ShouldLimitScrollback": 0 if meta.unlimited_scrollback else 1,
        # Cursor
        "CursorBlink": meta.cursor_blink,
        "CursorType": cursor_type,
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

    # Add encoded colors.
    for key, rgb in color_map.items():
        profile[key] = _encode_nscolor(rgb)

    # Write the profile.
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{display_name}.terminal"
    with open(output_path, "wb") as f:
        plistlib.dump(profile, f, fmt=plistlib.FMT_XML)

    return output_path
