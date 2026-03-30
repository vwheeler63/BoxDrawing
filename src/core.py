r""" ***********************************************************************
Box Drawing
===========================================================================

Box Drawing is Sublime Text package enabling the user to use

- [Alt+Arrow]             (single line)
- [Alt+Shift+Arrow]       (double line), or
- [Ctrl+Alt+Shift+Arrow]  (erase)

to draw lines and boxes in their text like these:

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

Wherever the user directs box drawing to go replaces any text that
is already there, as if in "overwrite" mode.

Box drawing can be directed into unused space after line endings and it
appends enough space characters at the end of the target line so as to
accommodate the new line character.


Vocabulary
==========

- src character, the character at the position the cursor is moving FROM.
- dest character, the character at the position the cursor is moving TO.


Behavior
========

Box drawing is turned ON to draw lines, and turned OFF again to permit the
mapped key combinations to be used for other things.

Issuing a box-drawing command impacts both the src and dest characters.  It
effects a "pull" on the src character, thus if 1 or 2 lines are being used,
that character gets 1 or 2 lines on the side of the direction the caret is
travelling.  As for the dest character, it effects a "push" the side the
caret is coming FROM.  Thus if 1 or 2 lines are being used, that character
gets 1 or 2 lines on the side of the "push".


      src character   dest character
    +---------------+---------------+
    |               |               |
    |               |               |
    |               |               |
    |               |               |
    |               |               |
    |         pull --> push         |
    |               |               |
    |               |               |
    |               |               |
    |               |               |
    |               |               |
    |               |               |
    +---------------+---------------+

Result if 1 line is being used:

      src character   dest character
    +---------------+---------------+
    |               |               |
    |               |               |
    |               |               |
    |               |               |
    |               |               |
    |        -------|-------        |
    |               |               |
    |               |               |
    |               |               |
    |               |               |
    |               |               |
    |               |               |
    +---------------+---------------+



Variables in the Algorithm
==========================

The algorithm used to modify the source and destination characters involves
a set of variables and character classifications.

- number of lines to write (1 or 2; see line characters below);
- direction of movement;
- classification of source character before and after the "pull";
- classification of destination character before and after the "push";
- classification of characters above, below, to the left and right of
  the destination character.   (?)  (Box drawing can be without this,
  but we may want to automate "connection" to neighboring characters.
  It might be enough to examine the characters on the LEFT and RIGHT
  of the direction of travel at the dest character.)
- Box drawing in ASCII mode should be compatible with reStructuredText tables.



Line Types
==========


ASCII:
------

- List of chars we are using:
    - single-line characters:  |, -
    - double-line characters:  #, =
    - intersection character:  +, #


Unicode:
--------

- single-line characters
    - straight lines               :  ─ │
    - corners                      :  ┌ ┐ └ ┘
    - vertical with intersections  :  ├ ┤
    - horizontal with intersections:  ┬ ┴
    - both                         :  ┼

- half lines (single-line only):
    - left side only, horizontal :  ╴
    - right side only, horizontal:  ╶
    - top side only, vertical    :  ╵
    - bottom side only, vertical :  ╷

- There is a whole set of bold-face and half-line-bold-face single-line characters
  which are not included here.  Not very useful in my opinion.  These code points
  would have been better served supplying partials (like the above) for double-lines,
  of which there appear to be none currently.  In my opinion, those 87 code points
  were wasted in a block of 256 code points for this box-drawing character set.

- double-line characters
    - straight lines               :  ═ ║
    - corners                      :  ╔ ╗ ╚ ╝
    - vertical with intersections  :  ╠ ╣
    - horizontal with intersections:  ╦ ╩
    - both                         :  ╬

- combinations:
    - corners with single vertical lines   :  ╒ ╕ ╘ ╛
    - corners with single horizontal lines :  ╓ ╖ ╙ ╜
    - double with single-line intersections:  ╟ ╢ ╤ ╧
    - single with double-line intersections:  ╞ ╡ ╥ ╨
    - both                                 :  ╪ ╫

Examples:
~~~~~~~~~

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



Character Classification
========================

See docstring in line_count() function below.



Keys
====

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



Resources for Detecting Empty Space to Right of EOL
===================================================

Given any document of any size, and arguments of `row` and `col`:

.. code-block:: py

    last_pt = view.size()
    last_row, last_col = view.rowcol(last_pt)

give us the boundaries we need to work with `row` and `col` and
append spaces where needed.

    pt1 = view.text_point(16, 10, clamp_column=False)
    pt2 = view.text_point(16, 10, clamp_column=True)
    last_pt = view.size()

``pt1`` is row (16,0) + 10 clamped to EOF
``pt2`` is row (16,0) + 10 clamped to EOF AND clamped to EOL.
``pt1 > pt2`` when column 10 is past the end of row 16.
But ``pt1 - pt2`` is not always the number of spaces that need to be
appended to row 16 for (row,col) to be a valid position in Buffer.

Because both ``pt1`` and ``pt2`` are clamped to EOF, neither will ever
be larger than ``last_pt``.




*********************************************************************** """
from datetime import datetime, timezone
from typing import List
import pprint  # For human-readable data dumps when debugging.
import re
import os
import sys
import sublime
from sublime import View, Region
import sublime_plugin
from enum import IntEnum, IntFlag
from ..lib.debug import DebugBit, is_debugging, set_debugging_bits
from ..lib import utils
from ..boxdrawing import package_name


# =========================================================================
# Configuration
# =========================================================================

# Use name of parent directory as `package_name`.
_cfg_pkg_settings_file = package_name + '.sublime-settings'

# Track on-settings-changed listener.
_cfg_on_settings_chgd_listener_id = '_bd_settings_changed_tag'

# Neutral character in look-up arrays.
_cfg_neutral_character = '·'

# Package Settings Names (most are used multiple times throughout this Plugin)
_cfg_stg_name__character_set                         = 'character_set'
_cfg_stg_name__debugging                             = 'debugging'


# =========================================================================
# Package Settings
# =========================================================================

def bd_setting(setting_name: str):
    """
    Get a setting from a cached settings object.
    This function expects the following objects to already exist:

    - ``bd_setting.obj``      a ``sublime.Settings`` object (looks like a dictionary)
    - ``bd_setting.default``  a dictionary object with named default values

    :param setting_name:  name of setting whose value will be returned
    """
    assert bd_setting.default is not None, '`bd_setting.default` must exist before calling `bd_setting()`.'
    assert bd_setting.obj is not None, '`bd_setting.obj` must exist before calling `bd_setting()`.'
    default = bd_setting.default.get(setting_name, None)
    return bd_setting.obj.get(setting_name, default)


# =========================================================================
# Load default settings once.
# =========================================================================

bd_setting.default = {
    _cfg_stg_name__character_set: "ASCII",
    _cfg_stg_name__debugging: False
}


# =========================================================================
# Package-Wide Classes
# =========================================================================

class Direction(IntEnum):
    """
    DrawingDirection Enumeration

    Characterization mentioned in comments is from
    `gdict_unicode_classification_by_char_ordered` dictionary values.
    """
    NONE  = -1  # Happens after Package load, turning box-drawing off, and an ERASE;
                #   to detect "change of direction"
    UP    = 0   # val * 2 = bit-shift right to isolate classification in 2 LSbs
    RIGHT = 1   # val * 2 = bit-shift right to isolate classification in 2 LSbs
    DOWN  = 2   # val * 2 = bit-shift right to isolate classification in 2 LSbs
    LEFT  = 3   # val * 2 = bit-shift right to isolate classification in 2 LSbs


class State(IntEnum):
    """
    Whether a particular View is in Box-Drawing Mode or not.
    """
    OFF = 0
    ON  = 1   # In box-drawing mode


class ClassificationField(IntFlag):
    r"""
    Character Classification
    ========================

    Character Classification consists of 1 byte containing four 2-bit fields:

    +-+-+-+-+-+-+-+-+
    |t|t|r|r|b|b|L|L|
    +-+-+-+-+-+-+-+-+
     \_/ \_/ \_/ \_/
      L   b   r   t

    where:
        t = top side
        r = right side
        b = bottom side
        L = left side

    The unsigned integer in each bit field contains:

    - 0 = no lines
    - 1 = 1 line
    - 2 = 2 lines

    The OR-ed combined value will index into a character-lookup array for fast
    character selection by combining bits from this classification list.
    """
    LINES_UP_0    = 0x00
    LINES_UP_1    = 0x01
    LINES_UP_2    = 0x02

    LINES_RIGHT_0 = 0x00
    LINES_RIGHT_1 = 0x04
    LINES_RIGHT_2 = 0x08

    LINES_DOWN_0  = 0x00
    LINES_DOWN_1  = 0x10
    LINES_DOWN_2  = 0x20

    LINES_LEFT_0  = 0x00
    LINES_LEFT_1  = 0x40
    LINES_LEFT_2  = 0x80


# Abbreviation for the box-drawing character classification dictionaries
# below, to make constants like ``gdict_unicode_classification_by_char_ordered``
# more readable.
CF = ClassificationField


# =========================================================================
# Constants
# =========================================================================

