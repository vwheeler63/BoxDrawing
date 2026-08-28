[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](https://github.com/vwheeler63/BoxDrawing/blob/master/LICENSE)
[![Requires Sublime Text Build 4000 or later](https://img.shields.io/badge/Sublime_Text-4000+-ca875a?style=flat-square&logo=sublimetext)](https://www.sublimetext.com)
[![Download BoxDrawing from Package Control](https://img.shields.io/packagecontrol/dt/BoxDrawing.svg?style=flat-square&logo=sublime-text)](https://packages.sublimetext.io/packages/BoxDrawing)
[![Latest Tag](https://img.shields.io/badge/tag-1.0.3-royalblue?style=flat-square&logo=github)](https://github.com/vwheeler63/BoxDrawing/tags)
[![GitHub Repository](https://img.shields.io/badge/github-repo-blue?style=flat-square&logo=github)](https://github.com/vwheeler63/BoxDrawing)

<div id="readme"></div>

# BoxDrawing

**BoxDrawing** is a Sublime Text package enabling the user, with these arrow-key combinations:

- <kbd>Alt-Arrow</kbd>  (single line)
- <kbd>Alt-Shift-Arrow</kbd>  (double line), or
- <kbd>Ctrl-Alt-Shift-Arrow</kbd>  (erase)

to draw lines and boxes like these:

![Example of BoxDrawing Lines and Boxes](https://raw.githubusercontent.com/vwheeler63/BoxDrawing/master/demo.png)



![Demo: Drawing an ASCII Table](https://raw.githubusercontent.com/vwheeler63/BoxDrawing/master/demo.gif)



#### Table of contents

* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)
* [Settings](#settings)
* [Key Bindings](#key-bindings)
* [Menu Items](#menu-items)
* [Commands](#commands)
* [Notes](#notes)

---



## Features

- Draw using intuitive key combinations with arrow keys.
- Arrow-key bindings are temporary, while Box Drawing is turned ON.  You turn it OFF again when you are done.
- Intuitively overwrites characters where directed as if always in "overwrite" mode.
- There is no need to add spaces to short lines.  The package extends short lines with spaces automatically when needed, enabling you to conveniently draw wherever you direct it.
- Initially uses ASCII or one of the Unicode box-drawing character sets, depending on a user-configurable setting.  (See below.)
- Conveniently switch between character sets with one keystroke.
- Box drawing with the ASCII character set is compatible with the requirements of reStructuredText tables.  (The ASCII table above is an example.)
- The current state of the BoxDrawing Package can be seen:
  - Tools > BoxDrawing > sub-menu items,
  - in the status bar continuously while Box Drawing is ON, and
  - in a status bar message for a few seconds after each state change.
- Supports these character sets:
  - ASCII
  - Unicode [Square Corners]
  - Unicode [Round Corners]
  - Unicode [2 Dashes]
  - Unicode [3 Dashes]
  - Unicode [4 Dashes]
  - Shadow Characters
- Paint with a *fill brush* instead of drawing lines.  Pick one of eight block/shade characters with a single keystroke, and the arrow keys paint instead of drawing:
  - ░ light shade, ▒ medium shade, ▓ dark shade, █ full block
  - ▀ upper half, ▄ lower half, ▌ left half, ▐ right half
- Flood-fill an area with the selected brush in one keystroke — or re-shade an already-filled area, or clear one back to spaces.
- The fill brush is independent of the character set:  switching character sets never changes your brush, and vice versa.
- While Box Drawing is ON, the status bar continuously shows the current mode, e.g. `Box Drawing ON (Unicode [Round Corners]) | Fill: ▐`.


## Installation

The preferred method of installing **BoxDrawing** is:  from Sublime Text's Command Palette, execute **Package Control: Install Package** and select **BoxDrawing**.

If you instead clone **BoxDrawing's** repository into your `<data_path>/Packages/BoxDrawing/` directory, ensure that the name of the directory uses a capital 'B' and capital 'D' as shown.  Otherwise, Sublime Text will not find certain files it needs.



## Usage

1. In any type of document, ensure there is just 1 selection (caret) and that no text is selected.

2. Turn Box-Drawing ON using <kbd>Alt-Keypad /</kbd> or `Tools > BoxDrawing > Enabled` or from the Command Palette `BoxDrawing: Toggle ON/OFF`.  (A temporary Status-Bar message "Box Drawing ON/OFF (<char_set>)" shows which mode the current View is in.)  The  `Tools > BoxDrawing > Enabled` menu item always shows the ON/OFF state for the current View by showing a checkmark (**✓**) next to that menu item when Box Drawing is enabled.

3. Draw using single lines using the arrow keys while the <kbd>Alt</kbd> key is held down.

4. Draw using double lines using the arrow keys while the <kbd>Alt-Shift</kbd> keys are held down.

5. Erase using the arrow keys while the <kbd>Alt-Shift-Ctrl</kbd> keys are held down.

6. Change current character set using <kbd>Alt-Keypad \*</kbd> or `Tools > BoxDrawing > Change Character Set (char_set)` or from the Command Palette `BoxDrawing: Change Character Set`.  (A temporary Status-Bar message "Box Drawing ON/OFF:  (char_set)" shows which character set is now current.)  The `Tools > BoxDrawing > Change Character Set (char_set)` menu item always shows the current character set in parentheses.

7. When you are done drawing, turn Box-Drawing OFF again with <kbd>Alt-Keypad /</kbd> or `Tools > BoxDrawing > Enabled` or from the Command Palette `BoxDrawing: Toggle ON/OFF`.


### Painting

While Box Drawing is ON, select a fill brush with <kbd>Ctrl-Alt-1</kbd> through <kbd>Ctrl-Alt-8</kbd>, or via `Tools > BoxDrawing > Fill Brush`, or from the Command Palette.  The arrow keys then paint that character instead of drawing lines:

Key Combination                        | Meaning
-------------------------------------- | ------------------------------------------
Alt-(Left\|Right\|Up\|Down)            | Paint the brush, then move in that direction
Alt-Shift-(Left\|Right\|Up\|Down)      | Paint the brush without moving
Ctrl-Alt-Shift-(Left\|Right\|Up\|Down) | Erase (unchanged)
Alt-Shift-Space                        | Flood fill, re-shade or clear

Erase deliberately keeps working while a brush is selected, so you never have to put the brush down just to rub something out.

<kbd>Ctrl-Alt-0</kbd> puts the brush down and returns to ordinary line drawing.  It changes drawing mode only:  it never modifies the document.

Here is a box drawn with the round-corner character set, then filled by putting the caret inside it, pressing <kbd>Ctrl-Alt-2</kbd> to pick ▒, and pressing <kbd>Alt-Shift-Space</kbd>.  The drop shadow was painted by hand with <kbd>Alt-Down</kbd> and <kbd>Alt-Right</kbd>:

```text
╭───────────────────╮
│▒▒╔═══╗▒Some▒Text▒▒│▒
│▒▒╚═╦═╝▒in▒the▒box▒│▒
╞═╤══╩══╤═══════════╡▒
│▒├──┬──┤▒▒▒▒▒▒▒▒▒▒▒│▒
│▒└──┴──┘▒▒▒▒▒▒▒▒▒▒▒│▒
╰───────────────────╯▒
 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
```


### What flood fill fills

Flood fill takes the connected run of **whatever character is under the caret** — the *seed* — and replaces all of it with your current brush, or with spaces when no brush is selected.  That one behavior covers three jobs:

Caret is on | Brush | Result
----------- | ----- | -----------------------------------------
a space     | ▓     | fill the empty area
▒           | ▓     | re-shade the already-filled area
▓           | none (<kbd>Ctrl-Alt-0</kbd>) | clear it back to spaces

You can only start a fill on a space or on one of the eight brush characters.  Put the caret on text or on a box-drawing character and it declines with "nothing to fill here" — which is what keeps the command safe to press:  otherwise a fill seeded on a box border would replace every connected border character in your drawing.

That cuts both ways, and is why boxes still work as boundaries:  a character that can't be seeded can't be overwritten either, since a cell only joins the region when it matches the seed.

Spreading is in the four cardinal directions, and stops at any character that isn't the seed — plus the end of each line and the edges of the document.

Because line ends and document edges are walls, the edges of your document are perfectly good sides of a shape.  A box flush against the right edge of the document fills correctly, and so does a shape with no right wall at all — each row simply fills up to its own end:

```text
┌──────────
│▒▒▒▒▒▒▒▒▒
│▒▒▒▒▒▒
│▒▒▒▒▒▒▒▒▒▒▒▒
└──────────────
```

A fill never lengthens a line, never adds trailing whitespace, and never extends the document.  The whole fill is a single undo step.

If the caret is not on something that can be seeded, if the region already holds the character you were about to fill it with, or if the region is larger than the `max_flood_cells` setting, the fill is abandoned:  in every case the document is left completely untouched and the status bar says why.



## Settings

The following setting items can be found and individually overridden via the usual method for Sublime Text Package settings:  `Preferences > Package Settings > BoxDrawing > Settings`.  The comments in the default settings file explain what each one means and lists valid values.  Their default values are shown below.

- `default_character_set_id`: 6 (means ASCII, as shown in comments)
- `default_fill_brush_id`: 0 (means no brush:  ordinary line-drawing mode)
- `fill_brush_characters`: `["░", "▒", "▓", "█", "▀", "▄", "▌", "▐"]`
- `max_flood_cells`: 100000
- `debugging`: false



## Key Bindings

This Package provides the following customizable key bindings:

Key Combination                        | Meaning
-------------------------------------- | ------------------------------------------
Alt-Keypad /                           | Turn Box Drawing ON or OFF 
Alt-Keypad \*                          | Switch character sets (ASCII <==> Unicode)
Alt-(Left\|Right\|Up\|Down)            | Draw with single lines[^1]
Alt-Shift-(Left\|Right\|Up\|Down)      | Draw with double lines[^1]
Ctrl-Alt-Shift-(Left\|Right\|Up\|Down) | Erase[^1]
Ctrl-Alt-0                             | Put the fill brush down[^1]
Ctrl-Alt-(1\|2\|3\|4\|5\|6\|7\|8)        | Select fill brush ░ ▒ ▓ █ ▀ ▄ ▌ ▐[^1]
Alt-Shift-Space                        | Flood fill, re-shade or clear[^1]

While a fill brush is selected, the <kbd>Alt</kbd>-arrow combinations above paint that brush instead of drawing lines.  See [Painting](#painting).

On Windows and Linux, <kbd>Ctrl-Alt</kbd> is the same as <kbd>AltGr</kbd>, which produces characters on several non-US keyboard layouts.  The brush bindings are therefore active only while Box Drawing is ON for the current View;  the rest of the time they are left alone for whatever else claims them.  If they still get in your way, re-map them via `Preferences > Package Settings > BoxDrawing > Key Bindings`.

When Box-Drawing is ON for a particular View, the Package temporarily overrides the normal key bindings for the arrow-key combinations for that View only.  When Box Drawing is turned OFF again, normal key bindings for the arrow keys are resumed.  <kbd>Alt-Keypad /</kbd> and <kbd>Alt-Keypad \*</kbd> both remain bound to the `ON/OFF` and `switch character sets` Commands full time.

By default, <kbd>Alt-(Left|Right)</kbd> key combinations are mapped to "move left/right by sub-words" with "extending selection" behavior added when the <kbd>Shift</kbd> key is held down.

And by default, <kbd>Alt-(Up|Down)</kbd> is mapped in the reStructuredText Package to "move up/down by 1 section", with a possible <kbd>Shift</kbd> modifier limiting the move to only the same level of section or higher.

If you need to re-map any of the above key bindings, you can do so via:

    `Preferences > Package Settings > BoxDrawing > Key Bindings`.



## Menu Items

**BoxDrawing** adds the following menu items to Sublime Text when installed:

- Tools >
    - BoxDrawing >
        - [✓] Enabled
        - Change Character Set (ASCII)
        - Draw Single Line  (Alt+Arrow)[^3]
        - Draw Double Line  (Alt+Shift+Arrow)[^3]
        - Fill Brush >
            - [✓] None
            - ░ Light Shade
            - ▒ Medium Shade
            - ▓ Dark Shade
            - █ Full Block
            - ▀ Upper Half Block
            - ▄ Lower Half Block
            - ▌ Left Half Block
            - ▐ Right Half Block
        - Flood Fill[^4]

[^3]: shown greyed out.  These are labels, not commands:  each arrow direction is a separate command invocation, so there is no single command a menu item could run.  They are listed so the key combinations are discoverable from the menu.
[^4]: this item explains itself when it is unavailable.  With Box Drawing OFF it reads "Flood Fill  (turn Box Drawing ON first)", and with a selection or multiple carets, "Flood Fill  (needs one caret, with nothing selected)".

- Preferences >
    -  Package Settings >
        - README
        - Settings
        - Key Bindings



## Commands

**BoxDrawing** adds the following Commands to Sublime Text when installed:

Action                           | Key Binding              | Command Palette
-------------------------------- | ------------------------ | ------------------------------
Open README                      | ---not bound---          | BoxDrawing: Open Readme
Edit BoxDrawing Settings         | ---not bound---          | Preferences: BoxDrawing Settings
Edit BoxDrawing Key Bindings     | ---not bound---          | Preferences: BoxDrawing Key Bindings
Turn Box-Drawing ON or OFF       | Alt-Keypad /             | BoxDrawing: Toggle ON/OFF
Toggle between ASCII and Unicode | Alt-Keypad \*            | BoxDrawing: Toggle ASCII <==> Unicode
DrawOneCharacter(up, single)     | Alt-Up[^1]               | BoxDrawing: Draw Single Line Up
DrawOneCharacter(right, single)  | Alt-Right[^1]            | BoxDrawing: Draw Single Line Right
DrawOneCharacter(down, single)   | Alt-Down[^1]             | BoxDrawing: Draw Single Line Down
DrawOneCharacter(left, single)   | Alt-Left[^1]             | BoxDrawing: Draw Single Line Left
DrawOneCharacter(up, double)     | Alt-Shift-Up[^1]         | BoxDrawing: Draw Double Line Up
DrawOneCharacter(right, double)  | Alt-Shift-Right[^1]      | BoxDrawing: Draw Double Line Right
DrawOneCharacter(down, double)   | Alt-Shift-Down[^1]       | BoxDrawing: Draw Double Line Down
DrawOneCharacter(left, double)   | Alt-Shift-Left[^1]       | BoxDrawing: Draw Double Line Left
DrawOneCharacter(up, none)       | Ctrl-Alt-Shift-Up[^1]    | BoxDrawing: Draw Erase Up
DrawOneCharacter(right, none)    | Ctrl-Alt-Shift-Right[^1] | BoxDrawing: Draw Erase Right
DrawOneCharacter(down, none)     | Ctrl-Alt-Shift-Down[^1]  | BoxDrawing: Draw Erase Down
DrawOneCharacter(left, none)     | Ctrl-Alt-Shift-Left[^1]  | BoxDrawing: Draw Erase Left
SelectFillBrush(none)            | Ctrl-Alt-0[^1]           | BoxDrawing: Fill Brush — None (return to line drawing)
SelectFillBrush(light shade)     | Ctrl-Alt-1[^1]           | BoxDrawing: Fill Brush — ░ Light Shade
SelectFillBrush(medium shade)    | Ctrl-Alt-2[^1]           | BoxDrawing: Fill Brush — ▒ Medium Shade
SelectFillBrush(dark shade)      | Ctrl-Alt-3[^1]           | BoxDrawing: Fill Brush — ▓ Dark Shade
SelectFillBrush(full block)      | Ctrl-Alt-4[^1]           | BoxDrawing: Fill Brush — █ Full Block
SelectFillBrush(upper half)      | Ctrl-Alt-5[^1]           | BoxDrawing: Fill Brush — ▀ Upper Half Block
SelectFillBrush(lower half)      | Ctrl-Alt-6[^1]           | BoxDrawing: Fill Brush — ▄ Lower Half Block
SelectFillBrush(left half)       | Ctrl-Alt-7[^1]           | BoxDrawing: Fill Brush — ▌ Left Half Block
SelectFillBrush(right half)      | Ctrl-Alt-8[^1]           | BoxDrawing: Fill Brush — ▐ Right Half Block
FloodFill                        | Alt-Shift-Space[^1]      | BoxDrawing: Flood Fill

[^1]: when BoxDrawing is ON



## Notes

1.  While Sublime Text supports having multiple carets, **BoxDrawing** will draw box characters only when:

    - Box Drawing is ON for that View,
    - there is one caret, and
    - no text is selected.

2.  While the Shadow Character Set is selected, there is no ERASE function.  Instead, the modifier key combinations select which shadow character is written to the Buffer:

    - <kbd>Alt</kbd> => light shadow character
    - <kbd>Alt-Shift</kbd> => medium shadow character
    - <kbd>Alt-Shift-Ctrl</kbd> => dark shadow character

3.  A selected fill brush supersedes the Shadow Character Set.  The brushes offer everything the Shadow Character Set does and more, so if you are reaching for shadow characters, <kbd>Ctrl-Alt-1</kbd> through <kbd>Ctrl-Alt-3</kbd> are usually what you want.

4.  The fill brush is global:  one brush is shared by every View, exactly like the character set.  Box Drawing's ON/OFF state remains per View.
