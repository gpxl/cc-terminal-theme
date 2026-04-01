"""Tests for the generate.py orchestrator."""

import tempfile
from pathlib import Path
from unittest.mock import patch

from generate import EMITTERS, THEMES_DIR, main


class TestEmitterRegistry:
    def test_has_six_emitters(self):
        assert len(EMITTERS) == 6

    def test_each_emitter_has_emit_function(self):
        for module, subdir in EMITTERS:
            assert hasattr(module, "emit"), f"{subdir} module missing emit()"
            assert callable(module.emit)

    def test_themes_dir_is_relative_to_script(self):
        assert THEMES_DIR.name == "themes"


class TestMain:
    def test_generates_all_theme_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir) / "themes"
            with patch("generate.THEMES_DIR", tmp_path):
                main()

            # 6 emitters x 4 variants = 24 files
            all_files = list(tmp_path.rglob("*"))
            theme_files = [f for f in all_files if f.is_file()]
            assert len(theme_files) == 24

    def test_creates_subdirectories(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir) / "themes"
            with patch("generate.THEMES_DIR", tmp_path):
                main()

            subdirs = sorted(d.name for d in tmp_path.iterdir() if d.is_dir())
            assert subdirs == [
                "alacritty", "ghostty", "iterm2",
                "kitty", "terminal-app", "windows-terminal",
            ]
