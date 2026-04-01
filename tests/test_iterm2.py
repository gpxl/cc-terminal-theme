"""Tests for the iTerm2 emitter."""

import plistlib
import tempfile
from pathlib import Path

import pytest

from emitters.iterm2 import emit
from palette import THEMES


@pytest.fixture
def output_dir():
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


class TestEmit:
    def test_generates_file(self, output_dir):
        path = emit("light", THEMES["light"], output_dir)
        assert path.exists()
        assert path.suffix == ".itermcolors"

    def test_filename_matches_theme(self, output_dir):
        path = emit("light", THEMES["light"], output_dir)
        assert path.name == "Claude Light.itermcolors"

    def test_dark_filename(self, output_dir):
        path = emit("dark", THEMES["dark"], output_dir)
        assert path.name == "Claude Dark.itermcolors"

    def test_daltonized_filename(self, output_dir):
        path = emit("dark_daltonized", THEMES["dark_daltonized"], output_dir)
        assert path.name == "Claude Dark (Daltonized).itermcolors"

    def test_output_is_valid_plist(self, output_dir):
        path = emit("light", THEMES["light"], output_dir)
        with open(path, "rb") as f:
            data = plistlib.load(f)
        assert isinstance(data, dict)

    def test_has_ansi_color_keys(self, output_dir):
        path = emit("light", THEMES["light"], output_dir)
        with open(path, "rb") as f:
            data = plistlib.load(f)
        for i in range(16):
            key = f"Ansi {i} Color"
            assert key in data, f"Missing key: {key}"

    def test_has_core_color_keys(self, output_dir):
        path = emit("light", THEMES["light"], output_dir)
        with open(path, "rb") as f:
            data = plistlib.load(f)
        for key in ("Background Color", "Foreground Color", "Cursor Color",
                     "Cursor Text Color", "Selection Color"):
            assert key in data, f"Missing key: {key}"

    def test_color_dict_has_components(self, output_dir):
        path = emit("light", THEMES["light"], output_dir)
        with open(path, "rb") as f:
            data = plistlib.load(f)
        color = data["Ansi 0 Color"]
        assert "Red Component" in color
        assert "Green Component" in color
        assert "Blue Component" in color
        assert "Color Space" in color
        assert color["Color Space"] == "sRGB"

    def test_component_values_are_floats(self, output_dir):
        path = emit("light", THEMES["light"], output_dir)
        with open(path, "rb") as f:
            data = plistlib.load(f)
        color = data["Background Color"]
        for key in ("Red Component", "Green Component", "Blue Component"):
            val = color[key]
            assert isinstance(val, float), f"{key} should be float, got {type(val)}"
            assert 0.0 <= val <= 1.0, f"{key} value {val} out of range"

    def test_light_background_is_white(self, output_dir):
        path = emit("light", THEMES["light"], output_dir)
        with open(path, "rb") as f:
            data = plistlib.load(f)
        bg = data["Background Color"]
        assert abs(bg["Red Component"] - 1.0) < 0.01
        assert abs(bg["Green Component"] - 1.0) < 0.01
        assert abs(bg["Blue Component"] - 1.0) < 0.01

    def test_all_variants_generate(self, output_dir):
        for name, palette in THEMES.items():
            path = emit(name, palette, output_dir)
            assert path.exists()
