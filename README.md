# BoxDrawing

**BoxDrawing** is a Sublime Text package enabling the user to draw lines and boxes like these:

```
┌─┬┐  ╔═╦╗  ╓─╥╖  ╒═╤╕
│ ││  ║ ║║  ║ ║║  │ ││
├─┼┤  ╠═╬╣  ╟─╫╢  ╞═╪╡
└─┴┘  ╚═╩╝  ╙─╨╜  ╘═╧╛
┌───────────────────┐
│  ╔═══╗ Some Text  │
│  ╚═╦═╝ in the box │
╞═╤══╩══╤═══════════╡
│ ├──┬──┤           │
│ └──┴──┘           │
└───────────────────┘

+-----+-+-+-+-----------------------------------------------------+
|Key  |S|C|A| Command                                             |
+=====+=+=+=+=====================================================+
|Up   | |x| | stop side-by-side editing                           |
+-----+-+-+-+-----------------------------------------------------+
|Left | |x| | deselect Sheet to the left                          |
+-----+-+-+-+-----------------------------------------------------+
|Left |x|x| | select Sheet to the left                            |
+-----+-+-+-+-----------------------------------------------------+
|Right| |x| | deselect Sheet to the right,                        |
+-----+-+-+-+-----------------------------------------------------+
|Right|x|x| | select Sheet to the right                           |
+-----+-+-+-+-----------------------------------------------------+
|PgUp | |x| | move focus to selected Sheet to the left            |
+-----+-+-+-+-----------------------------------------------------+
|PgDn | |x| | move focus to selected Sheet to the right           |
+-----+-+-+-+-----------------------------------------------------+
|j    | |x| | open message box explaining `ctrl+j` mapping change |
+-----+-+-+-+-----------------------------------------------------+
```

using:

- `[Alt+Arrow]` (to draw with single lines)
- `[Alt+Shift+Arrow]` (to draw with double lines), or
- `[Ctrl+Alt+Shift+Arrow]` (erase)

Wherever the user directs box drawing to go replaces any text that is already there, as if in "overwrite" mode, and extends text with spaces as needed to go there.

The type of box characters used depend upon the `character_set` setting.  Valid options are:  "ASCII" (default), and "Unicode".

Note:  re-binding the above key combinations in a `.sublime-keymap` file in your `User` package will interfere with this Package unless you re-bind the box-drawing keys to something else.



## Features

- feature 1
- feature 2
- feature 3
- feature 4
- feature 5
- feature 6
- feature 7



## Installation

The preferred method of installing **BoxDrawing** is:  from Sublime Text's Command Palette, execute **Package Control: Install Package** and select **BoxDrawing**.

If you clone **BoxDrawing's** repository into your Sublime Text's `Packages/BoxDrawing/` directory, ensure that the name of the directory uses a capital 'B' and capital 'D' as shown.  Otherwise, Sublime Text will not find certain files that it needs.



### Key Bindings

This Package remember what drawing mode it is in (``OFF`` vs ``ON``)
through a command to turn box-drawing mode ON and OFF (which the user is free
to map to any key combination he wishes, or simply execute the command via
the Command Palette).  The Package would have a custom ``on_query_context``
implemented to override these normal key combinations when box drawing mode
was ON:

+--------------------------------+-------------+
| Key Combination                | Meaning     |
+================================+=============+
| alt+(left|right|up|down)       | single line |
+--------------------------------+-------------+
| alt+shift+(left|right|up|down) | double line |
+--------------------------------+-------------+

When ``linedrawing.on_query_context()`` returns ``True`` (based on
mode), its keymap would override the default key mappings for
[alt+(left|right|up|down)].  [alt+(left|right)] is mapped by default to
"move left/right by subwords" with "extending selection" when the [Shift]
key is held down.

[alt+(up|down)] are mapped in the reStructuredText Package to "move up/down
by 1 section", with a possible [Shift] modifier limiting the move to only
the same level of section or higher.

When the LineDrawing Package is in OFF mode, ``linedrawing.on_query_context()``
returns ``False`` or ``None`` as appropriate, and Sublime Text would use the
normal mappings for these keys.  When the Package is in ``ON``
however, it will catch these keys and act on them with:

- [Alt] = draw single-line, and
- [Shift] = draw double-line.

They can be customized via:

    `Preferences > Package Settings > BoxDrawing > Key Bindings`.

These default Key Bindings are provided:

Action                          | Key                  | Command
------------------------------- | -------------------- | ------------------------------
DrawBoxCharacter(up, single)    | alt+up               | BoxDrawing: Draw Box Character -- Up Single Line
DrawBoxCharacter(up, double)    | alt+shift+up         | BoxDrawing: Draw Box Character -- Up Double Line
DrawBoxCharacter(up, none)      | ctrl+alt+shift+up    | BoxDrawing: Draw Box Character -- Up Erase
DrawBoxCharacter(right, single) | alt+right            | BoxDrawing: Draw Box Character -- Right Single Line
DrawBoxCharacter(right, double) | alt+shift+right      | BoxDrawing: Draw Box Character -- Right Double Line
DrawBoxCharacter(right, none)   | ctrl+alt+shift+right | BoxDrawing: Draw Box Character -- Right Erase
DrawBoxCharacter(down, single)  | alt+down             | BoxDrawing: Draw Box Character -- Down Single Line
DrawBoxCharacter(down, double)  | alt+shift+down       | BoxDrawing: Draw Box Character -- Down Double Line
DrawBoxCharacter(down, none)    | ctrl+alt+shift+down  | BoxDrawing: Draw Box Character -- Down Erase
DrawBoxCharacter(left, single)  | alt+left             | BoxDrawing: Draw Box Character -- Left Single Line
DrawBoxCharacter(left, double)  | alt+shift+left       | BoxDrawing: Draw Box Character -- Left Double Line
DrawBoxCharacter(left, none)    | ctrl+alt+shift+left  | BoxDrawing: Draw Box Character -- Left Erase



### Configuration

The following configuration items can be found and individually overridden via the usual method for Sublime Text Package settings (by creating a `BoxDrawing.sublime-settings` file in your `User` Package).  Access the default version of this file via:  `Preferences > Package Settings > BoxDrawing > Settings`.  The comments in the default version of this file explain what each one means and, where applicable, the limits of their valid values.  Their default values are shown below.

- `character_set`: "ASCII",
- `debugging`: false



## Usage

You get **BoxDrawing** to create both of these types of comments by telling it what you want through key combinations.

1. Ensure there is just 1 caret.

2. Start anywhere in text.

3. Ensure the keypad [NumLock] key is ON.

4. Hold down the [Alt] key and hit the keypad arrow keys to tell BoxDrawing where you want your line to go.

5.  Hold down the [Shift] to to draw with a "double line".

6.  Hold down all 3 of [Ctrl] + [Alt] + [Shift] to erase.


## Notes

While Sublime Text supports having multiple carets, **BoxDrawing** will only insert a comment when there is one caret.