# -------------------------------------------------------------------------
# Classifications by Box-Drawing Character
#
# Note:  not all bit combinations are represented.  While there appears
# to be a Unicode character for each bit-field combination, many fonts
# (including the one(s) used by Sublime Text) only have a subset of
# this list of characters in them.  So this list will be limited to
# those characters.
#
# Columns are in bit order left-to-right (most-significant to least):
#       LEFT   BOTTOM   RIGHT   TOP
# -------------------------------------------------------------------------
gdict_unicode_classification_by_char_ordered = {
    '└': CF.LINES_LEFT_0 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_1 | CF.LINES_UP_1,  # 0x05
    '╙': CF.LINES_LEFT_0 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_1 | CF.LINES_UP_2,  # 0x06
    '╘': CF.LINES_LEFT_0 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_2 | CF.LINES_UP_1,  # 0x09
    '╚': CF.LINES_LEFT_0 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_2 | CF.LINES_UP_2,  # 0x0A
    '│': CF.LINES_LEFT_0 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_0 | CF.LINES_UP_1,  # 0x11
    '┌': CF.LINES_LEFT_0 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_1 | CF.LINES_UP_0,  # 0x14
    '├': CF.LINES_LEFT_0 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_1 | CF.LINES_UP_1,  # 0x15
    '╒': CF.LINES_LEFT_0 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_2 | CF.LINES_UP_0,  # 0x18
    '╞': CF.LINES_LEFT_0 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_2 | CF.LINES_UP_1,  # 0x19
    '║': CF.LINES_LEFT_0 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_0 | CF.LINES_UP_2,  # 0x22
    '╓': CF.LINES_LEFT_0 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_1 | CF.LINES_UP_0,  # 0x24
    '╟': CF.LINES_LEFT_0 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_1 | CF.LINES_UP_2,  # 0x26
    '╔': CF.LINES_LEFT_0 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_2 | CF.LINES_UP_0,  # 0x28
    '╠': CF.LINES_LEFT_0 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_2 | CF.LINES_UP_2,  # 0x2A
    '┘': CF.LINES_LEFT_1 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_0 | CF.LINES_UP_1,  # 0x41
    '╜': CF.LINES_LEFT_1 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_0 | CF.LINES_UP_2,  # 0x42
    '─': CF.LINES_LEFT_1 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_1 | CF.LINES_UP_0,  # 0x44
    '┴': CF.LINES_LEFT_1 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_1 | CF.LINES_UP_1,  # 0x45
    '╨': CF.LINES_LEFT_1 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_1 | CF.LINES_UP_2,  # 0x46
    '┐': CF.LINES_LEFT_1 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_0 | CF.LINES_UP_0,  # 0x50
    '┤': CF.LINES_LEFT_1 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_0 | CF.LINES_UP_1,  # 0x51
    '┬': CF.LINES_LEFT_1 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_1 | CF.LINES_UP_0,  # 0x54
    '┼': CF.LINES_LEFT_1 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_1 | CF.LINES_UP_1,  # 0x55
    '╖': CF.LINES_LEFT_1 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_0 | CF.LINES_UP_0,  # 0x60
    '╢': CF.LINES_LEFT_1 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_0 | CF.LINES_UP_2,  # 0x62
    '╥': CF.LINES_LEFT_1 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_1 | CF.LINES_UP_0,  # 0x64
    '╫': CF.LINES_LEFT_1 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_1 | CF.LINES_UP_2,  # 0x66
    '╛': CF.LINES_LEFT_2 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_0 | CF.LINES_UP_1,  # 0x81
    '╝': CF.LINES_LEFT_2 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_0 | CF.LINES_UP_2,  # 0x82
    '═': CF.LINES_LEFT_2 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_2 | CF.LINES_UP_0,  # 0x88
    '╧': CF.LINES_LEFT_2 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_2 | CF.LINES_UP_1,  # 0x89
    '╩': CF.LINES_LEFT_2 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_2 | CF.LINES_UP_2,  # 0x8A
    '╕': CF.LINES_LEFT_2 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_0 | CF.LINES_UP_0,  # 0x90
    '╡': CF.LINES_LEFT_2 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_0 | CF.LINES_UP_1,  # 0x91
    '╤': CF.LINES_LEFT_2 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_2 | CF.LINES_UP_0,  # 0x98
    '╪': CF.LINES_LEFT_2 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_2 | CF.LINES_UP_1,  # 0x99
    '╗': CF.LINES_LEFT_2 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_0 | CF.LINES_UP_0,  # 0xA0
    '╣': CF.LINES_LEFT_2 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_0 | CF.LINES_UP_2,  # 0xA2
    '╦': CF.LINES_LEFT_2 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_2 | CF.LINES_UP_0,  # 0xA8
    '╬': CF.LINES_LEFT_2 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_2 | CF.LINES_UP_2,  # 0xAA
}

gdict_ascii_classification_by_char_ordered = {
    '|': CF.LINES_LEFT_0 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_0 | CF.LINES_UP_1,  # 0x11
    '-': CF.LINES_LEFT_1 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_1 | CF.LINES_UP_0,  # 0x44
    '+': CF.LINES_LEFT_1 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_1 | CF.LINES_UP_1,  # 0x55
    '=': CF.LINES_LEFT_2 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_2 | CF.LINES_UP_0,  # 0x88
    '#': CF.LINES_LEFT_2 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_2 | CF.LINES_UP_2,  # 0xAA
}

