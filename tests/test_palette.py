"""Tests for the canonical color palette module."""

import pytest

from palette import (
    CLAUDE_CODE_VERSION,
    THEMES,
    AnsiSlots,
    ProfileMeta,
    ThemePalette,
    rgb_to_hex,
)


class TestRgbToHex:
    def test_black(self):
        assert rgb_to_hex((0, 0, 0)) == "#000000"

    def test_white(self):
        assert rgb_to_hex((255, 255, 255)) == "#ffffff"

    def test_claude_orange(self):
        assert rgb_to_hex((215, 119, 87)) == "#d77757"

    def test_mixed_case_lowercase(self):
        result = rgb_to_hex((171, 43, 63))
        assert result == result.lower()

    def test_rejects_out_of_range(self):
        with pytest.raises(ValueError, match="0-255"):
            rgb_to_hex((256, 0, 0))

    def test_rejects_negative(self):
        with pytest.raises(ValueError, match="0-255"):
            rgb_to_hex((-1, 0, 0))


class TestThemePalette:
    def test_has_all_required_fields(self):
        palette = THEMES["light"]
        assert isinstance(palette, ThemePalette)
        assert isinstance(palette.ansi, AnsiSlots)
        assert isinstance(palette.meta, ProfileMeta)

    def test_ansi_slots_are_rgb_tuples(self):
        for name, palette in THEMES.items():
            for field_name in AnsiSlots.__dataclass_fields__:
                value = getattr(palette.ansi, field_name)
                assert isinstance(value, tuple), f"{name}.ansi.{field_name} is not a tuple"
                assert len(value) == 3, f"{name}.ansi.{field_name} length != 3"
                for component in value:
                    assert 0 <= component <= 255, (
                        f"{name}.ansi.{field_name} component {component} out of range"
                    )

    def test_core_colors_are_rgb_tuples(self):
        for name, palette in THEMES.items():
            for field in ("background", "foreground", "cursor", "cursor_text", "selection"):
                value = getattr(palette, field)
                assert isinstance(value, tuple), f"{name}.{field} is not a tuple"
                assert len(value) == 3, f"{name}.{field} length != 3"


class TestThemeVariants:
    def test_all_four_variants_exist(self):
        assert set(THEMES.keys()) == {"light", "dark", "light_daltonized", "dark_daltonized"}

    def test_light_has_white_background(self):
        assert THEMES["light"].background == (255, 255, 255)

    def test_dark_has_dark_background(self):
        r, g, b = THEMES["dark"].background
        assert r < 50 and g < 50 and b < 50

    def test_light_has_dark_foreground(self):
        assert THEMES["light"].foreground == (0, 0, 0)

    def test_dark_has_light_foreground(self):
        assert THEMES["dark"].foreground == (255, 255, 255)

    def test_cursor_is_claude_orange_in_standard_themes(self):
        """Both standard themes use Claude orange for the cursor."""
        assert THEMES["light"].cursor == (215, 119, 87)
        assert THEMES["dark"].cursor == (215, 119, 87)

    def test_daltonized_uses_adjusted_orange(self):
        """Daltonized themes use an adjusted orange for better visibility."""
        light_d = THEMES["light_daltonized"]
        dark_d = THEMES["dark_daltonized"]
        # Daltonized orange is different from standard
        assert light_d.cursor != THEMES["light"].cursor
        assert dark_d.cursor != THEMES["dark"].cursor


class TestAnsiSlotAlignment:
    """Verify ANSI slots align with Claude Code's ansi theme expectations.

    In Claude Code's light-ansi theme:
      error -> ansi:red, claude -> ansi:redBright
    In Claude Code's dark-ansi theme:
      error+claude -> ansi:redBright (shared), diffRemoved -> ansi:red
    """

    def test_light_red_is_error_color(self):
        """Light ANSI red slot should be the error color, not Claude orange."""
        red = THEMES["light"].ansi.red
        # Should be a red-ish color (high R, low G, low B), not orange
        r, g, b = red
        assert r > 150, "Red slot should have high red component"
        assert g < 100, "Red slot should have low green component (not orange)"

    def test_light_bright_red_is_claude_orange(self):
        """Light ANSI bright red slot should be Claude orange."""
        bright_red = THEMES["light"].ansi.bright_red
        assert bright_red == (215, 119, 87)

    def test_dark_bright_red_is_error_color(self):
        """Dark ANSI bright red should serve the error role."""
        bright_red = THEMES["dark"].ansi.bright_red
        r, g, b = bright_red
        # Should be a bright red/pink (error color for dark bg)
        assert r > 200, "Dark bright red should have high red component"

    def test_green_slots_are_success_colors(self):
        """Green ANSI slots should map to success colors."""
        for name in ("light", "dark"):
            green = THEMES[name].ansi.green
            r, g, b = green
            assert g > r and g > b, f"{name} green slot should be predominantly green"

    def test_blue_slots_are_suggestion_colors(self):
        """Blue ANSI slots should map to suggestion/permission colors."""
        for name in ("light", "dark"):
            blue = THEMES[name].ansi.blue
            r, g, b = blue
            assert b > r, f"{name} blue slot should have higher blue than red"

    def test_cyan_slots_are_plan_mode_colors(self):
        """Cyan ANSI slots should map to planMode colors."""
        for name in ("light", "dark"):
            cyan = THEMES[name].ansi.cyan
            r, g, b = cyan
            assert g > r or b > r, f"{name} cyan should be teal-ish"

    def test_magenta_slots_are_auto_accept_colors(self):
        """Magenta ANSI slots should map to autoAccept/merged colors."""
        for name in ("light", "dark"):
            magenta = THEMES[name].ansi.magenta
            r, g, b = magenta
            assert r > g or b > g, f"{name} magenta should be violet-ish"


class TestProfileMeta:
    def test_font_name(self):
        assert THEMES["light"].meta.font_name == "SFMono-Regular"

    def test_font_size(self):
        assert THEMES["light"].meta.font_size == 13.0

    def test_columns_and_rows(self):
        meta = THEMES["light"].meta
        assert meta.columns == 120
        assert meta.rows == 35

    def test_cursor_style_is_block(self):
        assert THEMES["light"].meta.cursor_style == "block"

    def test_all_themes_share_meta(self):
        """All theme variants should use the same profile metadata."""
        reference = THEMES["light"].meta
        for name, palette in THEMES.items():
            assert palette.meta == reference, f"{name} meta differs from light"


class TestVersionTracking:
    def test_version_is_set(self):
        assert isinstance(CLAUDE_CODE_VERSION, str)
        assert len(CLAUDE_CODE_VERSION) > 0

    def test_version_looks_like_semver(self):
        parts = CLAUDE_CODE_VERSION.split(".")
        assert len(parts) >= 2, "Version should have at least major.minor"
        for part in parts:
            assert part.isdigit(), f"Version part '{part}' is not numeric"
