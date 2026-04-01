"""Canonical color palette for CC terminal themes.

Single source of truth for all color data. Each theme variant defines
core terminal colors (background, foreground, cursor, selection) and
16 ANSI color slots mapped to Claude Code's semantic color roles.

Color values are stored as (R, G, B) integer tuples (0-255).
This module contains NO rendering or file-format logic.

Clean room implementation — color values observed from Claude Code's
terminal output; all code written from scratch.
"""

from __future__ import annotations

from dataclasses import dataclass

# Version of Claude Code these colors were extracted from.
CLAUDE_CODE_VERSION = "2.1.86"

# Type alias for RGB color tuples.
RGB = tuple[int, int, int]


def rgb_to_hex(color: RGB) -> str:
    """Convert an (R, G, B) tuple to a lowercase hex string like '#d77757'."""
    for component in color:
        if not (0 <= component <= 255):
            raise ValueError(f"RGB component {component} out of range 0-255")
    return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"


@dataclass(frozen=True)
class AnsiSlots:
    """The 16 ANSI color slots for a terminal profile.

    Slot assignments are aligned with Claude Code's ANSI theme mappings:
      - red: error / diffRemoved (NOT Claude orange)
      - bright_red: claude brand color (light) / error (dark)
      - green: success
      - blue: suggestion / permission
      - magenta: autoAccept / merged
      - cyan: planMode
      - yellow: warning
    """

    black: RGB
    red: RGB
    green: RGB
    yellow: RGB
    blue: RGB
    magenta: RGB
    cyan: RGB
    white: RGB
    bright_black: RGB
    bright_red: RGB
    bright_green: RGB
    bright_yellow: RGB
    bright_blue: RGB
    bright_magenta: RGB
    bright_cyan: RGB
    bright_white: RGB


@dataclass(frozen=True)
class ProfileMeta:
    """Terminal profile metadata (shared across all variants)."""

    font_name: str = "SFMono-Regular"
    font_size: float = 13.0
    columns: int = 120
    rows: int = 35
    cursor_style: str = "block"  # "block", "underline", or "bar"
    cursor_blink: bool = False
    unlimited_scrollback: bool = True


# Shared metadata — identical for all theme variants.
_META = ProfileMeta()


@dataclass(frozen=True)
class ThemePalette:
    """Complete terminal color theme.

    Combines core colors (background, foreground, cursor, selection),
    16 ANSI slots, and profile metadata into a single theme definition.
    """

    # Core terminal colors.
    background: RGB
    foreground: RGB
    cursor: RGB
    cursor_text: RGB
    selection: RGB
    # The 16 ANSI color slots.
    ansi: AnsiSlots
    # Profile metadata (font, window size, cursor style).
    meta: ProfileMeta


# ---------------------------------------------------------------------------
# Theme definitions
# ---------------------------------------------------------------------------

_LIGHT = ThemePalette(
    background=(255, 255, 255),
    foreground=(0, 0, 0),
    cursor=(215, 119, 87),        # Claude orange
    cursor_text=(255, 255, 255),
    selection=(180, 213, 255),     # selectionBg
    ansi=AnsiSlots(
        # Normal colors
        black=(0, 0, 0),              # text
        red=(171, 43, 63),            # error — aligned with ansi:red
        green=(44, 122, 57),          # success
        yellow=(150, 108, 30),        # warning
        blue=(87, 105, 247),          # suggestion / permission
        magenta=(135, 0, 255),        # autoAccept / merged
        cyan=(0, 102, 102),           # planMode
        white=(175, 175, 175),        # subtle
        # Bright colors
        bright_black=(102, 102, 102), # inactive
        bright_red=(215, 119, 87),    # claude — aligned with ansi:redBright
        bright_green=(105, 219, 124), # diffAdded
        bright_yellow=(200, 158, 80), # warningShimmer
        bright_blue=(117, 135, 255),  # claudeBlueShimmer
        bright_magenta=(255, 0, 135), # bashBorder
        bright_cyan=(8, 145, 178),    # cyan subagent
        bright_white=(255, 255, 255), # inverseText
    ),
    meta=_META,
)