# -------------------------------------------------------------------------
# The following used the above Unicode classification dictionary
# to generate this ASCII lookup array for manual editing.  The
# finished arrayis here.  It is indexed by classification as is
# ``glst_unicode_box_char_lookup_by_classification`` which is
# populated programmatically below.  The result looks a great deal
# like this lookup array.
# -------------------------------------------------------------------------
_nc = _cfg_neutral_character
glst_ascii_box_char_lookup_by_classification = [
    _nc,  # 0x00 = CF.LINES_LEFT_0 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_0 | CF.LINES_UP_0
    '|',  # 0x01 = CF.LINES_LEFT_0 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_0 | CF.LINES_UP_1
    '#',  # 0x02 = CF.LINES_LEFT_0 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_0 | CF.LINES_UP_2
    _nc,  # 0x03
    '-',  # 0x04 = CF.LINES_LEFT_0 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_1 | CF.LINES_UP_0
    '+',  # 0x05 = CF.LINES_LEFT_0 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_1 | CF.LINES_UP_1
    '#',  # 0x06 = CF.LINES_LEFT_0 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_1 | CF.LINES_UP_2
    _nc,  # 0x07
    '=',  # 0x08 = CF.LINES_LEFT_0 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_2 | CF.LINES_UP_0
    '+',  # 0x09 = CF.LINES_LEFT_0 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_2 | CF.LINES_UP_1
    '#',  # 0x0A = CF.LINES_LEFT_0 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_2 | CF.LINES_UP_2
    _nc,  # 0x0B
    _nc,  # 0x0C
    _nc,  # 0x0D
    _nc,  # 0x0E
    _nc,  # 0x0F
    '|',  # 0x10 = CF.LINES_LEFT_0 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_0 | CF.LINES_UP_0
    '|',  # 0x11 = CF.LINES_LEFT_0 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_0 | CF.LINES_UP_1
    _nc,  # 0x12
    _nc,  # 0x13
    '+',  # 0x14 = CF.LINES_LEFT_0 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_1 | CF.LINES_UP_0
    '+',  # 0x15 = CF.LINES_LEFT_0 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_1 | CF.LINES_UP_1
    _nc,  # 0x16
    _nc,  # 0x17
    '+',  # 0x18 = CF.LINES_LEFT_0 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_2 | CF.LINES_UP_0
    '+',  # 0x19 = CF.LINES_LEFT_0 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_2 | CF.LINES_UP_1
    _nc,  # 0x1A
    _nc,  # 0x1B
    _nc,  # 0x1C
    _nc,  # 0x1D
    _nc,  # 0x1E
    _nc,  # 0x1F
    '#',  # 0x20 = CF.LINES_LEFT_0 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_0 | CF.LINES_UP_0
    _nc,  # 0x21
    '#',  # 0x22 = CF.LINES_LEFT_0 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_0 | CF.LINES_UP_2
    _nc,  # 0x23
    '#',  # 0x24 = CF.LINES_LEFT_0 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_1 | CF.LINES_UP_0
    _nc,  # 0x25
    '#',  # 0x26 = CF.LINES_LEFT_0 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_1 | CF.LINES_UP_2
    _nc,  # 0x27
    '#',  # 0x28 = CF.LINES_LEFT_0 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_2 | CF.LINES_UP_0
    _nc,  # 0x29
    '#',  # 0x2A = CF.LINES_LEFT_0 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_2 | CF.LINES_UP_2
    _nc,  # 0x2B
    _nc,  # 0x2C
    _nc,  # 0x2D
    _nc,  # 0x2E
    _nc,  # 0x2F
    _nc,  # 0x30
    _nc,  # 0x31
    _nc,  # 0x32
    _nc,  # 0x33
    _nc,  # 0x34
    _nc,  # 0x35
    _nc,  # 0x36
    _nc,  # 0x37
    _nc,  # 0x38
    _nc,  # 0x39
    _nc,  # 0x3A
    _nc,  # 0x3B
    _nc,  # 0x3C
    _nc,  # 0x3D
    _nc,  # 0x3E
    _nc,  # 0x3F
    '-',  # 0x40 = CF.LINES_LEFT_1 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_0 | CF.LINES_UP_0
    '+',  # 0x41 = CF.LINES_LEFT_1 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_0 | CF.LINES_UP_1
    '#',  # 0x42 = CF.LINES_LEFT_1 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_0 | CF.LINES_UP_2
    _nc,  # 0x43
    '-',  # 0x44 = CF.LINES_LEFT_1 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_1 | CF.LINES_UP_0
    '+',  # 0x45 = CF.LINES_LEFT_1 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_1 | CF.LINES_UP_1
    '#',  # 0x46 = CF.LINES_LEFT_1 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_1 | CF.LINES_UP_2
    _nc,  # 0x47
    _nc,  # 0x48
    _nc,  # 0x49
    _nc,  # 0x4A
    _nc,  # 0x4B
    _nc,  # 0x4C
    _nc,  # 0x4D
    _nc,  # 0x4E
    _nc,  # 0x4F
    '+',  # 0x50 = CF.LINES_LEFT_1 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_0 | CF.LINES_UP_0
    '+',  # 0x51 = CF.LINES_LEFT_1 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_0 | CF.LINES_UP_1
    _nc,  # 0x52
    _nc,  # 0x53
    '+',  # 0x54 = CF.LINES_LEFT_1 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_1 | CF.LINES_UP_0
    '+',  # 0x55 = CF.LINES_LEFT_1 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_1 | CF.LINES_UP_1
    _nc,  # 0x56
    _nc,  # 0x57
    _nc,  # 0x58
    _nc,  # 0x59
    _nc,  # 0x5A
    _nc,  # 0x5B
    _nc,  # 0x5C
    _nc,  # 0x5D
    _nc,  # 0x5E
    _nc,  # 0x5F
    '#',  # 0x60 = CF.LINES_LEFT_1 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_0 | CF.LINES_UP_0
    _nc,  # 0x61
    '#',  # 0x62 = CF.LINES_LEFT_1 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_0 | CF.LINES_UP_2
    _nc,  # 0x63
    '#',  # 0x64 = CF.LINES_LEFT_1 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_1 | CF.LINES_UP_0
    _nc,  # 0x65
    '#',  # 0x66 = CF.LINES_LEFT_1 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_1 | CF.LINES_UP_2
    _nc,  # 0x67
    _nc,  # 0x68
    _nc,  # 0x69
    _nc,  # 0x6A
    _nc,  # 0x6B
    _nc,  # 0x6C
    _nc,  # 0x6D
    _nc,  # 0x6E
    _nc,  # 0x6F
    _nc,  # 0x70
    _nc,  # 0x71
    _nc,  # 0x72
    _nc,  # 0x73
    _nc,  # 0x74
    _nc,  # 0x75
    _nc,  # 0x76
    _nc,  # 0x77
    _nc,  # 0x78
    _nc,  # 0x79
    _nc,  # 0x7A
    _nc,  # 0x7B
    _nc,  # 0x7C
    _nc,  # 0x7D
    _nc,  # 0x7E
    _nc,  # 0x7F
    '=',  # 0x80 = CF.LINES_LEFT_2 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_0 | CF.LINES_UP_0
    '+',  # 0x81 = CF.LINES_LEFT_2 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_0 | CF.LINES_UP_1
    '#',  # 0x82 = CF.LINES_LEFT_2 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_0 | CF.LINES_UP_2
    _nc,  # 0x83
    _nc,  # 0x84
    _nc,  # 0x85
    _nc,  # 0x86
    _nc,  # 0x87
    '=',  # 0x88 = CF.LINES_LEFT_2 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_2 | CF.LINES_UP_0
    '+',  # 0x89 = CF.LINES_LEFT_2 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_2 | CF.LINES_UP_1
    '#',  # 0x8A = CF.LINES_LEFT_2 | CF.LINES_DOWN_0 | CF.LINES_RIGHT_2 | CF.LINES_UP_2
    _nc,  # 0x8B
    _nc,  # 0x8C
    _nc,  # 0x8D
    _nc,  # 0x8E
    _nc,  # 0x8F
    '+',  # 0x90 = CF.LINES_LEFT_2 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_0 | CF.LINES_UP_0
    '+',  # 0x91 = CF.LINES_LEFT_2 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_0 | CF.LINES_UP_1
    _nc,  # 0x92
    _nc,  # 0x93
    _nc,  # 0x94
    _nc,  # 0x95
    _nc,  # 0x96
    _nc,  # 0x97
    '+',  # 0x98 = CF.LINES_LEFT_2 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_2 | CF.LINES_UP_0
    '+',  # 0x99 = CF.LINES_LEFT_2 | CF.LINES_DOWN_1 | CF.LINES_RIGHT_2 | CF.LINES_UP_1
    _nc,  # 0x9A
    _nc,  # 0x9B
    _nc,  # 0x9C
    _nc,  # 0x9D
    _nc,  # 0x9E
    _nc,  # 0x9F
    '#',  # 0xA0 = CF.LINES_LEFT_2 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_0 | CF.LINES_UP_0
    _nc,  # 0xA1
    '#',  # 0xA2 = CF.LINES_LEFT_2 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_0 | CF.LINES_UP_2
    _nc,  # 0xA3
    _nc,  # 0xA4
    _nc,  # 0xA5
    _nc,  # 0xA6
    _nc,  # 0xA7
    '#',  # 0xA8 = CF.LINES_LEFT_2 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_2 | CF.LINES_UP_0
    _nc,  # 0xA9
    '#',  # 0xAA = CF.LINES_LEFT_2 | CF.LINES_DOWN_2 | CF.LINES_RIGHT_2 | CF.LINES_UP_2
    _nc,  # 0xAB
    _nc,  # 0xAC
    _nc,  # 0xAD
    _nc,  # 0xAE
    _nc,  # 0xAF
    _nc,  # 0xB0
    _nc,  # 0xB1
    _nc,  # 0xB2
    _nc,  # 0xB3
    _nc,  # 0xB4
    _nc,  # 0xB5
    _nc,  # 0xB6
    _nc,  # 0xB7
    _nc,  # 0xB8
    _nc,  # 0xB9
    _nc,  # 0xBA
    _nc,  # 0xBB
    _nc,  # 0xBC
    _nc,  # 0xBD
    _nc,  # 0xBE
    _nc,  # 0xBF
    _nc,  # 0xC0
    _nc,  # 0xC1
    _nc,  # 0xC2
    _nc,  # 0xC3
    _nc,  # 0xC4
    _nc,  # 0xC5
    _nc,  # 0xC6
    _nc,  # 0xC7
    _nc,  # 0xC8
    _nc,  # 0xC9
    _nc,  # 0xCA
    _nc,  # 0xCB
    _nc,  # 0xCC
    _nc,  # 0xCD
    _nc,  # 0xCE
    _nc,  # 0xCF
    _nc,  # 0xD0
    _nc,  # 0xD1
    _nc,  # 0xD2
    _nc,  # 0xD3
    _nc,  # 0xD4
    _nc,  # 0xD5
    _nc,  # 0xD6
    _nc,  # 0xD7
    _nc,  # 0xD8
    _nc,  # 0xD9
    _nc,  # 0xDA
    _nc,  # 0xDB
    _nc,  # 0xDC
    _nc,  # 0xDD
    _nc,  # 0xDE
    _nc,  # 0xDF
    _nc,  # 0xE0
    _nc,  # 0xE1
    _nc,  # 0xE2
    _nc,  # 0xE3
    _nc,  # 0xE4
    _nc,  # 0xE5
    _nc,  # 0xE6
    _nc,  # 0xE7
    _nc,  # 0xE8
    _nc,  # 0xE9
    _nc,  # 0xEA
    _nc,  # 0xEB
    _nc,  # 0xEC
    _nc,  # 0xED
    _nc,  # 0xEE
    _nc,  # 0xEF
    _nc,  # 0xF0
    _nc,  # 0xF1
    _nc,  # 0xF2
    _nc,  # 0xF3
    _nc,  # 0xF4
    _nc,  # 0xF5
    _nc,  # 0xF6
    _nc,  # 0xF7
    _nc,  # 0xF8
    _nc,  # 0xF9
    _nc,  # 0xFA
    _nc,  # 0xFB
    _nc,  # 0xFC
    _nc,  # 0xFD
    _nc,  # 0xFE
    _nc,  # 0xFF
]

# Pre-allocate array with 256 elements with _nc (middle dot U+00B7) as placeholder.
glst_unicode_box_char_lookup_by_classification = [_nc] * 256

# Populate Unicode look-up array using `gdict_unicode_classification_by_char_ordered`.
for c in gdict_unicode_classification_by_char_ordered:
    mc = c
    if c[0] == 'D':
        mc = c[1]
    classif_idx = gdict_unicode_classification_by_char_ordered[c]
    glst_unicode_box_char_lookup_by_classification[classif_idx] = mc

up_bit_shift_count = Direction.UP    << 1
rt_bit_shift_count = Direction.RIGHT << 1
dn_bit_shift_count = Direction.DOWN  << 1
lf_bit_shift_count = Direction.LEFT  << 1

cfg_view_box_drawing_state_key = '_box_drawing_state'
cfg_view_box_drawing_last_direction_key = '_box_drawing_last_direction'


# =========================================================================
# Data
# =========================================================================

# These will be arbitrarily assigned until we implement ASCII,
# then the configured character set will determine which arrays get
# assigned and this will get updated when Package settings change.
gdict_classification_by_char = gdict_ascii_classification_by_char_ordered
glst_box_char_lookup_by_classification = glst_ascii_box_char_lookup_by_classification


