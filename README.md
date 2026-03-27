# BoxDrawing

**BoxDrawing** is a Sublime Text package enabling the user to draw lines and boxes like these:

```
┌─┬┐  ╔═╦╗  ╓─╥╖  ╒═╤╕
│ ││  ║ ║║  ║ ║║  │ ││
├─┼┤  ╠═╬╣  ╟─╫╢  ╞═╪╡
└─┴┘  ╚═╩╝  ╙─╨╜  ╘═╧╛┌─────────────┐
┌───────────────────┐ │    ╔═══════╕│            ┌───┐
│  ╔═══╗ Some Text  │ │╓───╫┐ ╔══╗ ││ ┌──┬───┐  ┌┴┬┐ │
│  ╚═╦═╝ in the box │ │║   ║│ ║  ║ ││ ╞══╡   │  ├─┼┼─┘
╞═╤══╩══╤═══════════╡ │║   ║│ ║  ║ ││ │  │   │  │ ││
│ ├──┬──┤           │ │╙───╫┘ ╚══╝ ││ └──┴───┘  └─┴┘
│ └──┴──┘           │ └────╫───────┼┘
└───────────────────┘      ╙───────┘

+-----+-+-+-+---------------------------------------------------------------------+
|Key  |S|C|A| Command                                                             |
+=====+=+=+=+=====================================================================+
|Up   | |x| | stop side-by-side editing, deselecting all but the Sheet with focus |
+-----+-+-+-+---------------------------------------------------------------------+
|Left | |x| | deselect Sheet to the left, removing it from side-by-side editing   |
+-----+-+-+-+---------------------------------------------------------------------+
|Left |x|x| | select Sheet to the left, adding it to side-by-side editing         |
+-----+-+-+-+---------------------------------------------------------------------+
|Right| |x| | deselect Sheet to the right, removing it from side-by-side editing  |
+-----+-+-+-+---------------------------------------------------------------------+
|Right|x|x| | select Sheet to the right, adding it to side-by-side editing        |
+-----+-+-+-+---------------------------------------------------------------------+
|PgUp | |x| | move focus to selected Sheet to the left                            |
+-----+-+-+-+---------------------------------------------------------------------+
|PgDn | |x| | move focus to selected Sheet to the right                           |
+-----+-+-+-+---------------------------------------------------------------------+
|j    | |x| | open message box explaining `ctrl+j` mapping change                 |
+-----+-+-+-+---------------------------------------------------------------------+

```



Wherever the user directs box drawing to go replaces any text that is already there, as if in "overwrite" mode, and extends text with spaces as needed to go there.

The type of box characters used depend upon the Package's `character_set` setting.  Valid options are:  "ASCII" (default), and "Unicode".  See the Configuration section below to see how to change the Package's settings.



## Features

- Uses ASCII or Unicode box-drawing characters, depending on a customizable setting.
- feature 2
- feature 3
- feature 4
- feature 5
- feature 6
- feature 7



## Installation

The preferred method of installing **BoxDrawing** is:  from Sublime Text's Command Palette, execute **Package Control: Install Package** and select **BoxDrawing**.

If you instead clone **BoxDrawing's** repository into your `<data_path>/Packages/BoxDrawing/` directory, ensure that the name of the directory uses a capital 'B' and capital 'D' as shown.  Otherwise, Sublime Text will not find certain files that it needs.



## Usage

You get **BoxDrawing** to draw lines and boxes by telling it what you want through key combinations.

1. Ensure there is just 1 caret.

2. Start anywhere in text.

3. Turn Box-Drawing ON:  `[Alt-Keypad /]`.  (A temporary Status-Bar message "BoxDrawing ON" or "BoxDrawing OFF" shows which mode that View is in.)

4. Draw lines and boxes by hitting the arrow keys (`[Up]`, `[Right]`, `[Down]` or `[Left]`) while `[Alt]` or `[Alt-Shift]` are held down for single- and double-lines respectively.

5. Do the same while ERASING instead of drawing lines by holding down `[Alt-Shift-Ctrl]`.

