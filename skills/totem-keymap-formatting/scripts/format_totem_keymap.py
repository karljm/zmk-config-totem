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
INDENT = "  "
COLUMN_GAP = 2
DEFAULT_ROW_INDENT = 8
MIN_COL0_WIDTH = DEFAULT_ROW_INDENT - COLUMN_GAP


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
                    line += " " * (widths[column] + COLUMN_GAP)
            elif column == 0:
                line += " " * (widths[column] - len(cell))
                line += cell + " " * COLUMN_GAP
            else:
                line += cell
                line += " " * (widths[column] - len(cell) + COLUMN_GAP)
        lines.append(line.rstrip())

    return "\n".join(lines)


def format_keymap_indentation(text: str) -> str:
    """Use two-space indentation inside the root keymap node.

    Binding grid rows deliberately keep their absolute column positions: rows 1
    and 2 use normal content indentation when row 3's outer key fits before
    them, and row 4 is padded so its half separator aligns with the other rows.
    """
    lines = text.splitlines(keepends=True)
    keymap_start = next(
        (index for index, line in enumerate(lines) if re.match(r"\s*keymap\s*\{\s*$", line.rstrip("\r\n"))),
        None,
    )
    if keymap_start is None:
        return text

    depth = 0
    in_bindings = False
    for index in range(keymap_start, len(lines)):
        raw = lines[index]
        newline = "\n" if raw.endswith("\n") else ""
        content = raw.rstrip("\r\n").lstrip()

        if index == keymap_start:
            lines[index] = f"{INDENT}{content}{newline}"
            depth = 1
            continue

        if in_bindings:
            if content == ">;":
                lines[index] = f"{INDENT * (depth + 1)}{content}{newline}"
                in_bindings = False
            continue

        if not content:
            continue

        closes = content.startswith("}")
        line_depth = depth - 1 if closes else depth
        lines[index] = f"{INDENT * (line_depth + 1)}{content}{newline}"

        if content.startswith("bindings = <"):
            in_bindings = True

        depth += content.count("{") - content.count("}")
        if depth == 0:
            break

    return "".join(lines)


def format_keymap(text: str) -> str:
    pattern = re.compile(r"(?P<prefix>bindings = <\n)(?P<body>.*?)(?P<suffix>\n\s*>;)", re.DOTALL)

    def replace(match: re.Match[str]) -> str:
        body = match.group("body")
        cells = split_cells(body)
        formatted = format_rows(cells)
        return f"{match.group('prefix')}{formatted}{match.group('suffix')}"

    return format_keymap_indentation(pattern.sub(replace, text))


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
