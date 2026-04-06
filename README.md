# BoxDrawing

**BoxDrawing** is a Sublime Text package enabling the user, normally with these arrow-key combinations:

- `[Alt-Arrow]`             (single line)
- `[Alt-Shift-Arrow]`       (double line), or
- `[Ctrl-Alt-Shift-Arrow]`  (erase)

to draw lines and boxes like these:

```
┌─┬┐  ╔═╦╗  ╓─╥╖  ╒═╤╕
│ ││  ║ ║║  ║ ║║  │ ││
├─┼┤  ╠═╬╣  ╟─╫╢  ╞═╪╡
└─┴┘  ╚═╩╝  ╙─╨╜  ╘═╧╛ ┌─────────────┐
╭───────────────────╮  │    ╔═══════╕│            ┌───┐
│  ╔═══╗ Some Text  │  │╓───╫┐ ╔══╗ ││ ┌──┬───┐  ┌┴┬┐ │
│  ╚═╦═╝ in the box │░ │║   ║│ ║  ║ ││ ╞══╡   │  ├─┼┼─┘
╞═╤══╩══╤═══════════╡░ │║   ║│ ║  ║ ││ │  │   │  │ ││
│ ├──┬──┤           │░ │╙───╫┘ ╚══╝ ││ └──┴───┘  └─┴┘
│ └──┴──┘           │░ └────╫───────┼┘
╰───────────────────╯░      ╙───────┘
  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░

+------------+----------------+--------------+
| Column One | Column Two     | Column Three |
+============+================+==============+
|            |                |              |
+------------+----------------+--------------+
|            |                |              |
+------------+----------------+--------------+
|            |                |              |
+------------+----------------+--------------+
|            |                |              |
+------------+----------------+--------------+

```



## Features

- Draw using intuitive key combinations with arrow keys.
- Arrow-key bindings are temporary, while Box Drawing is turned ON.  You turn it OFF again when you are done.
- Intuitively overwrites characters where directed as if always in "overwrite" mode.
- There is no need to add spaces to short lines.  The package extends short lines with spaces automatically when needed, enabling you to conveniently draw wherever you direct it.
- Initially uses ASCII or one of the Unicode box-drawing character sets, depending on a user-configurable setting.  (See below.)
- Conveniently switch between character sets with one keystroke.
- Box drawing with the ASCII character set is compatible with the requirements of reStructuredText tables.  (The above ASCII-based table is an example.)
- The current state of the BoxDrawing Package can be seen:
  - Tools > BoxDrawing > sub-menu items, and
  - in the status bar for 4 seconds after each state change.
- Supports these character sets:
  - ASCII
  - Unicode [Square Corners]
  - Unicode [Round Corners]
  - Unicode [2 Dashes]
  - Unicode [3 Dashes]
  - Unicode [4 Dashes]
  - Shadow Characters


## Installation

The preferred method of installing **BoxDrawing** is:  from Sublime Text's Command Palette, execute **Package Control: Install Package** and select **BoxDrawing**.

If you instead clone **BoxDrawing's** repository into your `<data_path>/Packages/BoxDrawing/` directory, ensure that the name of the directory uses a capital 'B' and capital 'D' as shown.  Otherwise, Sublime Text will not find certain files it needs.



## Usage

1. In any type of document, ensure there is just 1 selection (caret) and that no text is selected.

2. Turn Box-Drawing ON using `[Alt-Keypad /]` or `Tools > BoxDrawing > Enabled` or from the Command Palette `BoxDrawing: Toggle ON/OFF`.  (A temporary Status-Bar message "Box Drawing ON/OFF (<char_set>)" shows which mode the current View is in.)  The  `Tools > BoxDrawing > Enabled` menu item always shows the ON/OFF state for the current View by showing a checkmark (**✓**) next to that menu item when Box Drawing is enabled.

3. Draw using single lines using the arrow keys while the `[Alt]` key is held down.

4. Draw using double lines using the arrow keys while the `[Alt-Shift]` keys are held down.

