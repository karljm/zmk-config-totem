#!/usr/bin/env python3
"""Format Totem ZMK keymap binding blocks into the repo's visual grid."""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path


ROW_COLUMNS = [
    range(1, 11),
    range(1, 11),
    range(0, 12),
    range(3, 9),
]
EXPECTED_BINDINGS = sum(len(row) for row in ROW_COLUMNS)
MIN_COL0_WIDTH = 12


def split_cells(block: str) -> list[str]:
    cells: list[list[str]] = []
    current: list[str] | None = None

    for token in re.findall(r"\S+", block):
        if token == "/**/":
            continue
        if token.startswith("&"):
            current = [token]
            cells.append(current)
        elif current is not None:
            current.append(token)

    return [" ".join(cell) for cell in cells]


def cells_to_rows(cells: list[str]) -> list[list[str | None]]:
    if len(cells) != EXPECTED_BINDINGS:
        raise ValueError(f"expected {EXPECTED_BINDINGS} bindings, found {len(cells)}")

    rows: list[list[str | None]] = []
    index = 0
    for columns in ROW_COLUMNS:
        row: list[str | None] = [None] * 12
        for column in columns:
            row[column] = cells[index]
            index += 1
        rows.append(row)
    return rows


def format_rows(cells: list[str]) -> str:
    rows = cells_to_rows(cells)
    widths = []
    for column in range(12):
        width = max((len(row[column]) for row in rows if row[column] is not None), default=0)
        if column == 0:
            width = max(width, MIN_COL0_WIDTH)
        widths.append(width)

    lines = []
    for row in rows:
        line = ""
        for column, cell in enumerate(row):
            if column == 6:
                line += "/**/  "
            if cell is None:
                if column != 6:
                    line += " " * (widths[column] + 2)
            else:
                line += cell
                line += " " * (widths[column] - len(cell) + 2)
        lines.append(line.rstrip())

    return "\n".join(lines)


def format_keymap(text: str) -> str:
    pattern = re.compile(r"(?P<prefix>bindings = <\n)(?P<body>.*?)(?P<suffix>\n\s*>;)", re.DOTALL)

    def replace(match: re.Match[str]) -> str:
        body = match.group("body")
        cells = split_cells(body)
        formatted = format_rows(cells)
        return f"{match.group('prefix')}{formatted}{match.group('suffix')}"

    return pattern.sub(replace, text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("keymap", type=Path, help="Path to config/totem.keymap")
    parser.add_argument("--check", action="store_true", help="Exit non-zero if formatting would change")
    args = parser.parse_args()

    original = args.keymap.read_text()
    try:
        formatted = format_keymap(original)
    except ValueError as exc:
        print(f"{args.keymap}: {exc}", file=sys.stderr)
        return 2

    if args.check:
        if formatted == original:
            return 0
        diff = difflib.unified_diff(
            original.splitlines(),
            formatted.splitlines(),
            fromfile=str(args.keymap),
            tofile=f"{args.keymap} (formatted)",
            lineterm="",
        )
        print("\n".join(diff))
        return 1

    if formatted != original:
        args.keymap.write_text(formatted)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