6. When you are done, turn Box-Drawing OFF again:  `[Alt-Keypad /]`.




## Key Bindings

This Package provides the following key customizable bindings:

Key Combination                        | Meaning
-------------------------------------- | -----------
Alt-Keypad / | turn Box Drawing ON or OFF
Alt-(Left\|Right\|Up\|Down)            | single line
Alt-Shift-(Left\|Right\|Up\|Down)      | double line
Ctrl-Alt-Shift-(Left\|Right\|Up\|Down) | erase

When Box-Drawing is ON, the Package temporarily overrides the normal key bindings for the arrow-key combinations.  When Box Drawing is turned OFF again, everything goes back to normal.  (The [Alt-Keypad /] remains active full time.)

When the ``on_query_context()`` returns ``True`` (based on ON/OFF mode, there being only a single caret, and no text being selected), this Package's key map overrides the default key mappings for the various [Alt] [Alt-Shift] and [Ctrl-Alt-Shift] key modifiers combined with the arrow keys.

By default, [Alt-(Left|Right)] key combinations are mapped to "move left/right by sub-words" with "extending selection" when the [Shift] key is held down.

And by default, [Alt-(Up|Down)] is mapped in the reStructuredText Package to "move up/down by 1 section", with a possible [Shift] modifier limiting the move to only the same level of section or higher.

When the Box-Drawing is OFF for a particular View, its ``on_query_context()`` returns ``False`` or ``None`` as appropriate, and Sublime Text uses the normal mappings for these keys.

These key bindings can be customized via:

    `Preferences > Package Settings > BoxDrawing > Key Bindings`.



## Commands

BoxDrawing adds the following Commands to Sublime Text when installed:

Action                          | Key Combination      | Command Palette
------------------------------- | -------------------- | ------------------------------
Open README                     | ---not mapped---     | BoxDrawing: Open Readme
Edit BoxDrawing Settings        | ---not mapped---     | BoxDrawing: Edit BoxDrawing Settings
Edit BoxDrawing Key Bindings    | ---not mapped---     | BoxDrawing: Edit BoxDrawing Key Bindings
Turn Box-Drawing ON or OFF      | Alt-Keypad /         | BoxDrawing: Toggle ON/OFF
DrawOneCharacter(up, single)    | Alt-Up               | BoxDrawing: Draw Single Line Up
DrawOneCharacter(right, single) | Alt-Right            | BoxDrawing: Draw Single Line Right
DrawOneCharacter(down, single)  | Alt-Down             | BoxDrawing: Draw Single Line Down
DrawOneCharacter(left, single)  | Alt-Left             | BoxDrawing: Draw Single Line Left
DrawOneCharacter(up, double)    | Alt-Shift-Up         | BoxDrawing: Draw Double Line Up
DrawOneCharacter(right, double) | Alt-Shift-Right      | BoxDrawing: Draw Double Line Right
DrawOneCharacter(down, double)  | Alt-Shift-Down       | BoxDrawing: Draw Double Line Down
DrawOneCharacter(left, double)  | Alt-Shift-Left       | BoxDrawing: Draw Double Line Left
DrawOneCharacter(up, none)      | Ctrl-Alt-Shift-Up    | BoxDrawing: Draw Erase Up
DrawOneCharacter(right, none)   | Ctrl-Alt-Shift-Right | BoxDrawing: Draw Erase Right
DrawOneCharacter(down, none)    | Ctrl-Alt-Shift-Down  | BoxDrawing: Draw Erase Down
DrawOneCharacter(left, none)    | Ctrl-Alt-Shift-Left  | BoxDrawing: Draw Erase Left



## Settings

The following setting items can be found and individually overridden via the usual method for Sublime Text Package settings:  `Preferences > Package Settings > BoxDrawing > Settings`.  The comments in the default settings file explain what each one means and, where applicable, the limits of their valid values.  Their default values are shown below.

- `character_set`: "ASCII"
- `debugging`: false



## Notes

While Sublime Text supports having multiple carets, **BoxDrawing** will draw box characters when:

- Box Drawing is ON for that View,
- there is one caret, and
- no text is selected.