5. Erase using the arrow keys while the `[Alt-Shift-Ctrl]` keys are held down.

6. Change current character set using `[Alt-Keypad *]` or `Tools > BoxDrawing > Change Character Set (<char_set>)` or from the Command Palette `BoxDrawing: Change Character Set`.  (A temporary Status-Bar message "Box Drawing ON/OFF:  <char_set>" shows which character set is now current.)  The `Tools > BoxDrawing > Change Character Set (<char_set>)` menu item always shows the current character set in parentheses.

7. When you are done drawing, turn Box-Drawing OFF again with `[Alt-Keypad /]`.




## Settings

The following setting items can be found and individually overridden via the usual method for Sublime Text Package settings:  `Preferences > Package Settings > BoxDrawing > Settings`.  The comments in the default settings file explain what each one means and lists valid values.  Their default values are shown below.

- `default_character_set_id`: 6 (means ASCII, as shown in comments)
- `debugging`: false



## Key Bindings

This Package provides the following customizable key bindings:

Key Combination                        | Meaning
-------------------------------------- | ------------------------------------------
Alt-Keypad /                           | Turn Box Drawing ON or OFF 
Alt-Keypad \*                          | Switch character sets (ASCII <==> Unicode)
Alt-(Left\|Right\|Up\|Down)            | Draw with single lines 
Alt-Shift-(Left\|Right\|Up\|Down)      | Draw with double lines 
Ctrl-Alt-Shift-(Left\|Right\|Up\|Down) | Erase

When Box-Drawing is ON for a particular View, the Package temporarily overrides the normal key bindings for the arrow-key combinations for that View only.  When Box Drawing is turned OFF again, normal key bindings for the arrow keys are resumed.  `[Alt-Keypad /]` and `[Alt-Keypad *]` both remain bound to the `ON/OFF` and `switch character sets` Commands full time.

By default, `[Alt-(Left|Right)]` key combinations are mapped to "move left/right by sub-words" with "extending selection" behavior added when the `[Shift]` key is held down.

And by default, `[Alt-(Up|Down)]` is mapped in the reStructuredText Package to "move up/down by 1 section", with a possible `[Shift]` modifier limiting the move to only the same level of section or higher.

These key bindings can be customized via:

    `Preferences > Package Settings > BoxDrawing > Key Bindings`.



## Menu Items

BoxDrawing adds the following menu items to Sublime Text when installed:

- [**✓**]  `Tools > BoxDrawing > Enabled` (checkmark appears when enabled; it's OFF by default)
- `Tools > Toggle BoxDrawing > Change Character Set (<char set>)`  (default character set is configurable)
- Preferences > Package Settings > BoxDrawing > README
- Preferences > Package Settings > BoxDrawing > Settings
- Preferences > Package Settings > BoxDrawing > Key Bindings



## Commands

BoxDrawing adds the following Commands to Sublime Text when installed:

Action                           | Key Combination          | Command Palette
-------------------------------- | ------------------------ | ------------------------------
Open README                      | ---not mapped---         | BoxDrawing: Open Readme
Edit BoxDrawing Settings         | ---not mapped---         | BoxDrawing: Edit BoxDrawing Settings
Edit BoxDrawing Key Bindings     | ---not mapped---         | BoxDrawing: Edit BoxDrawing Key Bindings
Turn Box-Drawing ON or OFF       | Alt-Keypad /             | BoxDrawing: Toggle ON/OFF
Toggle between ASCII and Unicode | Alt-Keypad *             | BoxDrawing: Toggle ASCII <==> Unicode
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

[^1]: when BoxDrawing is ON



## Notes

1.  While Sublime Text supports having multiple carets, **BoxDrawing** will draw box characters only when:

    - Box Drawing is ON for that View,
    - there is one caret, and
    - no text is selected.

2.  While the Shadow Character Set is selected, there is no ERASE function.  Instead, the modifier key combinations select which shadow character is written to the Buffer:

    - [Alt] => ligh shadow character
    - [Alt-Shift] => medium shadow character
    - [Alt-Shift-Ctrl] => dark shadow character