# =========================================================================
# Box-Drawing Character Characterization Utilities
# =========================================================================

def line_count(c: str, side: Direction, debugging: bool) -> int:
    r"""
    Number of lines for character `c` on side `side`.

    Only box-drawing characters can have 1 or 2 lines, and most box-drawing
    characters have 0 lines coming out of at least one of their sides.

    All other characters will be considered to have 0 lines on all sides
    because they are not found in global ``gdict_classification_by_char``.

    ``gdict_classification_by_char`` references a dictionary with the
    box-drawing characters as keys.  Which dictionary it references is
    based on the "character_set" Package setting:  ASCII or Unicode.  The
    integer values contain bit fields that tell us how many lines come out
    of each side of that box-drawing character.  Here is how the bits are
    arranged:

    .. code-block:: text

        +-+-+-+-+-+-+-+-+
        |L|L|b|b|r|r|t|t|
        +-+-+-+-+-+-+-+-+
         \_/ \_/ \_/ \_/
          L   b   r   t

        where:
            t = top side
            r = right side
            b = bottom side
            L = left side

    The unsigned integer in each bit field contains:

    - 0 = 0b00 = no lines
    - 1 = 0b01 = 1 line
    - 2 = 0b10 = 2 lines

    The OR-ed combined value will index into a character-lookup array for fast
    character selection by combining bits from this classification list.

    Note that the ``Direction`` IntEnum class is carefully ordered to so
    that the ``side`` can be used to compute the number of bits to
    right-shift this integer value to place the indicated field into the
    least-significant 2 bits.

        UP    = 0   # 0 << 1 == 0 == number of bits to shift
        RIGHT = 1   # 1 << 1 == 2 == number of bits to shift
        DOWN  = 2   # 2 << 1 == 4 == number of bits to shift
        LEFT  = 3   # 3 << 1 == 6 == number of bits to shift

    :param c:          Character to examine
    :param side:       Which side of character to examine
    :param debugging:  Are we debugging?
    """
    if debugging:
        print('  In line_count()...')
    result = 0

    if c in gdict_classification_by_char:
        classification = gdict_classification_by_char[c]
        right_shift_bit_count = side << 1
        result = (classification >> right_shift_bit_count) & 0x03
        if debugging:
            print(f'    classification=0x{classification:02X}')
            print(f'    {right_shift_bit_count=}')

    if debugging:
        print(f'    {result=}')

    return result


def adjusted_classification(c: str, side: Direction, new_line_count: int, debugging: bool):
    """ Adjusted classification to connect on ``side`` with ``new_line_count``. """
    classification = gdict_classification_by_char[c]
    shift_bit_count = side << 1

    # Remove any old bits.
    mask_out_bits_mask = 0x03 << shift_bit_count
    if debugging:
        print('In adjusted_classification()...')
        print(f'  {c=}')
        print(f'  {side=}')
        print(f'  {new_line_count=}')
        print(f'  Characterization   : 0x{classification:02X}')
        print(f'  {shift_bit_count=}')
        print(f'  Mask-out bits      : 0x{mask_out_bits_mask:02X}')
    classification &= ~mask_out_bits_mask
    if debugging:
        print(f'   Bits masked out   : 0x{classification:02X}')

    # Add new bits.
    new_bit_mask = new_line_count << shift_bit_count
    classification |= new_bit_mask
    if debugging:
        print(f'   New bit field     : 0x{new_bit_mask:02X}')
        print(f'   Adj classification: 0x{classification:02X}')

    return classification


# =========================================================================
# Utilities
# =========================================================================

def ok_to_do_box_drawing(view: sublime.View, debugging: bool) -> bool:
    if debugging:
        print('In ok_to_do_box_drawing()...')

    result = False

    if view.sheet_id() != 0:
        live_sel_list = view.sel()
        sel_rgn = live_sel_list[0]
        view_settings = view.settings()
        drawing_state = view_settings.get(cfg_view_box_drawing_state_key)

        # ---------------------------------------------------------------------
        # - View is attached to a Sheet, not a Panel or Overlay.
        # - State = ON?
        # - Only 1 selection (caret)?
        # - No text selected?
        # ---------------------------------------------------------------------
        result = ((
                    (drawing_state == State.ON)
                and (len(live_sel_list) == 1)
                and (sel_rgn.b - sel_rgn.a == 0)
                ))

        if debugging:
            print(f'  {drawing_state=}')
            print(f'  {len(live_sel_list)=}')
            print(f'  {sel_rgn=}')

    if debugging:
        print(f'  {result=}')

    return result


def timestamp() -> str:
    """ Configured timestamp; used in some Package debug output. """
    now = datetime.now()
    fmt = '%Y-%m-%d %H:%M'
    return now.strftime(fmt)


# =========================================================================
# State Utilities
#
# State (OFF or ON)---per View
#
# Because ``BoxDrawingContextEventListener`` needs to know about this
# state, and because it is a per-view state, and because it will not
# have access to the ``BoxDrawingDrawOneCharacterCommand`` per-view
# object, we keep this state in the View's settings rather than have it
# be in 2 places, eliminating the error-proneness of redundant state
# memory.  This gives access to these values for both the listener and
# the Commands.
# =========================================================================

def is_state_active(view: View) -> bool:
    view_settings = view.settings()
    drawing_state = view_settings.get(cfg_view_box_drawing_state_key)
    return ((drawing_state == State.ON))


def set_state_off(view: View):
    """
    Set box-drawing state OFF in ``view``, but only if View is connected to a Sheet,
    i.e. not part of a Panel or Overlay.
    """
    debugging = is_debugging(DebugBit.COMMANDS | DebugBit.STATE)
    if debugging:
        print('In set_state_on()...')

    if view.sheet_id() != 0:
        view_settings = view.settings()
        view_settings.set(cfg_view_box_drawing_state_key, State.OFF)
        view_settings.set(cfg_view_box_drawing_last_direction_key, Direction.NONE)
        sublime.status_message('BoxDrawing OFF')
        if debugging:
            print(f'  {is_state_active(view)=}')
    else:
        if debugging:
            print('  View is not part of Sheet.  Not setting.')


def set_state_on(view: View):
    """
    Set box-drawing state ON in ``view``, but only if View is connected to a Sheet,
    i.e. not part of a Panel or Overlay.
    """
    debugging = is_debugging(DebugBit.COMMANDS | DebugBit.STATE)
    if debugging:
        print('In set_state_on()...')

    if view.sheet_id() != 0:
        view_settings = view.settings()
        view_settings.set(cfg_view_box_drawing_state_key, State.ON)
        sublime.status_message('BoxDrawing ON')
        if debugging:
            print(f'  {is_state_active(view)=}')
    else:
        if debugging:
            print('  View is not part of Sheet.  Not setting.')


def toggle_state(view: View):
    if is_debugging(DebugBit.COMMANDS | DebugBit.STATE):
        print('In toggle_state()...')

    if is_state_active(view):
        set_state_off(view)
    else:
        set_state_on(view)


# =========================================================================
# Events
# =========================================================================

def _on_pkg_settings_chgd():
    """
    Take action after Package settings have changed.
    """
    # Load overridable Package settings.
    # `bd_setting()` cannot be called until this is done, and
    # `is_debugging()` will return an incorrect value until this is done.
    bd_setting.obj = sublime.load_settings(_cfg_pkg_settings_file)

    # Initialize debugging subsystem.
    temp = bd_setting(_cfg_stg_name__debugging)
    set_debugging_bits(temp)
    debugging = is_debugging(DebugBit.SETTINGS_CHANGED_EVENT)
    if debugging:
        print(f'In _on_pkg_settings_chgd()')

    # Initialize character set data.
    global gdict_classification_by_char
    global glst_box_char_lookup_by_classification
    is_ascii = ((bd_setting(_cfg_stg_name__character_set) == 'ASCII'))
    if is_ascii:
        gdict_classification_by_char = gdict_ascii_classification_by_char_ordered
        glst_box_char_lookup_by_classification = glst_ascii_box_char_lookup_by_classification
        if debugging:
            print('  ASCII mode initialized.')
    else:
        gdict_classification_by_char = gdict_unicode_classification_by_char_ordered
        glst_box_char_lookup_by_classification = glst_unicode_box_char_lookup_by_classification
        if debugging:
            print('  Unicode mode initialized.')


def on_plugin_loaded():
    """
    Initialize plugin; called by Sublime Text after plugin is loaded.
    """
    # Prepare cached Package settings.
    # Anything that relies on Package settings will not work before
    # ``_on_pkg_settings_chgd()`` is called, since it is what loads
    # the Package settings.
    _on_pkg_settings_chgd()
    if is_debugging(DebugBit.SETTINGS_CHANGED_EVENT):
        print(f'In on_plugin_loaded()')

    # Establish event hook for "settings changed" event. This allows the user
    # to change the lists that partake in the content of the RegEx that detects
    # Comment Specifier strings, and have updated behavior immediately after
    # saving the changed configuration. Note:  Callback must be unloaded in
    # `plugin_unloaded()` to prevent a callback leak.
    bd_setting.obj.add_on_change(_cfg_on_settings_chgd_listener_id, _on_pkg_settings_chgd)

    # Report.
    if is_debugging(DebugBit.LOAD_UNLOAD):
        print(f'{package_name}:  Initialized at {timestamp()}.')


