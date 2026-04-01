"""Tests for Ghostty, Alacritty, Kitty, and Windows Terminal emitters."""

import json
import tempfile
from pathlib import Path

import pytest

from emitters.ghostty import emit as ghostty_emit
from emitters.alacritty import emit as alacritty_emit
from emitters.kitty import emit as kitty_emit
from emitters.windows_terminal import emit as wt_emit
from palette import THEMES


@pytest.fixture
def output_dir():
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


class TestGhostty:
    def test_generates_file(self, output_dir):
        path = ghostty_emit("light", THEMES["light"], output_dir)
        assert path.exists()
        assert path.name == "claude-light"

    def test_dark_filename(self, output_dir):
        path = ghostty_emit("dark", THEMES["dark"], output_dir)
        assert path.name == "claude-dark"

    def test_daltonized_filename(self, output_dir):
        path = ghostty_emit("light_daltonized", THEMES["light_daltonized"], output_dir)
        assert path.name == "claude-light-daltonized"

    def test_contains_background(self, output_dir):
        path = ghostty_emit("light", THEMES["light"], output_dir)
        content = path.read_text()
        assert "background = ffffff" in content

    def test_contains_foreground(self, output_dir):
        path = ghostty_emit("light", THEMES["light"], output_dir)
        content = path.read_text()
        assert "foreground = 000000" in content

    def test_contains_palette_lines(self, output_dir):
        path = ghostty_emit("light", THEMES["light"], output_dir)
        content = path.read_text()
        # Should have palette = N=hex for all 16 ANSI colors
        for i in range(16):
            assert f"palette = {i}=#" in content

    def test_contains_cursor(self, output_dir):
        path = ghostty_emit("light", THEMES["light"], output_dir)
        content = path.read_text()
        assert "cursor-color = d77757" in content

    def test_all_variants_generate(self, output_dir):
        for name, palette in THEMES.items():
            path = ghostty_emit(name, palette, output_dir)
            assert path.exists()


class TestAlacritty:
    def test_generates_file(self, output_dir):
        path = alacritty_emit("light", THEMES["light"], output_dir)
        assert path.exists()
        assert path.suffix == ".toml"

    def test_filename(self, output_dir):
        path = alacritty_emit("dark", THEMES["dark"], output_dir)
        assert path.name == "claude-dark.toml"

    def test_contains_primary_section(self, output_dir):
        path = alacritty_emit("light", THEMES["light"], output_dir)
        content = path.read_text()
        assert "[colors.primary]" in content
        assert 'background = "#ffffff"' in content

    def test_contains_normal_section(self, output_dir):
        path = alacritty_emit("light", THEMES["light"], output_dir)
        content = path.read_text()
        assert "[colors.normal]" in content

    def test_contains_bright_section(self, output_dir):
        path = alacritty_emit("light", THEMES["light"], output_dir)
        content = path.read_text()
        assert "[colors.bright]" in content

    def test_all_variants_generate(self, output_dir):
        for name, palette in THEMES.items():
            path = alacritty_emit(name, palette, output_dir)
            assert path.exists()


class TestKitty:
    def test_generates_file(self, output_dir):
        path = kitty_emit("light", THEMES["light"], output_dir)
        assert path.exists()
        assert path.suffix == ".conf"

    def test_filename(self, output_dir):
        path = kitty_emit("dark", THEMES["dark"], output_dir)
        assert path.name == "claude-dark.conf"

    def test_contains_background(self, output_dir):
        path = kitty_emit("light", THEMES["light"], output_dir)
        content = path.read_text()
        assert "background #ffffff" in content

    def test_contains_all_color_slots(self, output_dir):
        path = kitty_emit("light", THEMES["light"], output_dir)
        content = path.read_text()
        for i in range(16):
            assert f"color{i} #" in content

    def test_contains_cursor(self, output_dir):
        path = kitty_emit("light", THEMES["light"], output_dir)
        content = path.read_text()
        assert "cursor #d77757" in content

    def test_all_variants_generate(self, output_dir):
        for name, palette in THEMES.items():
            path = kitty_emit(name, palette, output_dir)
            assert path.exists()


class TestWindowsTerminal:
    def test_generates_file(self, output_dir):
        path = wt_emit("light", THEMES["light"], output_dir)
        assert path.exists()
        assert path.suffix == ".json"

    def test_filename(self, output_dir):
        path = wt_emit("dark", THEMES["dark"], output_dir)
        assert path.name == "claude-dark.json"

    def test_output_is_valid_json(self, output_dir):
        path = wt_emit("light", THEMES["light"], output_dir)
        data = json.loads(path.read_text())
        assert isinstance(data, dict)

    def test_has_name(self, output_dir):
        path = wt_emit("light", THEMES["light"], output_dir)
        data = json.loads(path.read_text())
        assert data["name"] == "Claude Light"

    def test_has_background(self, output_dir):
        path = wt_emit("light", THEMES["light"], output_dir)
        data = json.loads(path.read_text())
        assert data["background"] == "#FFFFFF"

    def test_has_all_color_keys(self, output_dir):
        path = wt_emit("light", THEMES["light"], output_dir)
        data = json.loads(path.read_text())
        required = [
            "black", "red", "green", "yellow", "blue", "purple", "cyan", "white",
            "brightBlack", "brightRed", "brightGreen", "brightYellow",
            "brightBlue", "brightPurple", "brightCyan", "brightWhite",
        ]
        for key in required:
            assert key in data, f"Missing key: {key}"

    def test_colors_are_uppercase_hex(self, output_dir):
        """Windows Terminal convention uses uppercase hex."""
        path = wt_emit("light", THEMES["light"], output_dir)
        data = json.loads(path.read_text())
        assert data["background"] == data["background"].upper()

    def test_all_variants_generate(self, output_dir):
        for name, palette in THEMES.items():
            path = wt_emit(name, palette, output_dir)
            assert path.exists()
