#!/usr/bin/env python3

import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "format_totem_keymap.py"
SPEC = importlib.util.spec_from_file_location("format_totem_keymap", SCRIPT)
FORMATTER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(FORMATTER)


class FormatRowsTest(unittest.TestCase):
    def test_outer_key_uses_normal_indent_when_it_fits(self):
        cells = [f"&k{index}" for index in range(FORMATTER.EXPECTED_BINDINGS)]
        cells[20] = "&none"

        lines = FORMATTER.format_rows(cells).splitlines()
        second_key_column = FORMATTER.DEFAULT_ROW_INDENT

        self.assertEqual(lines[0].find("&"), second_key_column)
        self.assertEqual(lines[1].find("&"), second_key_column)
        self.assertEqual(lines[2].find("&"), FORMATTER.MIN_COL0_WIDTH - len(cells[20]))
        self.assertEqual(lines[2].find("&", lines[2].find("&") + 1), second_key_column)

    def test_long_outer_key_sets_top_row_start_and_split_alignment(self):
        cells = [f"&k{index}" for index in range(FORMATTER.EXPECTED_BINDINGS)]
        cells[20] = "&lt DEVICE ESC"

        lines = FORMATTER.format_rows(cells).splitlines()
        second_key_column = len(cells[20]) + FORMATTER.COLUMN_GAP

        self.assertEqual(lines[0].find("&"), second_key_column)
        self.assertEqual(lines[1].find("&"), second_key_column)
        self.assertTrue(lines[2].startswith(f"{cells[20]}  "))
        self.assertEqual(len({line.find("/**/") for line in lines}), 1)


class FormatKeymapIndentationTest(unittest.TestCase):
    def test_keymap_uses_two_space_indentation_without_shifting_grid(self):
        source = """/ {
    keymap {
        compatible = \"zmk,keymap\";

        base {
            label = \"BASE\";
            bindings = <
GRID ROW
            >;
        };
    };
};
"""
        expected = """/ {
  keymap {
    compatible = \"zmk,keymap\";

    base {
      label = \"BASE\";
      bindings = <
GRID ROW
      >;
    };
  };
};
"""

        self.assertEqual(FORMATTER.format_keymap_indentation(source), expected)


if __name__ == "__main__":
    unittest.main()
