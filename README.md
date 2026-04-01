# Claude Terminal Theme

Terminal color schemes derived from Claude Code's visual identity. Supports 6 terminal emulators with light, dark, and color-blind accessible (daltonized) variants.

## Supported Terminals

| Terminal | Format | Variants |
|----------|--------|----------|
| [Terminal.app](#terminalapp) | `.terminal` | Light, Dark, Daltonized |
| [iTerm2](#iterm2) | `.itermcolors` | Light, Dark, Daltonized |
| [Ghostty](#ghostty) | config | Light, Dark, Daltonized |
| [Alacritty](#alacritty) | `.toml` | Light, Dark, Daltonized |
| [Kitty](#kitty) | `.conf` | Light, Dark, Daltonized |
| [Windows Terminal](#windows-terminal) | `.json` | Light, Dark, Daltonized |

## Quick Install

### Terminal.app

Double-click any `.terminal` file in `themes/terminal-app/` to import, then set as default in **Terminal > Settings > Profiles**.

### iTerm2

Go to **iTerm2 > Settings > Profiles > Colors > Color Presets > Import** and select a `.itermcolors` file from `themes/iterm2/`.

### Ghostty

Copy a theme file from `themes/ghostty/` to `~/.config/ghostty/themes/`, then set in your config:

```
theme = claude-dark
```

### Alacritty

Add to `~/.config/alacritty/alacritty.toml`:

```toml
[general]
import = ["~/.config/alacritty/claude-dark.toml"]
```

### Kitty

Add to `~/.config/kitty/kitty.conf`:

```
include claude-dark.conf
```

### Windows Terminal

Copy the JSON object from a file in `themes/windows-terminal/` into the `"schemes"` array in your Windows Terminal `settings.json`, then select the scheme in your profile.

## Color Palette

### Light

| Element | Hex | Role |
|---------|-----|------|
| Background | `#ffffff` | White |
| Foreground | `#000000` | Black |
| Cursor | `#d77757` | Claude orange |
| Selection | `#b4d5ff` | Light blue |

#### ANSI Colors (Light)

| Slot | Normal | Bright | Normal Role | Bright Role |
|------|--------|--------|-------------|-------------|
| Black | `#000000` | `#666666` | text | inactive |
| Red | `#ab2b3f` | `#d77757` | error | claude |
| Green | `#2c7a39` | `#69db7c` | success | diffAdded |
| Yellow | `#966c1e` | `#c89e50` | warning | warningShimmer |
| Blue | `#5769f7` | `#7587ff` | suggestion | blueShimmer |
| Magenta | `#8700ff` | `#ff0087` | autoAccept | bashBorder |
| Cyan | `#006666` | `#0891b2` | planMode | subagent |
| White | `#afafaf` | `#ffffff` | subtle | inverseText |

### Dark

| Element | Hex | Role |
|---------|-----|------|
| Background | `#1a1a1a` | Near-black |
| Foreground | `#ffffff` | White |
| Cursor | `#d77757` | Claude orange |
| Selection | `#264f78` | Dark blue |

#### ANSI Colors (Dark)

| Slot | Normal | Bright | Normal Role | Bright Role |
|------|--------|--------|-------------|-------------|
| Black | `#000000` | `#505050` | inverseText | subtle |
| Red | `#d77757` | `#ff6b80` | claude | error |
| Green | `#4eba65` | `#38a660` | success | diffAddedWord |
| Yellow | `#ffc107` | `#ffdf39` | warning | warningShimmer |
| Blue | `#b1b9f9` | `#cfd7ff` | suggestion | permissionShimmer |
| Magenta | `#af87ff` | `#fd5db1` | autoAccept | bashBorder |
| Cyan | `#48968c` | `#0891b2` | planMode | subagent |
| White | `#999999` | `#c1c1c1` | inactive | inactiveShimmer |

## ANSI Slot Philosophy

The red ANSI slot contains the **error** color (not Claude orange), because Claude Code's built-in ANSI theme maps `error` to `ansi:red`. Claude's brand orange is in **bright red**, matching `claude: 'ansi:redBright'`. This ensures errors look like errors in both Claude Code and other CLI programs (ls, git, etc.).

## Daltonized Variants

The daltonized themes adjust colors for deuteranopia (red-green color blindness):

- **Success** uses blue instead of green
- **Diffs** use blue/red instead of green/red
- **Claude orange** is shifted to `#ff9933` for better contrast
- **Bash border** uses blue instead of pink

## Font

All Terminal.app profiles use **SF Mono Regular 13pt** (ships with macOS). For other terminals, set your preferred monospace font.

### Glyph Compatibility

Claude Code uses these Unicode glyphs in its UI:

```
⏺ ✻ ↯ ◐ ◉ ▎ ━ ◇ ◆ ※ ⚑ ▶ ⏸ ↻ ⑂
```

Recommended fonts with full glyph support: **SF Mono**, **JetBrains Mono**, **Fira Code**, **Cascadia Code**.

## Shell Integration

Help Claude Code's theme auto-detection by setting `COLORFGBG` in your shell profile:

```bash
# For light themes
export COLORFGBG="0;15"

# For dark themes
export COLORFGBG="15;0"
```

## Tab Status Colors

Claude Code colors your terminal tab to indicate state (via OSC 21337):

| State | Color | Meaning |
|-------|-------|---------|
| Idle | Green (`#00d75f`) | Ready for input |
| Busy | Orange (`#ff9500`) | Processing |
| Waiting | Blue (`#5f87ff`) | Awaiting approval |

These are hardcoded in Claude Code and not affected by the terminal theme.

## Regenerating

Edit `palette.py` to change colors, then:

```bash
python3 generate.py
```

This regenerates all 24 theme files across all terminals.

## Project Structure

```
palette.py               # Canonical color data (single source of truth)
generate.py              # Orchestrator — calls all emitters
emitters/
  terminal_app.py        # macOS Terminal.app
  iterm2.py              # iTerm2
  ghostty.py             # Ghostty
  alacritty.py           # Alacritty
  kitty.py               # Kitty
  windows_terminal.py    # Windows Terminal
themes/                  # Generated output (24 files)
tests/                   # pytest test suite
```

## License

MIT