_DARK = ThemePalette(
    background=(26, 26, 26),
    foreground=(255, 255, 255),
    cursor=(215, 119, 87),        # Claude orange
    cursor_text=(0, 0, 0),
    selection=(38, 79, 120),       # selectionBg
    ansi=AnsiSlots(
        # Normal colors
        black=(0, 0, 0),              # inverseText
        red=(215, 119, 87),           # claude — dark-ansi maps diffRemoved here
        green=(78, 186, 101),         # success
        yellow=(255, 193, 7),         # warning
        blue=(177, 185, 249),         # suggestion / permission
        magenta=(175, 135, 255),      # autoAccept / merged
        cyan=(72, 150, 140),          # planMode
        white=(153, 153, 153),        # inactive
        # Bright colors
        bright_black=(80, 80, 80),    # subtle
        bright_red=(255, 107, 128),   # error — dark-ansi maps error+claude here
        bright_green=(56, 166, 96),   # diffAddedWord
        bright_yellow=(255, 223, 57), # warningShimmer
        bright_blue=(207, 215, 255),  # permissionShimmer
        bright_magenta=(253, 93, 177),# bashBorder
        bright_cyan=(8, 145, 178),    # cyan subagent
        bright_white=(193, 193, 193), # inactiveShimmer
    ),
    meta=_META,
)

_LIGHT_DALTONIZED = ThemePalette(
    background=(255, 255, 255),
    foreground=(0, 0, 0),
    cursor=(255, 153, 51),         # Adjusted orange for deuteranopia
    cursor_text=(255, 255, 255),
    selection=(180, 213, 255),
    ansi=AnsiSlots(
        # Normal colors
        black=(0, 0, 0),
        red=(204, 0, 0),              # Pure red (error)
        green=(0, 102, 153),          # Blue instead of green (success)
        yellow=(255, 153, 0),         # Adjusted warning
        blue=(51, 102, 255),          # Bright blue (suggestion)
        magenta=(135, 0, 255),        # autoAccept
        cyan=(51, 102, 102),          # planMode (blue-gray)
        white=(175, 175, 175),        # subtle
        # Bright colors
        bright_black=(102, 102, 102), # inactive
        bright_red=(255, 153, 51),    # Adjusted claude orange
        bright_green=(153, 204, 255), # Light blue instead of green (diffAdded)
        bright_yellow=(255, 183, 50), # warningShimmer
        bright_blue=(101, 152, 255),  # Lighter blue
        bright_magenta=(0, 102, 204), # Blue instead of pink (bashBorder)
        bright_cyan=(0, 178, 178),    # Adjusted cyan
        bright_white=(255, 255, 255), # inverseText
    ),
    meta=_META,
)

_DARK_DALTONIZED = ThemePalette(
    background=(26, 26, 26),
    foreground=(255, 255, 255),
    cursor=(255, 153, 51),         # Adjusted orange for deuteranopia
    cursor_text=(0, 0, 0),
    selection=(38, 79, 120),
    ansi=AnsiSlots(
        # Normal colors
        black=(0, 0, 0),
        red=(255, 153, 51),           # Adjusted claude orange
        green=(51, 153, 255),         # Blue instead of green (success)
        yellow=(255, 204, 0),         # Adjusted warning
        blue=(153, 204, 255),         # Light blue (suggestion)
        magenta=(175, 135, 255),      # autoAccept
        cyan=(72, 150, 140),          # planMode
        white=(153, 153, 153),        # inactive
        # Bright colors
        bright_black=(80, 80, 80),    # subtle
        bright_red=(204, 0, 0),       # Pure red (error)
        bright_green=(0, 119, 179),   # Medium blue (diffAddedWord)
        bright_yellow=(255, 230, 50), # warningShimmer
        bright_blue=(180, 215, 255),  # Lighter blue
        bright_magenta=(51, 153, 255),# Blue instead of pink (bashBorder)
        bright_cyan=(0, 178, 178),    # Adjusted cyan
        bright_white=(193, 193, 193), # inactiveShimmer
    ),
    meta=_META,
)

# Public registry of all theme variants.
THEMES: dict[str, ThemePalette] = {
    "light": _LIGHT,
    "dark": _DARK,
    "light_daltonized": _LIGHT_DALTONIZED,
    "dark_daltonized": _DARK_DALTONIZED,
}
