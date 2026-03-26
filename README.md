# Claude Terminal Theme

A macOS Terminal.app theme inspired by the Claude desktop app's warm, cream-tinted aesthetic.

## Install

1. Download [`Claude.terminal`](./Claude.terminal)
2. Double-click to open — it imports automatically into Terminal.app
3. Go to **Terminal > Settings > Profiles** and set "Claude" as your default

Or import manually: **Terminal > Settings > Profiles > ⚙️ > Import**

## Color Palette

| Element | Hex | Preview |
|---------|-----|---------|
| Background | `#ffffff` | ![#ffffff](https://placehold.co/24/ffffff/ffffff) |
| Text | `#3b3b3b` | ![#3b3b3b](https://placehold.co/24/3b3b3b/3b3b3b) |
| Bold | `#2c2c2c` | ![#2c2c2c](https://placehold.co/24/2c2c2c/2c2c2c) |
| Cursor | `#c4725a` | ![#c4725a](https://placehold.co/24/c4725a/c4725a) |
| Selection | `#f0ddd7` | ![#f0ddd7](https://placehold.co/24/f0ddd7/f0ddd7) |

### ANSI Colors

| Color | Normal | Bright |
|-------|--------|--------|
| Black | `#3b3b3b` | `#6b6b65` |
| Red | `#c4725a` | `#d4836b` |
| Green | `#6b8f71` | `#7faa85` |
| Yellow | `#c9a96e` | `#d9bc82` |
| Blue | `#6b7f99` | `#8299b3` |
| Magenta | `#9b7291` | `#b38aaa` |
| Cyan | `#6b9b9b` | `#85b3b3` |
| White | `#eae9e4` | `#f5f4f0` |

## Font

SF Mono Regular 13pt (ships with macOS).

## Customizing

Edit the hex values in `generate.py` and re-run:

```bash
python3 generate.py
```

## License

MIT
