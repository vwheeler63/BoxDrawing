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

2. Turn Box-Drawing ON using <kbd>Alt-Keypad /</kbd> or `Tools > BoxDrawing > Enabled` or from the Command Palette `BoxDrawing: Toggle ON/OFF`.  (A temporary Status-Bar message "Box Drawing ON/OFF (<char_set>)" shows which mode the current View is in.)  The  `Tools > BoxDrawing > Enabled` menu item always shows the ON/OFF state for the current View by showing a checkmark (**✓**) next to that menu item when Box Drawing is enabled.

3. Draw using single lines using the arrow keys while the <kbd>Alt</kbd> key is held down.

4. Draw using double lines using the arrow keys while the <kbd>Alt-Shift</kbd> keys are held down.

5. Erase using the arrow keys while the <kbd>Alt-Shift-Ctrl</kbd> keys are held down.

6. Change current character set using <kbd>Alt-Keypad \*</kbd> or `Tools > BoxDrawing > Change Character Set (char_set)` or from the Command Palette `BoxDrawing: Change Character Set`.  (A temporary Status-Bar message "Box Drawing ON/OFF:  (char_set)" shows which character set is now current.)  The `Tools > BoxDrawing > Change Character Set (char_set)` menu item always shows the current character set in parentheses.

7. When you are done drawing, turn Box-Drawing OFF again with <kbd>Alt-Keypad /</kbd> or `Tools > BoxDrawing > Enabled` or from the Command Palette `BoxDrawing: Toggle ON/OFF`.



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
Alt-(Left\|Right\|Up\|Down)            | Draw with single lines[^1]
Alt-Shift-(Left\|Right\|Up\|Down)      | Draw with double lines[^1]
Ctrl-Alt-Shift-(Left\|Right\|Up\|Down) | Erase[^1]

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
