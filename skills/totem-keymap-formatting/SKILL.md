---
name: totem-keymap-formatting
description: Format Totem ZMK keymap layer bindings in config/totem.keymap. Use when Codex is editing, reflowing, reviewing, or preserving the visual layout of Totem keymap layers, especially tasks involving binding alignment, the /**/ half separator, 38-key layer shape, or column spacing.
---

# Totem Keymap Formatting

## Workflow

Use this skill when changing `config/totem.keymap` layer bindings or when asked to reformat the keymap layout.

1. Preserve binding order unless the user explicitly asks for a remap.
2. Format each `bindings = < ... >;` block as the Totem 38-key shape:
   - Row 1: columns 1-10
   - Row 2: columns 1-10
   - Row 3: columns 0-11
   - Row 4: columns 3-8
3. Insert `/**/` before column 6 on every row to mark the split between halves.
4. Pad every physical column to the longest binding in that column, then add exactly two spaces before the next column.
5. Align row 1 and row 2 with the same horizontal start as row 3's second key. This is done by treating column 0 as at least 12 characters wide, then adding the normal two-space gap.
6. Keep labels and non-binding properties unchanged.

## Formatter Script

Prefer the bundled script for repeatable formatting:

```bash
python3 skills/totem-keymap-formatting/scripts/format_totem_keymap.py config/totem.keymap
```

Use `--check` to verify formatting without writing:

```bash
python3 skills/totem-keymap-formatting/scripts/format_totem_keymap.py --check config/totem.keymap
```

The script parses binding cells that start with `&` and keeps trailing binding parameters together, such as `&lt NAV SPACE`, `&bt BT_SEL 0`, and `&kp LS(TAB)`.

## Validation

After formatting, verify that each layer binding block still has 38 bindings:

```bash
awk '/bindings = </{in_block=1; count=0; next} in_block && />;/{print count; in_block=0; next} in_block {for (i=1; i<=NF; i++) if ($i ~ /^&/) count++}' config/totem.keymap
```

Expected output for six layers:

```text
38
38
38
38
38
38
```
