# Totem Key Position Reference

ZMK combo `key-positions` use the zero-based position of each binding in the
keymap, read left-to-right and top-to-bottom.

```text
                00  01  02  03  04      05  06  07  08  09
                10  11  12  13  14      15  16  17  18  19
            20  21  22  23  24  25      26  27  28  29  30  31
                            32  33  34      35  36  37
```

Base layer labels for orientation:

```text
                B   L   D   W   Z       ?   F   O   U   J
                N   R   T   S   G       Y   H   A   E   I
            --  Q   X   M   C   V       K   P   .   ,   /   ;
                            NUM NAV SYM     SYM NAV NUM
```

Hold 34 or 35 for SYM; tap either for sticky Shift.

While holding a NUM/SYM thumb, tap a pinky key to switch:

| Row | Positions | Destination |
| --- | --- | --- |
| Top | 0 / 9 | SYM |
| Middle | 10 / 19 | SYM2 |
| Bottom | 21 / 30 | NUM |

These destinations are identical on NUM, SYM and SYM2. Release the entry
thumb to clear the number/symbol layers and FUN.
Use this flow with a held entry: switching after a sticky NUM tap leaves the
destination active; hold and release a SYM thumb to clear it.

Relocated keys: NUM has keypad 0 at 4, percent at 14 and slash at 25;
SYM has backslash at 4 and colon at 25. The 3x3 number block is unchanged.
