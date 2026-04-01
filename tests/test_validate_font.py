"""Tests for the font glyph validation script."""

import tempfile
from pathlib import Path
from unittest.mock import patch

from validate_font import CLAUDE_GLYPHS, check_glyphs_in_font, main


class TestClaudeGlyphs:
    def test_glyph_registry_not_empty(self):
        assert len(CLAUDE_GLYPHS) > 0

    def test_each_entry_has_required_fields(self):
        for glyph in CLAUDE_GLYPHS:
            assert "char" in glyph
            assert "codepoint" in glyph
            assert "name" in glyph
            assert isinstance(glyph["codepoint"], int)

    def test_contains_black_circle(self):
        codepoints = {g["codepoint"] for g in CLAUDE_GLYPHS}
        assert 0x23FA in codepoints  # ⏺

    def test_contains_lightning_bolt(self):
        codepoints = {g["codepoint"] for g in CLAUDE_GLYPHS}
        assert 0x21AF in codepoints  # ↯

    def test_contains_blockquote_bar(self):
        codepoints = {g["codepoint"] for g in CLAUDE_GLYPHS}
        assert 0x258E in codepoints  # ▎

    def test_all_codepoints_are_valid_unicode(self):
        for glyph in CLAUDE_GLYPHS:
            cp = glyph["codepoint"]
            assert 0 < cp < 0x10FFFF, f"Invalid codepoint: {cp:#06x}"
            assert glyph["char"] == chr(cp), f"Char doesn't match codepoint for {glyph['name']}"


class TestCheckGlyphs:
    def test_returns_dict(self):
        result = check_glyphs_in_font("/nonexistent/font.ttf")
        assert isinstance(result, dict)

    def test_missing_font_reports_error(self):
        result = check_glyphs_in_font("/nonexistent/font.ttf")
        assert result.get("error") is not None

    def test_result_structure_on_error(self):
        result = check_glyphs_in_font("/nonexistent/font.ttf")
        assert "font_path" in result
        assert "error" in result

    def test_fonttools_not_installed_error(self):
        """When fonttools is not importable, report a helpful error."""
        import builtins
        real_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "fontTools.ttLib":
                raise ImportError("No module named 'fontTools'")
            return real_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            result = check_glyphs_in_font("/some/font.ttf")
        assert "fonttools not installed" in result["error"]

    def test_real_font_returns_coverage_data(self):
        """If fonttools is available and we have a system font, test the full path."""
        try:
            from fontTools.ttLib import TTFont  # noqa: F401
        except ImportError:
            # fonttools not available — test the structure only
            return

        # Try to find a system font on macOS
        sf_mono = Path("/System/Library/Fonts/SFMono-Regular.otf")
        if not sf_mono.exists():
            # Try the font collection
            sf_mono = Path(
                "/System/Library/Fonts/Supplemental/SF-Mono-Regular.otf"
            )
        if not sf_mono.exists():
            # Fall back to any available system font
            font_dirs = [
                Path("/System/Library/Fonts"),
                Path("/usr/share/fonts"),
            ]
            for font_dir in font_dirs:
                if font_dir.exists():
                    for f in font_dir.glob("*.ttf"):
                        sf_mono = f
                        break
                    if sf_mono.exists():
                        break

        if not sf_mono.exists():
            return  # No fonts found, skip

        result = check_glyphs_in_font(str(sf_mono))
        assert "error" not in result
        assert "supported" in result
        assert "missing" in result
        assert "total" in result
        assert result["total"] == len(CLAUDE_GLYPHS)
        assert result["supported_count"] + result["missing_count"] == result["total"]
        assert 0 <= result["coverage_pct"] <= 100

    def test_no_cmap_table_error(self):
        """Test handling of a font with no cmap table."""
        try:
            from fontTools.ttLib import TTFont
        except ImportError:
            return

        # Create a minimal TTFont with no cmap and save it
        with tempfile.NamedTemporaryFile(suffix=".ttf", delete=False) as f:
            font = TTFont()
            font.setGlyphOrder([".notdef"])
            # Add minimal required tables
            from fontTools.fontBuilder import FontBuilder

            fb = FontBuilder(1000, isTTF=True)
            fb.setupGlyphOrder([".notdef"])
            fb.setupCharacterMap({})
            fb.setupGlyf({".notdef": {"numberOfContours": 0}})
            fb.setupHorizontalMetrics({".notdef": (500, 0)})
            fb.setupHorizontalHeader()
            fb.setupHead(unitsPerEm=1000)
            fb.setupOs2()
            fb.setupPost()
            fb.setupNameTable({"familyName": "Test", "styleName": "Regular"})
            fb.font.save(f.name)
            font_path = f.name

        result = check_glyphs_in_font(font_path)
        # Should succeed but report all glyphs as missing
        assert "error" not in result
        assert result["missing_count"] == result["total"]
        Path(font_path).unlink()


class TestMain:
    def test_no_args_prints_usage(self, capsys):
        """With no args, should print usage and glyph list."""
        import sys

        with patch.object(sys, "argv", ["validate_font.py"]):
            try:
                main()
            except SystemExit as e:
                assert e.code == 1

        captured = capsys.readouterr()
        assert "Usage:" in captured.out
        assert "U+23FA" in captured.out  # Should list the glyphs

    def test_missing_font_arg_prints_error(self, capsys):
        """With a nonexistent font, should print error."""
        import sys

        with patch.object(sys, "argv", ["validate_font.py", "/no/such/font.ttf"]):
            try:
                main()
            except SystemExit as e:
                assert e.code == 1

        captured = capsys.readouterr()
        assert "Error:" in captured.out
