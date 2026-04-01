"""Tests for the macOS Terminal.app emitter."""

import plistlib
import tempfile
from pathlib import Path

import pytest

from emitters.terminal_app import emit, decode_nscolor, decode_nsfont
from palette import THEMES


@pytest.fixture
def output_dir():
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


class TestEmit:
    def test_generates_file(self, output_dir):
        path = emit("light", THEMES["light"], output_dir)
        assert path.exists()
        assert path.suffix == ".terminal"

    def test_filename_matches_theme(self, output_dir):
        path = emit("light", THEMES["light"], output_dir)
        assert path.name == "Claude Light.terminal"

    def test_dark_filename(self, output_dir):
        path = emit("dark", THEMES["dark"], output_dir)
        assert path.name == "Claude Dark.terminal"

    def test_daltonized_filename(self, output_dir):
        path = emit("light_daltonized", THEMES["light_daltonized"], output_dir)
        assert path.name == "Claude Light (Daltonized).terminal"

    def test_output_is_valid_plist(self, output_dir):
        path = emit("light", THEMES["light"], output_dir)
        with open(path, "rb") as f:
            data = plistlib.load(f)
        assert isinstance(data, dict)

    def test_profile_has_name(self, output_dir):
        path = emit("light", THEMES["light"], output_dir)
        with open(path, "rb") as f:
            data = plistlib.load(f)
        assert data["name"] == "Claude Light"

    def test_profile_has_color_keys(self, output_dir):
        path = emit("light", THEMES["light"], output_dir)
        with open(path, "rb") as f:
            data = plistlib.load(f)
        required_keys = [
            "BackgroundColor", "TextColor", "CursorColor",
            "ANSIBlackColor", "ANSIRedColor", "ANSIGreenColor",
            "ANSIYellowColor", "ANSIBlueColor", "ANSIMagentaColor",
            "ANSICyanColor", "ANSIWhiteColor",
            "ANSIBrightBlackColor", "ANSIBrightRedColor",
        ]
        for key in required_keys:
            assert key in data, f"Missing key: {key}"

    def test_profile_has_font(self, output_dir):
        path = emit("light", THEMES["light"], output_dir)
        with open(path, "rb") as f:
            data = plistlib.load(f)
        assert "Font" in data
        assert isinstance(data["Font"], bytes)

    def test_profile_has_window_settings(self, output_dir):
        path = emit("light", THEMES["light"], output_dir)
        with open(path, "rb") as f:
            data = plistlib.load(f)
        assert data["columnCount"] == 120
        assert data["rowCount"] == 35

    def test_cursor_not_blinking(self, output_dir):
        path = emit("light", THEMES["light"], output_dir)
        with open(path, "rb") as f:
            data = plistlib.load(f)
        assert data["CursorBlink"] is False

    def test_all_variants_generate(self, output_dir):
        for name, palette in THEMES.items():
            path = emit(name, palette, output_dir)
            assert path.exists()


class TestDecodeNscolor:
    """Verify that encoded NSColor data can be decoded back."""

    def test_roundtrip_black(self):
        r, g, b = decode_nscolor((0, 0, 0))
        assert abs(r) < 0.01 and abs(g) < 0.01 and abs(b) < 0.01

    def test_roundtrip_white(self):
        r, g, b = decode_nscolor((255, 255, 255))
        assert abs(r - 1.0) < 0.01 and abs(g - 1.0) < 0.01 and abs(b - 1.0) < 0.01

    def test_roundtrip_claude_orange(self):
        r, g, b = decode_nscolor((215, 119, 87))
        assert abs(r - 215 / 255) < 0.01
        assert abs(g - 119 / 255) < 0.01
        assert abs(b - 87 / 255) < 0.01


class TestDecodeNsfont:
    def test_roundtrip_sf_mono(self):
        name, size = decode_nsfont("SFMono-Regular", 13.0)
        assert name == "SFMono-Regular"
        assert abs(size - 13.0) < 0.01
