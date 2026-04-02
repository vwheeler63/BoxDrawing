# BoxDrawing

**BoxDrawing** is a Sublime Text package enabling the user to draw lines and boxes like these:

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

- Draws using intuitive key combinations with arrow keys.
- Arrow-key bindings are temporary, while Box Drawing is turned ON.  You turn it OFF again when you are done.
- Intuitively overwrites characters where directed as if always in "overwrite" mode.
- There is no need to add spaces to short lines.  The package extends short lines with spaces automatically when needed, enabling you to conveniently draw wherever you direct it.
- Initially uses ASCII or Unicode box-drawing character sets, depending on a user-configurable setting.
- Switching between ASCII and Unicode character sets is conveniently accomplished with one keystroke.
- Box drawing with the ASCII character set is compatible with the requirements of reStructuredText tables.  (The above ASCII-based table is an example.)




## Installation

The preferred method of installing **BoxDrawing** is:  from Sublime Text's Command Palette, execute **Package Control: Install Package** and select **BoxDrawing**.

If you instead clone **BoxDrawing's** repository into your `<data_path>/Packages/BoxDrawing/` directory, ensure that the name of the directory uses a capital 'B' and capital 'D' as shown.  Otherwise, Sublime Text will not find certain files that it needs.



## Usage

1. In any type of document, ensure there is just 1 selection (caret) and that no text is selected.

2. Turn Box-Drawing ON using `[Alt-Keypad /]` or `Tools > Box Drawing Enabled`.  (A temporary Status-Bar message "Box Drawing ON/OFF" shows which mode that View is in.)  The  `Tools > Box Drawing Enabled` menu item always shows the ON/OFF state for the current View by showing a checkmark (**✓**) next to that menu item when Box Drawing is enabled.

4. Draw using single lines using the arrow keys while the `[Alt]` key is held down.

5. Draw using double lines using the arrow keys while the `[Alt+Shift]` keys are held down.

6. Erase using the arrow keys while the `[Alt-Shift-Ctrl]` keys are held down.
7. Toggle between character sets (ASCII/Unicode) using `[Alt-Keypad *]` or `Tools > Toggle Box Drawing Character Set (<current_set>)`.  (A temporary Status-Bar message "Box Drawing:  ASCII/Unicode" shows which character set was switched in.)  The `Tools > Toggle Box Drawing Character Set (<current_set>)` menu item always shows the current character set in parentheses.
8. When you are done drawing, turn Box-Drawing OFF again:  `[Alt-Keypad /]`.




## Settings

The following setting items can be found and individually overridden via the usual method for Sublime Text Package settings:  `Preferences > Package Settings > BoxDrawing > Settings`.  The comments in the default settings file explain what each one means and lists valid values.  Their default values are shown below.

- `default_character_set_id`: 0 (means ASCII)
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

By default, `[Alt-(Left|Right)]` key combinations are mapped to "move left/right by sub-words" with "extending selection" when the `[Shift]` key is held down.

And by default, `[Alt-(Up|Down)]` is mapped in the reStructuredText Package to "move up/down by 1 section", with a possible `[Shift]` modifier limiting the move to only the same level of section or higher.

These key bindings can be customized via:

    `Preferences > Package Settings > BoxDrawing > Key Bindings`.



## Menu Items

BoxDrawing adds the following menu items to Sublime Text when installed:

- [**✓**]  Tools > Box Drawing Enabled (checkmark appears when enabled; it's OFF by default)
- Tools > Toggle Box Drawing Character Set (ASCII/Unicode)  (default character set is configurable)
- Preferences > Package Settings > BoxDrawing > README
- Preferences > Package Settings > BoxDrawing > Settings
- Preferences > Package Settings > BoxDrawing > Key Bindings



## Commands

BoxDrawing adds the following Commands to Sublime Text when installed:

Action                           | Key Combination      | Command Palette
-------------------------------- | -------------------- | ------------------------------
Open README                      | ---not mapped---     | BoxDrawing: Open Readme
Edit BoxDrawing Settings         | ---not mapped---     | BoxDrawing: Edit BoxDrawing Settings
Edit BoxDrawing Key Bindings     | ---not mapped---     | BoxDrawing: Edit BoxDrawing Key Bindings
Turn Box-Drawing ON or OFF       | Alt-Keypad /         | BoxDrawing: Toggle ON/OFF
Toggle between ASCII and Unicode | Alt-Keypad *         | BoxDrawing: Toggle ASCII <==> Unicode
DrawOneCharacter(up, single)     | Alt-Up               | BoxDrawing: Draw Single Line Up
DrawOneCharacter(right, single)  | Alt-Right            | BoxDrawing: Draw Single Line Right
DrawOneCharacter(down, single)   | Alt-Down             | BoxDrawing: Draw Single Line Down
DrawOneCharacter(left, single)   | Alt-Left             | BoxDrawing: Draw Single Line Left
DrawOneCharacter(up, double)     | Alt-Shift-Up         | BoxDrawing: Draw Double Line Up
DrawOneCharacter(right, double)  | Alt-Shift-Right      | BoxDrawing: Draw Double Line Right
DrawOneCharacter(down, double)   | Alt-Shift-Down       | BoxDrawing: Draw Double Line Down
DrawOneCharacter(left, double)   | Alt-Shift-Left       | BoxDrawing: Draw Double Line Left
DrawOneCharacter(up, none)       | Ctrl-Alt-Shift-Up    | BoxDrawing: Draw Erase Up
DrawOneCharacter(right, none)    | Ctrl-Alt-Shift-Right | BoxDrawing: Draw Erase Right
DrawOneCharacter(down, none)     | Ctrl-Alt-Shift-Down  | BoxDrawing: Draw Erase Down
DrawOneCharacter(left, none)     | Ctrl-Alt-Shift-Left  | BoxDrawing: Draw Erase Left



## Notes

While Sublime Text supports having multiple carets, **BoxDrawing** will draw box characters only when:

- Box Drawing is ON for that View,
- there is one caret, and
- no text is selected.