def on_plugin_unloaded():
    if hasattr(bd_setting, 'obj'):
        # That test is for when this Plugin is in a state where it generates
        # an exception upon attempting to be loaded by Sublime Text, then
        # the `obj` attribute may not exist.
        if bd_setting.obj:
            bd_setting.obj.clear_on_change(_cfg_on_settings_chgd_listener_id)

    if is_debugging(DebugBit.LOAD_UNLOAD):
        print(f'{package_name}:  Plugin unloaded at {timestamp()}')


"""
--------( LineDraw.sh )---------
/******************************************************************************
                             Multi-Edit Macro File
                               23-Oct-03  16:30

  $Header: /Me91/Sh/LineDraw.sh 4     03-10-24 14:48 Danh $

             Copyright (C) 2002-2003 by Multi Edit Software, Inc.
 *******************************************************************( ldh )***/

prototype LineDraw {
  void LineDrawKey( );
}

global {
  int g_Ld_Direction  "~Ld_Direction";
  int g_Ld_HDlg       "~Ld_HDlg";
  int g_Ld_Stat       "~Ld_Stat";
  int g_Ld_EditWindow "~Ld_EditWindow";
  int g_Ld_MovedPosX  "&Ld_PosX";
  int g_Ld_MovedPosY  "&Ld_PosY";
}



--------( LineDraw.s )---------
macro_file LineDraw;
/******************************************************************************
                             Multi-Edit Macro File

  Function: Macros to Generate linedrawing boxes in the text

  $Header: /Me91/Src/Linedraw.s 20    10/23/03 7:10p Reids $

             Copyright (C) 2002-2003 by Multi Edit Software, Inc.
 ******************************************************************************/

#include Win32.sh
#include Messages.sh

#ifdef _MeSAS_
  #include MeLSLib.sh
#endif

#ifdef _MeLite_
  #include MeLiteLib.sh
#endif

#ifdef _Mew32_
  #include MeLib.sh
#endif

#include Dialog.sh
#include LineDraw.sh

#define wm_LdInit 0x2000




void LineDraw( ) trans
/*******************************************************************************
                                MULTI-EDIT MACRO

Name: LINEDRAW

Description: This macro allows the user to draw the single and double line
characters using the arrow keys to create lines and boxes etc.

             Copyright (C) 2002-2003 by Multi Edit Software, Inc.
*******************************************************************************/
{
  if ( g_Ld_hDlg != 0 ) {
    // don't allow multiple occurances, switch to currently active notebook
    SendMessage( g_Ld_Hdlg, wm_SysCommand, sc_Close, 0 );
    return ( );
  }

/*
Here is a list of all of the linedrawing characters:
³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚ
 */

  struct tRect rect;

 // int main_dlg = Create_Mew_DlgEx ("", WS_POPUP, 1, 1, frame_handle, DLG_NOSIZE | DLG_NOCENTER | DLG_NOPARDISABLE | DLG_MODELESS);
  int main_dlg = Create_Mew_Dlg ("LineDraw", "", frame_handle, DLG_NOSIZE | DLG_NOCENTER | DLG_NOPARDISABLE | DLG_MODELESS);
  int ldb = Create_MEW_Ctrl( "BUTTON", "Single",
                bs_autoradiobutton,
                1, 1, 60, 20,
                main_dlg,101,
                app_handle, 0
              );
  int ldb = Create_MEW_Ctrl( "BUTTON", "Double",
                bs_autoradiobutton,
                61, 1, 60, 20,
                main_dlg,102,
                app_handle, 0
              );
  int ldb = Create_MEW_Ctrl( "BUTTON", "Erase",
                bs_autoradiobutton,
                121, 1, 60, 20,
                main_dlg,103,
                app_handle, 0
              );
  SubClass_With_Macro( main_dlg, "LinedrawProc", "" );


  SendDlgItemMessage(main_dlg, 101, BM_SETCHECK, 1, 0);
  Auto_Size_Mew_Dlg (main_dlg, 100, 100);
  struct tpoint pt;
  if ( g_Ld_MovedPosX || g_Ld_MovedPosY )
  {
    pt.x = g_Ld_MovedPosX;
    pt.y = g_Ld_MovedPosY;
  }
  else
  {
    GetWindowRect (client_handle, &rect);
    pt.x = rect.right;
    pt.y = rect.top;

    GetWindowRect (main_dlg, &rect);
    pt.x -= (rect.right - rect.left) + 1;
    if ( SendMessage(client_handle, WM_MDIGETACTIVE, 0, 0) & 0xFFFF0000)
    {
      pt.x -= GetSystemMetrics(SM_CXVSCROLL) - 1;
    }
  }
  SetWindowPos ( main_dlg, 0, pt.x, pt.y, 0, 0, SWP_NOSIZE | SWP_NOZORDER);
  ShowWindow( main_dlg, sw_shownormal );
  BringWindowToTop( main_dlg );
  PostMessage(main_dlg, WM_LDINIT, 0, 0);

  int blarg, k1, k2;
  str tst, tst1;
  if( Wcmd_Find( 0, global_int('~LD_WCMD_ID'), blarg, k1, k2, tst, tst1)){
    tst = '';
    if ( k2 )
    {
      tst = Make_Key_Name(k2) + '  OR  ';
    }
    tst += Make_Key_Name(k1) + '  to toggle mode.';
    make_message(tst);
  }
}  // LineDraw



int LineDrawProc(
  int &RetVal,
  int Window,
  int Message,
  int WParam,
  int LParam,
  str Parms
  ) trans2 no_break
/******************************************************************************
                               Multi-Edit Macro
                               04-Jan-01  12:40


             Copyright (C) 2002-2003 by Multi Edit Software, Inc.
 *******************************************************************( ldh )***/
{
  int Rv = 0;

  switch ( Message ) {

    case wm_Activate :
    {
      if ( !WParam ) {
        g_Ld_HDlg = Window;
        if ( SendDlgItemMessage( Window, 101, bm_GetCheck, 0, 0 ) ) {
          g_Ld_Stat = 1;
        }
        else if (SendDlgItemMessage( Window, 102, bm_GetCheck, 0, 0 ) ) {
          g_Ld_Stat = 2;
        }
        else if ( SendDlgItemMessage( Window, 103, bm_GetCheck, 0, 0 ) ) {
          g_Ld_Stat = 3;
        }
      }
      else {
        g_Ld_EditWindow = ( LParam & 0x0000FFFF );
      }
      break;
    }

    case wm_Command :
    {
      switch ( WParam ) {

        case  101 :
        case  102 :
        case  103 :
          if ( ( LParam >> 16 ) == bn_Clicked ) {
            SetActiveWindow( g_Ld_EditWindow );
          }
      }
      break;
    }

    case wm_LdInit :
    {
      SetActiveWindow( g_Ld_EditWindow );
      break;
    }

    case wm_Destroy :
    {
      struct TRect Rect;

      GetWindowRect( Window, &Rect );
      g_Ld_MovedPosX = Rect.Left;
      g_Ld_MovedPosY = Rect.Top;
      g_Ld_hDlg = 0;
      g_Ld_Stat = 0;
      Make_Message( "" );
      break;
    }
  }
  RetVal = 0;
  return ( Rv );

}  // LineDrawProc



void LdToggle( ) trans2
/******************************************************************************
                               Multi-Edit Macro
                               04-Jan-01  12:37


             Copyright (C) 2002-2003 by Multi Edit Software, Inc.
 *******************************************************************( ldh )***/
{
  int Jx = g_Ld_Stat;

  if ( Jx ) {
    ++g_Ld_Stat;
    if ( g_Ld_Stat > 3 ) {
      g_Ld_Stat = 1;
    }
    SendDlgItemMessage( g_Ld_hDlg, 100 + Jx, bm_SetCheck, 0, 0 );
    SendDlgItemMessage( g_Ld_hDlg, 100 + g_Ld_Stat, bm_SetCheck, 1, 0 );
    RedrawWindow( g_Ld_hDlg, 0, 0, rdw_Invalidate | rdw_UpdateNow );
  }
}  // LdToggle



void LineDrawKey( ) trans2 no_break
/******************************************************************************
                               Multi-Edit Macro
                               04-Jan-01  12:18


             Copyright (C) 2002-2003 by Multi Edit Software, Inc.
 *
 * Revision History
 * v2.0 28-Aug-2012 09:16 vw  -  Made to work with ANSI characters as opposed
 *                               to OEM characters.  (Windows uses ANSI.)
 *******************************************************************( ldh )***/
{
  int K1 = Key1,
      K2 = Key2,
      Need_Redraw = false,
      A_Left = 1,
      A_Right = 2,
      A_Up = 3,
      A_Down = 4,
      L_Mode,
      R_Mode,
      U_Mode,
      D_Mode,
      Same_Direction = 0,
      Ti = 0,
      OIm = Insert_Mode,
      Tr = Refresh;

  char L_Char;
  char R_Char;
  char U_Char;
  char D_Char;

  int liIsOemMode;                      /* 1 = OEM, 0 = ANSI */

  Insert_Mode = false;


  /*-----------------------------------------------------------------------
   * 28-Aug-2012 09:23 vw  ANSI mode IF block added:  places OEM switch
   * block in the TRUE part of the IF block, and ANSI (new) switch block
   * in the FALSE part of the IF block.
   *-----------------------------------------------------------------------*/
  liIsOemMode = Get_OEM_ANSI(Cur_Window);

  if (liIsOemMode) {
  /*---------------------------------------------------------------------
   * OEM Mode
   *---------------------------------------------------------------------*/
    switch ( K1 ) {

      case vk_Down :
        if ( g_Ld_Stat == 3 ) {
          Text( " " );
          Left;
          Down;
          g_Ld_Direction = 0;
          break;
        }
        Same_Direction = ( g_Ld_Direction == A_Down);
        if (Same_Direction) {
          /* If we were previously going a different direction, then insert char
           at current cusror position. Otherwise, insert char in the next down
           position */
          Down;
        }
        g_Ld_Direction = A_Down;
        call LookAroundOEM;

        Ti = XPos( U_Char, "Ù¾½¼ÀÓÔÈÁÏÊÐ", 1 );
        if ( Ti && Same_Direction ) {
          /* We're going down.  If char above is not connected, then we need to change it to be connected. */
          Up;
          Text( Copy( "´µ´µÃÃÆÆÅØØÅ¹¹¶¹ÌÇÌÌÎÎÎ×",( ( g_Ld_Stat - 1 ) * 12 ) + Ti, 1 ) );
          Left;
          break;
        }
        if ( ( U_Mode > 0 ) && ( ( R_Mode + D_Mode + L_Mode ) == 0 ) ) {
          Text( Copy( "³º", g_Ld_Stat, 1 ) );
          Left;
          break;
        }
        if ( ( L_Mode == 1 ) && ( R_Mode == 1 ) ) {
          Text( Copy( "ÂÒÂÒÒËÂÒÁÊÅÎÁÊÂÒÐÐÂÐ×Î", ( U_Mode * 8 ) + ( D_Mode * 2 ) + g_Ld_Stat, 1 ) );
          Left;
          break;
        }
        if ( ( L_Mode == 2 ) && ( R_Mode == 2 ) ) {
          Text( Copy( "ÑËÑËÑËÑËÏÊØÎÏËÑËÁÊÁÊÅÎ", ( U_Mode * 8 ) + ( D_Mode * 2 ) + g_Ld_Stat, 1 ) );
          Left;
          break;
        }
        if ( L_Mode == 1 ) {
          Text( Copy( "¿·¿·¿·¿·Ù¼´¹Ù¼¿·Ù½¿½´¶", ( U_Mode * 8 ) + ( D_Mode * 2 ) + g_Ld_Stat, 1 ) );
          Left;
          break;
        }
        if ( L_Mode == 2 ) {
          Text( Copy( "¸»¸»¸»¸»¾¼µ¹¾¼¸»¾¼¸¼µ¹", ( U_Mode * 8 ) + ( D_Mode * 2 ) + g_Ld_Stat, 1 ) );
          Left;
          break;
        }
        if ( R_Mode == 2 ) {
          Text( Copy( "ÕÉÕÉÕÉÕÉÔÈÆÌÔÈÕÉÔÈÕÈÆÌ", ( U_Mode * 8 ) + ( D_Mode * 2 ) + g_Ld_Stat, 1 ) );
          Left;
          break;
        }
        if ( R_Mode == 1 ) {
          Text( Copy( "ÚÖÚÖÚÖÚÖÀÈÃÌÀÈÚÖÀÓÚÓÃÇ", ( U_Mode * 8 ) + ( D_Mode * 2 ) + g_Ld_Stat, 1 ) );
          Left;
          break;
        }
        /* If no other condition exists... */
        Text( Copy( "³º", g_Ld_Stat, 1 ) );
        Left;
        break;

      case vk_Right :
        if ( g_Ld_Stat == 3 ) {
          Text( " " );
          g_Ld_Direction = 0;
          break;
        }
        Same_Direction = ( g_Ld_Direction == A_Right );
        if ( Same_Direction ) {
          /* If we were previously going a different direction, then insert char
           at current cusror position. Otherwise, insert char in the next right
           position */
          Right;
        }
        g_Ld_Direction = A_Right;
        call LookAroundOEM;

        Ti = XPos( L_Char, "¿·¸»Ù¾½¼´¶¹µ", 1 );
        if ( Ti && Same_Direction ) {
      /* We're going right.  If char to left is not connected, then we need to change it to be connected. */
          Left;
          Text( Copy( "ÂÒÂÒÁÁÐÐÅ××ÅËËÑËÊÏÊÊÎÎÎØ", ( ( g_Ld_Stat - 1 ) * 12 ) + Ti, 1 ) );
          Left;
          break;
        }
        if ( (L_Mode > 0 ) && ( ( D_Mode + U_Mode + R_Mode ) == 0 ) ) {
          Text( Copy( "ÄÍ", g_Ld_Stat, 1 ) );
          Left;
          break;
        }
        if ( ( D_Mode == 1 ) && ( U_Mode == 1 ) ) {
          Text( Copy( "ÃÆÃÆÆÌÃÆ´¹ÅÎ´¹ÃÆµµµµØÎ", ( L_Mode * 8 ) + ( R_Mode * 2 ) + g_Ld_Stat, 1 ) );
          Left;
          break;
        }
        if ( ( D_Mode == 2 ) && ( U_Mode == 2 ) ) {
          Text( Copy( "ÇÌÇÌÇÌÇÌ¶¹×Î¶ÌÇÌ´¹´¹ÅÎ", ( L_Mode * 8 ) + ( R_Mode * 2 ) + g_Ld_Stat, 1 ) );
          Left;
          break;
        }
        if ( D_Mode == 1 ) {
          Text( Copy( "ÚÕÚÕ¿¸ÚÕ¿»ÂË¿»ÚÕ¿¸Ú¸ÂÑ", ( L_Mode * 8 ) + ( R_Mode * 2 ) + g_Ld_Stat, 1 ) );
          Left;
          break;
        }

        if ( D_Mode == 2 ) {
          Text( Copy( "ÖÉÖÉÖÉÖÉ·»ÒË·»ÖÉ·»Ö»ÒË", ( L_Mode * 8 ) + ( R_Mode * 2 ) + g_Ld_Stat, 1 ) );
          Left;
          break;
        }

        if ( U_Mode == 2 ) {
          Text( Copy( "ÓÈÓÈÓÈÓÈ½¼ÐÊ½¼ÓÈ½¼Ó¼ÐÊ", ( L_Mode * 8 ) + ( R_Mode * 2 ) + g_Ld_Stat, 1 ) );
          Left;
          break;
        }
        if ( U_Mode == 1 ) {
          Text( Copy( "ÀÔÀÔÙ¾ÀÔÙ¼ÁÊÙ¼ÀÔÙ¾À¾ÁÏ", ( L_Mode * 8 ) + ( R_Mode * 2 ) + g_Ld_Stat, 1 ) );
          Left;
          break;
        }
        /* If no other condition exists... */
        Text( Copy( "ÄÍ", g_Ld_Stat, 1 ) );
        Left;
        break;

      case vk_Up :
        if ( g_Ld_Stat == 3 ) {
          Text( " " );
          Left;
          Up;
          g_Ld_Direction = 0;
          break;
        }
        Same_Direction = ( g_Ld_Direction == A_Up );
        if ( Same_Direction ) {
          /* If we were previously going a different direction, then insert char
           at current cusror position. Otherwise, insert char in the next up
           position */
          Up;
        }
        g_Ld_Direction = A_Up;
        call LookAroundOEM;

        Ti = XPos(D_Char,'¿¸·»ÚÖÕÉÂÑËÒ',1);
        if ((Ti) && (Same_Direction)) {
          Down;
          Text(Copy('´µ´µÃÃÆÆÅØØÅ¹¹¶¹ÌÇÌÌÎÎÎ×',((g_Ld_Stat - 1) * 12) + Ti,1));
          LEFT;
          break;
        }

        if(  ((D_Mode > 0) & ((R_Mode + U_Mode + L_Mode) == 0))  ) {
          Text(Copy('³º',g_Ld_Stat,1));
          LEFT;
          break;
        }

        if(  ((L_Mode == 1) & (R_Mode == 1))  ) {
          Text(Copy('ÁÐÂËÒÒÁÐÁÐÅÎÁÒÁÐÐÊÂË×Î',((U_Mode * 8) + (D_Mode * 2)) + g_Ld_Stat,1));
          LEFT;
          break;
        }

        if(  ((L_Mode == 2) & (R_Mode == 2))  ) {
          Text(Copy('ÏÊÑËÂËÏÊÏÊØÎÂËÏÊÏÊÑÊÅÎ',((U_Mode * 8) + (D_Mode * 2)) + g_Ld_Stat,1));
          LEFT;
          break;
        }

        if(  (L_Mode == 1)  ) {
          Text(Copy('Ù½¿»¿·Ù½Ù½´¹Ù·Ù½Ù½¿»´¶',((U_Mode * 8) + (D_Mode * 2)) + g_Ld_Stat,1));
          LEFT;
          break;
        }

        if(  (L_Mode == 2)  ) {
          Text(Copy('¾¼¸»¸»¾¼¾¼µ¹¾»¾¼¾¼¸»µ¹',((U_Mode * 8) + (D_Mode * 2)) + g_Ld_Stat,1));
          LEFT;
          break;
        }

        if(  (R_Mode == 2)  ) {
          Text(Copy('ÔÈÕÉÕÉÔÈÔÈÆÌÔÉÔÈÔÈÕÉÆÌ',((U_Mode * 8) + (D_Mode * 2)) + g_Ld_Stat,1));
          LEFT;
          break;
        }

        if(  (R_Mode == 1)  ) {
          Text(Copy('ÀÓÚÉÚÖÀÓÀÓÃÌÀÖÀÓÀÓÚÉÃÇ',((U_Mode * 8) + (D_Mode * 2)) + g_Ld_Stat,1));
          LEFT;
          break;
        }

        /* If no other condition exists... */
        Text(Copy('³º',g_Ld_Stat,1));
        LEFT;
        break;

      case vk_Left :
        if(  (g_Ld_Stat == 3)  ) {
          Text(' ');
          Left;
          Left;
          g_Ld_Direction = 0;
          break;
        }
        Same_Direction = (g_Ld_Direction == A_Left);
        if (Same_Direction) {
          /* If we were previously going a different direction, then insert char
           at current cusror position. Otherwise, insert char in the next left
           position */
          Left;
        }
        g_Ld_Direction = A_Left;
        call LookAroundOEM;

        Ti = XPos( R_Char, "ÚÖÕÉÀÔÓÈÃÇÌÆ", 1 );
        if ( Ti && Same_Direction ) {
          Right;
          Text( Copy( "ÂÒÂÒÁÁÐÐÅ××ÅËËÑËÊÏÊÊÎÎÎØ", ( ( g_Ld_Stat - 1 ) * 12 ) + Ti, 1 ) );
          Left;
          break;
        }
        if ( (R_Mode > 0 ) && ( ( D_Mode + U_Mode + L_Mode ) == 0 ) ) {
          Text( Copy( "ÄÍ", g_Ld_Stat, 1 ) );
          Left;
          break;
        }
        if ( ( D_Mode == 1 ) && ( U_Mode == 1 ) ) {
          Text( Copy( "´µÃÌÆÆ´µ´µÅÎ´Æ´µµ¹ÃÌØÎ", ( L_Mode * 8 ) + ( R_Mode * 2 ) + g_Ld_Stat, 1 ) );
          Left;
          break;
        }
        if(  ((D_Mode == 2) & (U_Mode == 2))  ) {
          Text(Copy('¶¹ÇÌÃÌ¶¹¶¹×ÎÃÌ¶¹¶¹Ç¹ÅÎ',((L_Mode * 8) + (R_Mode * 2)) + g_Ld_Stat,1));
          Left;
          break;
        }
        if(  (D_Mode == 1)  ) {
          Text(Copy('¿¸ÚÉÚÕ¿¸¿¸ÂË¿Õ¿¸ÚÕÚÉÂÑ',((L_Mode * 8) + (R_Mode * 2)) + g_Ld_Stat,1));
          Left;
          break;
        }
        if ( D_Mode == 2 ) {
          Text(Copy('·»ÖÉÖÉ·»·»ÒË·É·»·»ÖÉÒË',((L_Mode * 8) + (R_Mode * 2)) + g_Ld_Stat,1));
          Left;
          break;
        }
        if ( U_Mode == 2 ) {
          Text(Copy('½¼ÓÈÓÈ½¼½¼ÐÊ½È½¼½¼ÓÈÐÊ',((L_Mode * 8) + (R_Mode * 2)) + g_Ld_Stat,1));
          Left;
          break;
        }
        if ( U_Mode == 1 ) {
          Text(Copy('Ù¾ÀÈÀÔÙ¾Ù¾ÁÊÙÔÙ¾Ù¾ÀÈÁÏ',((L_Mode * 8) + (R_Mode * 2)) + g_Ld_Stat,1));
          Left;
          break;
        }
        /* If no other condition exists... */
        Text( Copy( "ÄÍ", g_Ld_Stat, 1 ) );
        Left;
        break;
    }
  } else {
    /*---------------------------------------------------------------------
     * ANSI Mode
     *---------------------------------------------------------------------*/
    /*
    Here is a list of all of the linedrawing characters:
    ³ ´ µ ¶ · ¸ ¹ º » ¼ ½ ¾ ¿ À Á Â Ã Ä Å Æ Ç È É Ê Ë Ì Í Î Ï Ð Ñ Ò Ó Ô Õ Ö × Ø Ù Ú
     *
     * Plan:
     * Part of the problem is in ANSI, we HAVE line-draw characters, but the are
     * unfortunately in different positions in the character map, and are so high
     * up (e.g. Courier New font has them in the Unicode 0x2052 (9700) range.
     * While it would be great to just do a 1-to-1 substituion, since the compilers
     * don't choke on this, the EDITORS (both Multi-edit and MPLAB IDE) don't know
     * what to do with this code range.  So we're going to have to substitute regular
     * type-able characters instead.  This will look okay in both OEM and ANSI
     * editor fonts.
     *
     * To do this, we need to establish a policy about what to do for vertical and
     * horizontal line meetings, and note that the results are going to be more crude
     * than the original (beautiful) OEM line-draw characters.  Thus, the policy is
     * set here:
     *
     * 1. Non-intersecting lines:
     *    a.  Single vertical line replaced by '|'.
     *    b.  Single horizontal line replaced by '-'.
     *    c.  Clean double-vertical line replaced by '#'
     *    d.  Clean double-horizontal line replaced by '='.
     * 2. Intersecting lines:
     *    a.  Clean single-line intersection of all types replaced by '+'.
     *    b.  All others (with at least one double-line in it) replaced by '#'.
     *    c.  Exceptions to 2.b above:
     *      1)  Double-horizontal-single-vertical (whether only up-side, down-side or both, and corners as well)
     *            |
     *         ===+===
     *            |
     *
     * OEM => ANSI
     * ³      |
     * ´      +
     * µ      +
     * ¶      #
     * ·      #
     * ¸      +
     * ¹      #
     * º      #
     * »      #
     * ¼      #
     * ½      #
     * ¾      +
     * ¿      +
     * À      +
     * Á      +
     * Â      +
     * Ã      +
     * Ä      -
     * Å      +
     * Æ      +
     * Ç      #
     * È      #
     * É      #
     * Ê      #
     * Ë      #
     * Ì      #
     * Í      =
     * Î      #
     * Ï      +
     * Ð      #
     * Ñ      +
     * Ò      #
     * Ó      #
     * Ô      +
     * Õ      +
     * Ö      #
     * ×      #         |
     * Ø      +      ===+===
     * Ù      +
     * Ú      +
     *
     * List of chars we are using:  | - + = #
     */
    switch ( K1 ) {


      case vk_Down :
        if ( g_Ld_Stat == 3 ) {
          Text( " " );
          Left;
          Down;
          g_Ld_Direction = 0;
          break;
        }
        Same_Direction = ( g_Ld_Direction == A_Down);
        if (Same_Direction) {
          /* If we were previously going a different direction, then insert char
           at current cusror position. Otherwise, insert char in the next down
           position */
          Down;
        }
        g_Ld_Direction = A_Down;
        call LookAroundANSI;

        /* List of chars we are using:  | - + = # */

        Ti = XPos( U_Char, "-=", 1 );
        if ( Ti && Same_Direction ) {
          /* We're going down.  If char above is not connected, then we need to change it to be connected. */
          /* g_Ld_Stat = which radio button is selected?  1=single, 2=double, 3=erase.
           * Since we are drawing a VERTICAL line (which has priority over horizontal lines) priority is
           * given to the line draw mode as to which connecting character we use. */
          Up;
          Text( Copy( "+#", g_Ld_Stat, 1 ) );
          Left;
          break;
        }
        if ( ( U_Mode > 0 ) && ( ( R_Mode + D_Mode + L_Mode ) == 0 ) ) {
          Text( Copy( "|#", g_Ld_Stat, 1 ) );
          Left;
          break;
        }
        /* Since we are drawing a vertical line, if we are drawing a DOUBLE-vertical line, the only choice is '#'.
         * If we are drawing a SINGLE-vertical line, then we NEVER draw a '#', but only '|' except if either
         * a SINGLE- or DOUBLE-horizontal line is on either side, then we draw a '+'. */
        if (g_Ld_Stat == 2) {
          Text( '#' );
          Left;
          break;
        } else {
          /* If any type of line-draw char is on left or right, then '+'. */
          if ( (L_Mode > 0) || (R_Mode > 0) ) {
            Text( '+' );
            Left;
            break;
          }
        }
        /* If no other condition exists... */
        Text( Copy( "|#", g_Ld_Stat, 1 ) );
        Left;
        break;


      case vk_Right :
        if ( g_Ld_Stat == 3 ) {
          Text( " " );
          g_Ld_Direction = 0;
          break;
        }
        Same_Direction = ( g_Ld_Direction == A_Right );
        if ( Same_Direction ) {
          /* If we were previously going a different direction, then insert char
           at current cusror position. Otherwise, insert char in the next right
           position */
          Right;
        }
        g_Ld_Direction = A_Right;
        call LookAroundANSI;

        /* List of chars we are using:  | - + = # */

        Ti = XPos( L_Char, "|", 1 );
        if ( Ti && Same_Direction ) {
        /* We're going right.  If char to left is not connected, then we need to change it to be connected.
         * The sole choice here is a '+' since we assume L_Char is connected to a single-vertical line. */
          Left;
          Text( '+' );
          Left;
          break;
        }
        if ( (L_Mode > 0 ) && ( ( D_Mode + U_Mode + R_Mode ) == 0 ) ) {
          /* Line-draw char on left, but nowhere else. Priority is given to draw mode (single or double). */
          Text( Copy( "-=", g_Ld_Stat, 1 ) );
          Left;
          break;
        }
        /* If there is a single-vertical line above or below us, then this is given priority over any
         * double-vertical line, and the only choice is a '+'.  Otherwise, if there is a double-vertical
         * on EITHER side, then meet it with a '#'. */
        if ( ( D_Mode == 1 ) || ( U_Mode == 1 ) ) {
          /* Single-vertical either above or below or both.  Priority is given to single-vertical line.  Only choice is '+'. */
          Text( '+' );
          Left;
          break;
        } else {
          if ((D_Mode == 2) || (U_Mode == 2)) {
            /* Double-vertical either above or below or both.  Meet it with a '#'. */
            Text( '#' );
            Left;
            break;
          }
        }
        /* If no other condition exists... */
        Text( Copy( "-=", g_Ld_Stat, 1 ) );
        Left;
        break;


      case vk_Up :
        if ( g_Ld_Stat == 3 ) {
          Text( " " );
          Left;
          Up;
          g_Ld_Direction = 0;
          break;
        }
        Same_Direction = ( g_Ld_Direction == A_Up );
        if ( Same_Direction ) {
          /* If we were previously going a different direction, then insert char
           at current cusror position. Otherwise, insert char in the next up
           position */
          Up;
        }
        g_Ld_Direction = A_Up;
        call LookAroundANSI;

    /* List of chars we are using:  | - + = # */

        Ti = XPos( D_Char, "-=", 1 );
        if ( Ti && Same_Direction ) {
          /* We're going up.  If char below is not connected, then we need to change it to be connected. */
          /* g_Ld_Stat = which radio button is selected?  1=single, 2=double, 3=erase.
           * Since we are drawing a VERTICAL line (which has priority over horizontal lines) priority is
           * given to the line draw mode as to which connecting character we use. */
          Down;                         /* Go back to not-connected char behind us. */
          Text( Copy( "+#", g_Ld_Stat, 1 ) );
          Left;
          break;
        }
        if ( ( D_Mode > 0 ) && ( ( R_Mode + U_Mode + L_Mode ) == 0 ) ) {
          /* Char behind us is a line-draw char, but no others around, then just draw the vertical line per the mode. */
          Text( Copy( "|#", g_Ld_Stat, 1 ) );
          Left;
          break;
        }
        /* Since we are drawing a vertical line, if we are drawing a DOUBLE-vertical line, the only choice is '#'.
         * If we are drawing a SINGLE-vertical line, then we NEVER draw a '#', but only '|' except if either
         * a SINGLE- or DOUBLE-horizontal line is on either side, then we draw a '+'. */
        if (g_Ld_Stat == 2) {
          Text( '#' );
          Left;
          break;
        } else {
          /* If any type of line-draw char is on left or right, then '+'. */
          if ( (L_Mode > 0) || (R_Mode > 0) ) {
            Text( '+' );
            Left;
            break;
          }
        }
        /* If no other condition exists... */
        Text( Copy( "|#", g_Ld_Stat, 1 ) );
        Left;
        break;


      case vk_Left :
        if(  (g_Ld_Stat == 3)  ) {
          Text(' ');
          Left;
          Left;
          g_Ld_Direction = 0;
          break;
        }
        Same_Direction = (g_Ld_Direction == A_Left);
        if (Same_Direction) {
          /* If we were previously going a different direction, then insert char
           at current cusror position. Otherwise, insert char in the next left
           position */
          Left;
        }
        g_Ld_Direction = A_Left;
        call LookAroundANSI;

        /* List of chars we are using:  | - + = # */

        Ti = XPos( R_Char, "|", 1 );
        if ( Ti && Same_Direction ) {
          /* We're going Left.  If char to right is not connected, then we need to change it to be connected.
           * The sole choice here is a '+' since we assume R_Char is connected to a single-vertical line. */
          Right;
          Text( '+' );
          Left;
          break;
        }
        if ( (R_Mode > 0 ) && ( ( D_Mode + U_Mode + L_Mode ) == 0 ) ) {
          /* Line-draw char on right, but nowhere else. Priority is given to draw mode (single or double). */
          Text( Copy( "-=", g_Ld_Stat, 1 ) );
          Left;
          break;
        }
        /* If there is a single-vertical line above or below us, then this is given priority over any
         * double-vertical line, and the only choice is a '+'.  Otherwise, if there is a double-vertical
         * on EITHER side, then meet it with a '#'. */
        if ( ( D_Mode == 1 ) || ( U_Mode == 1 ) ) {
          /* Single-vertical either above or below or both.  Priority is given to single-vertical line.  Only choice is '+'. */
          Text( '+' );
          Left;
          break;
        } else {
          if ( (D_Mode == 2) || (U_Mode == 2) ) {
            /* Double-vertical either above or below or both.  Meet it with a '#'. */
            Text( '#' );
            Left;
            break;
          }
        }
        /* If no other condition exists... */
        Text( Copy( "-=", g_Ld_Stat, 1 ) );
        Left;
        break;
    }
  }


  Insert_Mode = OIm;
  return ( );


LookAroundOEM:
  /*  This subroutine looks at all chars surrounding CUR_CHAR and stores
   special values into variables based on what it finds  */

  Undo_Stat = false;
  Refresh = false;
  HideCaret( Window_Handle );

  if ( C_Line > 1 ) {
    Up;
    U_Char = Cur_Char;
    Right;
    Down;
  }
  else {
    U_Char = '|0';
    Right;
  }
  R_Char = Cur_Char;
  Down;
  Left;
  D_Char = Cur_Char;
  if ( C_Col > 1 ) {
    Left;
    Up;
    L_Char = Cur_Char;
    Right;
  }
  else {
    L_Char = '|0';
    Up;
  }
  D_Mode = XPos( D_Char, "³´µ¾ÀÁÃÅÆÔØÙÏ¶¹º¼½ÇÈÊÌÎÐÓ×", 1 );
  /*                                   ^ 14th char */
  D_Mode = ( D_Mode > 0 ) + ( D_Mode > 13 );
  /* D_Mode: 0=not a line-draw char, 1=single-vertical line involved, 2=double-vertical line involved. */

  U_Mode = XPos( U_Char, "³´µ¸¿ÂÃÅÆÑÕØÚ¶·¹º»ÇÉËÌÎÒÖ×", 1 );
  U_Mode = ( U_Mode > 0 ) + ( U_Mode > 13 );
  /* U_Mode: 0=not a line-draw char, 1=single-vertical line involved, 2=double-vertical line involved. */

  L_Mode = XPos( L_Char, "ÀÁÂÃÄÅÇÐÒÓÖ×ÚÆÈÉÊËÌÍÎÏÑÔÕØ", 1 );
  L_Mode = ( L_Mode > 0 ) + ( L_Mode > 13 );
  /* L_Mode: 0=not a line-draw char, 1=single-horizontal line involved, 2=double-horozontal line involved. */

  R_Mode = XPos( R_Char, "´¶·½¿ÁÂÄÅÐÒ×Ùµ¸¹»¼¾ÊËÍÎÏÑØ", 1 );
  R_Mode = ( R_Mode > 0 ) + ( R_Mode > 13 );
  /* R_Mode: 0=not a line-draw char, 1=single-horizontal line involved, 2=double-horozontal line involved. */


  ShowCaret( Window_Handle );
  Refresh = true;
  Undo_Stat = true;
  ret;




/*-------------------------------------------------------------------------
 * 28-Aug-2012 09:21 vw  ADDED FOR ANSI MODE
 *-------------------------------------------------------------------------*/
LookAroundANSI:
  /*  This subroutine looks at all chars surrounding CUR_CHAR and stores
   special values into variables based on what it finds  */

  Undo_Stat = false;
  Refresh = false;
  HideCaret( Window_Handle );

  if ( C_Line > 1 ) {
    Up;
    U_Char = Cur_Char;
    Right;
    Down;
  }
  else {
    U_Char = '|0';
    Right;
  }
  R_Char = Cur_Char;
  Down;
  Left;
  D_Char = Cur_Char;
  if ( C_Col > 1 ) {
    Left;
    Up;
    L_Char = Cur_Char;
    Right;
  }
  else {
    L_Char = '|0';
    Up;
  }

  D_Mode = XPos( D_Char, "|+#", 1 );
  D_Mode = ( D_Mode > 0 ) + ( D_Mode > 2 );
  /* D_Mode: 0=not a line-draw char, 1=single-vertical line involved, 2=double-vertical line involved. */

  U_Mode = XPos( U_Char, "|+#", 1 );
  U_Mode = ( U_Mode > 0 ) + ( U_Mode > 2 );
  /* U_Mode: 0=not a line-draw char, 1=single-vertical line involved, 2=double-vertical line involved. */

  L_Mode = XPos( L_Char, "+-#=", 1 );
  L_Mode = ( L_Mode > 0 ) + ( L_Mode > 2 );
  /* L_Mode: 0=not a line-draw char, 1=single-horizontal line involved, 2=double-horozontal line involved. */

  R_Mode = XPos( R_Char, "+-#=", 1 );
  R_Mode = ( R_Mode > 0 ) + ( R_Mode > 2 );
  /* R_Mode: 0=not a line-draw char, 1=single-horizontal line involved, 2=double-horozontal line involved. */


  ShowCaret( Window_Handle );
  Refresh = true;
  Undo_Stat = true;
  ret;


}  // LineDrawKey

"""