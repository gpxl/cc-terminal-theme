"""Tests for the palette sync-from-source extraction tool."""

import tempfile
from pathlib import Path
from unittest.mock import patch

from sync_from_source import extract_rgb_values, find_theme_blocks, main, parse_theme_block


class TestExtractRgbValues:
    def test_extracts_rgb_from_line(self):
        line = "  claude: 'rgb(215,119,87)', // Claude orange"
        results = extract_rgb_values(line)
        assert (215, 119, 87) in results

    def test_extracts_multiple_rgb_from_line(self):
        line = "  a: 'rgb(1,2,3)', b: 'rgb(4,5,6)'"
        results = extract_rgb_values(line)
        assert len(results) == 2
        assert (1, 2, 3) in results
        assert (4, 5, 6) in results

    def test_returns_empty_for_no_rgb(self):
        line = "  claude: 'ansi:red',"
        results = extract_rgb_values(line)
        assert results == []

    def test_handles_spaces_in_rgb(self):
        line = "  bg: 'rgb(240, 240, 240)',"
        results = extract_rgb_values(line)
        assert (240, 240, 240) in results


class TestParseThemeBlock:
    def test_extracts_named_colors(self):
        block = """
  claude: 'rgb(215,119,87)', // Claude orange
  success: 'rgb(44,122,57)', // Green
  error: 'rgb(171,43,63)', // Red
"""
        result = parse_theme_block(block)
        assert result["claude"] == (215, 119, 87)
        assert result["success"] == (44, 122, 57)
        assert result["error"] == (171, 43, 63)

    def test_skips_ansi_colors(self):
        block = """
  claude: 'ansi:redBright',
  success: 'rgb(44,122,57)',
"""
        result = parse_theme_block(block)
        assert "claude" not in result
        assert "success" in result

    def test_handles_empty_block(self):
        result = parse_theme_block("")
        assert result == {}

    def test_handles_spaces_in_rgb_values(self):
        block = "  bg: 'rgb(240, 240, 240)',"
        result = parse_theme_block(block)
        assert result["bg"] == (240, 240, 240)


class TestFindThemeBlocks:
    def test_finds_single_theme(self):
        content = """
const lightTheme: Theme = {
  claude: 'rgb(215,119,87)',
  success: 'rgb(44,122,57)',
}
"""
        blocks = find_theme_blocks(content)
        assert "lightTheme" in blocks
        assert "rgb(215,119,87)" in blocks["lightTheme"]

    def test_finds_multiple_themes(self):
        content = """
const lightTheme: Theme = {
  claude: 'rgb(215,119,87)',
}

const darkTheme: Theme = {
  claude: 'rgb(215,119,87)',
}
"""
        blocks = find_theme_blocks(content)
        assert len(blocks) == 2
        assert "lightTheme" in blocks
        assert "darkTheme" in blocks

    def test_handles_nested_braces(self):
        content = """
const lightTheme: Theme = {
  claude: 'rgb(215,119,87)',
  nested: { inner: 'value' },
  success: 'rgb(44,122,57)',
}
"""
        blocks = find_theme_blocks(content)
        assert "lightTheme" in blocks
        assert "rgb(44,122,57)" in blocks["lightTheme"]

    def test_returns_empty_for_no_themes(self):
        content = "const x = 42;"
        blocks = find_theme_blocks(content)
        assert blocks == {}

    def test_skips_non_theme_consts(self):
        content = """
const someOtherConst = { a: 1 };
const lightTheme: Theme = {
  claude: 'rgb(215,119,87)',
}
"""
        blocks = find_theme_blocks(content)
        assert len(blocks) == 1
        assert "lightTheme" in blocks


class TestMain:
    def test_no_args_prints_usage(self, capsys):
        import sys

        with patch.object(sys, "argv", ["sync_from_source.py"]):
            try:
                main()
            except SystemExit as e:
                assert e.code == 1

        captured = capsys.readouterr()
        assert "Usage:" in captured.out

    def test_missing_file_prints_error(self, capsys):
        import sys

        with patch.object(sys, "argv", ["sync_from_source.py", "/no/such/theme.ts"]):
            try:
                main()
            except SystemExit as e:
                assert e.code == 1

        captured = capsys.readouterr()
        assert "not found" in captured.out

    def test_valid_file_prints_colors(self, capsys):
        import sys

        content = """
const lightTheme: Theme = {
  claude: 'rgb(215,119,87)',
  success: 'rgb(44,122,57)',
}
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ts", delete=False) as f:
            f.write(content)
            f.flush()

            with patch.object(sys, "argv", ["sync_from_source.py", f.name]):
                main()

        captured = capsys.readouterr()
        assert "lightTheme" in captured.out
        assert "(215, 119, 87)" in captured.out
        Path(f.name).unlink()

    def test_file_with_no_themes_exits(self, capsys):
        import sys

        with tempfile.NamedTemporaryFile(mode="w", suffix=".ts", delete=False) as f:
            f.write("const x = 42;")
            f.flush()

            with patch.object(sys, "argv", ["sync_from_source.py", f.name]):
                try:
                    main()
                except SystemExit as e:
                    assert e.code == 1

        captured = capsys.readouterr()
        assert "No theme blocks" in captured.out
        Path(f.name).unlink()
