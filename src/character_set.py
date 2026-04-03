"""
Box Character Set
=================

This logic pertains to box-character drawing logic, and its ability to become
"attached" to different character sets, namely:

- ASCII
- Unicode [Square Corners]
- Unicode [Round Corners]
- Unicode [2 Dashes]
- Unicode [3 Dashes]
- Unicode [4 Dashes]
- Shadow Characters

By design, this module knows nothing about Sublime Text, Views, View settings, etc..
Only these sets of characters and their characteristics (classifications).


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

- rounded corners (single-line only):
    - ╭ ╮ ╰ ╯

- dashed:
    - 2 dashes vertical  :  ╎
    - 2 dashes horizontal:  ╌
    - 3 dashes vertical  :  ┆
    - 3 dashes horizontal:  ┄
    - 4 dashes vertical  :  ┊
    - 4 dashes horizontal:  ┈

- shadow characters:
    - ░
    - ▒
    - ▓


Examples:
~~~~~~~~~

┌─┬┐  ╔═╦╗  ╓─╥╖  ╒═╤╕    +------------+----------------+
│ ││  ║ ║║  ║ ║║  │ ││    | Column One | Column Two     |
├─┼┤  ╠═╬╣  ╟─╫╢  ╞═╪╡    +============+================+
└─┴┘  ╚═╩╝  ╙─╨╜  ╘═╧╛    |            |                |
╭───────────────────╮     +------------+----------------+
│  ╔═══╗ Some Text  │     |            |                |
│  ╚═╦═╝ in the box │░    +------------+----------------+
╞═╤══╩══╤═══════════╡░    |            |                |
│ ├──┬──┤           │░    +------------+----------------+
│ └──┴──┘           │░    |            |                |
╰───────────────────╯░    +------------+----------------+
  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░


Character Classification
========================

See docstring in ``line_count()`` function below.


Checklist to Add a New Character Set
====================================

1.  Modify list in comments above.

2.  Build and append new character set to `_g_character_sets` in the
    correct sequence.

    a.  Create character set classification dictionary:
        _temp_dict = {
            '╰': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x05
            '╙': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_2,  # 0x06
            '╘': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_1,  # 0x09
            ...
        }

    b.  Generate lookup array:
        _temp_array = _generated_lookup_array(_temp_dict)

    c.  Append to `_g_character_sets` as new CharacterSet:
        _name = 'Unicode [Round Corners]'
        _g_character_sets.append(CharacterSet(_name, _temp_array))

    d.  Update `_combined_classification_dict` with unique characters from
        dictionary created in (2.a.).
        _temp_dict = {
            '╰': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x05
            '╭': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x14
            '╯': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x41
            '╮': CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_0,  # 0x50
        }
        _combined_classification_dict.update(_temp_dict)

3.  Modify `CharacterSetID` enumeration class.
    - Add enumeration name and value to match new sequence.
    - Ensure LAST enumeration contains value of new last value.
    - Ensure COUNT enumeration contains value == LAST + 1.

4.  Modify `BoxDrawing.sublime-settings`:
    - documentation of `CharacterSetID` class (lists valid values);
    - `default_character_set_id` setting integer to match whatever
      integer is now associated with ASCII.

5.  Open the console window ([Ctrl-`])

6.  Reload the Package (can be done by saving `boxdrawing.py`).
    Observe in the Console Panel that there are no error messages.

7.  Test by turning ON and OFF Box Drawing and use key binding to
    progress through new list of character sets.  Check status bar and
    `Tools > BoxDrawing` submenu to ensure the names are as intended.

8.  Test actual drawing to confirm things are coming out as intended.
    Fix if not.
"""
from enum import IntFlag, IntEnum
from typing import List, Dict
from ..lib.debug import DebugBit, is_debugging


# =========================================================================
# Classes
# =========================================================================

class ClassificationBit(IntFlag):
    r"""
    Character Classification Bits
    =============================

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

    The unsigned integer in each bit field contains the count of lines for
    each character in the classification dictionary:

    - 0 = no lines
    - 1 = 1 line
    - 2 = 2 lines

    The OR-ed combined values of the 4 bit fields index into a
    character-lookup array for fast character look-up.
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
# below, to make the two classification dictionaries below more readable.
CB = ClassificationBit


class Direction(IntEnum):
    """
    DrawingDirection Enumeration

    Classification mentioned in comments is from ``ClassificationBit`` class above.
    """
    NONE  = -1  # Used after Package load, turning box-drawing off,
                #   and after an ERASE, to detect "change of direction".
    UP    = 0   # val * 2 = bit-shift right to isolate classification in 2 LSbs.
    RIGHT = 1   # val * 2 = bit-shift right to isolate classification in 2 LSbs.
    DOWN  = 2   # val * 2 = bit-shift right to isolate classification in 2 LSbs.
    LEFT  = 3   # val * 2 = bit-shift right to isolate classification in 2 LSbs.


class CharacterSet:
    """
    A CharacterSet knows:
    - its name
    - its classification dictionary
    - its lookup array (by classification)
    """
    __slots__ = ['name', 'classification_dict', 'lookup_array']

    def __init__(self, name, classification_dict, lookup_array):
        self.name                = name
        self.classification_dict = classification_dict
        self.lookup_array        = lookup_array


class CharacterSetID(IntEnum):
    """
    DrawingDirection Enumeration

    Classification mentioned in comments is from ``ClassificationBit`` class above.

    Maintenance Note:  when this class changes, also change the
    documentation in ``BoxDrawing.sublime-settings``.
    """
    UNICODE_SQUARE_CORNERS = 0
    UNICODE_ROUND_CORNERS  = 1
    UNICODE_2_DASHES       = 2
    UNICODE_3_DASHES       = 3
    UNICODE_4_DASHES       = 4
    UNICODE_SHADOW         = 5
    ASCII                  = 6
    LAST                   = 6


# =========================================================================
# Configuration
# =========================================================================

# Neutral character in look-up arrays.
_cfg_neutral_character = '·'
# Abbreviation to make the various look-up arrays more readable.
_nc = _cfg_neutral_character

# Initial character set.
_cfg_initial_character_set_id: CharacterSetID = CharacterSetID.ASCII


# =========================================================================
# Constants
# =========================================================================

_g_character_sets: List[CharacterSet] = []


def _generated_lookup_array(classification_dict: Dict[str, int]) -> List[str]:
    """
    Populate square-corner Unicode look-up array using `classification_dict`.
    """
    # Pre-allocate look-up array with 256 elements with
    # _nc (middle dot U+00B7) as placeholder.
    result = [_nc] * 256

    for c in classification_dict:
        classif_idx = classification_dict[c]
        result[classif_idx] = c

    return result


# -------------------------------------------------------------------------
# Classifications by Box-Drawing Character
#
# Note that not all bit combinations are represented.  Some bit-field
# combinations do not appear in the Unicode box-drawing character set,
# so they are not represented below.  Such combinations are caught within
# the box-drawing logic before they are used.  Also, many fonts only have
# a subset of the full set of Unicode box-drawing characters (including
# Sublime Text) so only the normally-supported character set is used.
#
# Columns are in bit order left-to-right (most-significant to least):
#       LEFT   BOTTOM   RIGHT   TOP
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# Unicode (Square Corners)
# -------------------------------------------------------------------------
_temp_dict = {
    '└': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x05
    '╙': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_2,  # 0x06
    '╘': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_1,  # 0x09
    '╚': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_2,  # 0x0A
    '│': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x11
    '┌': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x14
    '├': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x15
    '╒': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0x18
    '╞': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_1,  # 0x19
    '║': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0x22
    '╓': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x24
    '╟': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_2,  # 0x26
    '╔': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0x28
    '╠': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_2,  # 0x2A
    '┘': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x41
    '╜': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0x42
    '─': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x44
    '┴': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x45
    '╨': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_2,  # 0x46
    '┐': CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_0,  # 0x50
    '┤': CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x51
    '┬': CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x54
    '┼': CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x55
    '╖': CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_0,  # 0x60
    '╢': CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0x62
    '╥': CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x64
    '╫': CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_2,  # 0x66
    '╛': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x81
    '╝': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0x82
    '═': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0x88
    '╧': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_1,  # 0x89
    '╩': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_2,  # 0x8A
    '╕': CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_0,  # 0x90
    '╡': CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x91
    '╤': CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0x98
    '╪': CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_1,  # 0x99
    '╗': CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_0,  # 0xA0
    '╣': CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0xA2
    '╦': CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0xA8
    '╬': CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_2,  # 0xAA
}

_name = 'Unicode [Square Corners]'
_temp_array = _generated_lookup_array(_temp_dict)
_g_character_sets.append(CharacterSet(_name, _temp_dict, _temp_array))

# -------------------------------------------------------------------------
# Unicode (Round Corners)
# -------------------------------------------------------------------------
_temp_dict = {
    '╰': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x05
    '╙': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_2,  # 0x06
    '╘': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_1,  # 0x09
    '╚': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_2,  # 0x0A
    '│': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x11
    '╭': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x14
    '├': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x15
    '╒': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0x18
    '╞': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_1,  # 0x19
    '║': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0x22
    '╓': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x24
    '╟': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_2,  # 0x26
    '╔': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0x28
    '╠': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_2,  # 0x2A
    '╯': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x41
    '╜': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0x42
    '─': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x44
    '┴': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x45
    '╨': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_2,  # 0x46
    '╮': CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_0,  # 0x50
    '┤': CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x51
    '┬': CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x54
    '┼': CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x55
    '╖': CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_0,  # 0x60
    '╢': CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0x62
    '╥': CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x64
    '╫': CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_2,  # 0x66
    '╛': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x81
    '╝': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0x82
    '═': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0x88
    '╧': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_1,  # 0x89
    '╩': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_2,  # 0x8A
    '╕': CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_0,  # 0x90
    '╡': CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x91
    '╤': CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0x98
    '╪': CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_1,  # 0x99
    '╗': CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_0,  # 0xA0
    '╣': CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0xA2
    '╦': CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0xA8
    '╬': CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_2,  # 0xAA
}

_name = 'Unicode [Round Corners]'
_temp_array = _generated_lookup_array(_temp_dict)
_g_character_sets.append(CharacterSet(_name, _temp_dict, _temp_array))

# -------------------------------------------------------------------------
# Unicode (2 Dashes)
# -------------------------------------------------------------------------
_temp_dict = {
    '└': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x05
    '╙': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_2,  # 0x06
    '╘': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_1,  # 0x09
    '╚': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_2,  # 0x0A
    '╎': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x11
    '┌': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x14
    '├': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x15
    '╒': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0x18
    '╞': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_1,  # 0x19
    '║': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0x22
    '╓': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x24
    '╟': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_2,  # 0x26
    '╔': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0x28
    '╠': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_2,  # 0x2A
    '┘': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x41
    '╜': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0x42
    '╌': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x44
    '┴': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x45
    '╨': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_2,  # 0x46
    '┐': CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_0,  # 0x50
    '┤': CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x51
    '┬': CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x54
    '┼': CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x55
    '╖': CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_0,  # 0x60
    '╢': CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0x62
    '╥': CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x64
    '╫': CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_2,  # 0x66
    '╛': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x81
    '╝': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0x82
    '═': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0x88
    '╧': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_1,  # 0x89
    '╩': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_2,  # 0x8A
    '╕': CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_0,  # 0x90
    '╡': CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x91
    '╤': CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0x98
    '╪': CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_1,  # 0x99
    '╗': CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_0,  # 0xA0
    '╣': CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0xA2
    '╦': CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0xA8
    '╬': CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_2,  # 0xAA
}

_name = 'Unicode [2 Dashes]'
_temp_array = _generated_lookup_array(_temp_dict)
_g_character_sets.append(CharacterSet(_name, _temp_dict, _temp_array))

# -------------------------------------------------------------------------
# Unicode (3 Dashes)
# -------------------------------------------------------------------------
_temp_dict = {
    '└': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x05
    '╙': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_2,  # 0x06
    '╘': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_1,  # 0x09
    '╚': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_2,  # 0x0A
    '┆': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x11
    '┌': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x14
    '├': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x15
    '╒': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0x18
    '╞': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_1,  # 0x19
    '║': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0x22
    '╓': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x24
    '╟': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_2,  # 0x26
    '╔': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0x28
    '╠': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_2,  # 0x2A
    '┘': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x41
    '╜': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0x42
    '┄': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x44
    '┴': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x45
    '╨': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_2,  # 0x46
    '┐': CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_0,  # 0x50
    '┤': CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x51
    '┬': CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x54
    '┼': CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x55
    '╖': CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_0,  # 0x60
    '╢': CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0x62
    '╥': CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x64
    '╫': CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_2,  # 0x66
    '╛': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x81
    '╝': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0x82
    '═': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0x88
    '╧': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_1,  # 0x89
    '╩': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_2,  # 0x8A
    '╕': CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_0,  # 0x90
    '╡': CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x91
    '╤': CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0x98
    '╪': CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_1,  # 0x99
    '╗': CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_0,  # 0xA0
    '╣': CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0xA2
    '╦': CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0xA8
    '╬': CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_2,  # 0xAA
}

_name = 'Unicode [3 Dashes]'
_temp_array = _generated_lookup_array(_temp_dict)
_g_character_sets.append(CharacterSet(_name, _temp_dict, _temp_array))

# -------------------------------------------------------------------------
# Unicode (4 Dashes)
# -------------------------------------------------------------------------
_temp_dict = {
    '└': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x05
    '╙': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_2,  # 0x06
    '╘': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_1,  # 0x09
    '╚': CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_2,  # 0x0A
    '┊': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x11
    '┌': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x14
    '├': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x15
    '╒': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0x18
    '╞': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_1,  # 0x19
    '║': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0x22
    '╓': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x24
    '╟': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_2,  # 0x26
    '╔': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0x28
    '╠': CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_2,  # 0x2A
    '┘': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x41
    '╜': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0x42
    '┈': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x44
    '┴': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x45
    '╨': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_2,  # 0x46
    '┐': CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_0,  # 0x50
    '┤': CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x51
    '┬': CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x54
    '┼': CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x55
    '╖': CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_0,  # 0x60
    '╢': CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0x62
    '╥': CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x64
    '╫': CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_2,  # 0x66
    '╛': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x81
    '╝': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0x82
    '═': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0x88
    '╧': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_1,  # 0x89
    '╩': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_2,  # 0x8A
    '╕': CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_0,  # 0x90
    '╡': CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x91
    '╤': CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0x98
    '╪': CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_1,  # 0x99
    '╗': CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_0,  # 0xA0
    '╣': CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_2,  # 0xA2
    '╦': CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0xA8
    '╬': CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_2,  # 0xAA
}

_name = 'Unicode [4 Dashes]'
_temp_array = _generated_lookup_array(_temp_dict)
_g_character_sets.append(CharacterSet(_name, _temp_dict, _temp_array))

# -------------------------------------------------------------------------
# Unicode (Shadow) and ASCII
# -------------------------------------------------------------------------
gdict_ascii_classification_by_char = {
    '|': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x11
    '-': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x44
    '+': CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x55
    '=': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0x88
    '#': CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_2,  # 0xAA
}

# The ASCII look-up array is an exception that needed to be created manually.
#
# The following used the above Unicode classification dictionary to generate
# this ASCII lookup array for manual editing.  The finished array is here.
# It is indexed by classification like the other character look-up arrays.
glst_ascii_box_char_lookup_by_classification = [
    _nc,  # 0x00
    '|',  # 0x01 = CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_1
    '#',  # 0x02 = CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_2
    _nc,  # 0x03
    '-',  # 0x04 = CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_0
    '+',  # 0x05 = CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_1
    '#',  # 0x06 = CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_2
    _nc,  # 0x07
    '=',  # 0x08 = CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_0
    '+',  # 0x09 = CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_1
    '#',  # 0x0A = CB.LINES_LEFT_0 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_2
    _nc,  # 0x0B
    _nc,  # 0x0C
    _nc,  # 0x0D
    _nc,  # 0x0E
    _nc,  # 0x0F
    '|',  # 0x10 = CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_0
    '|',  # 0x11 = CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_1
    _nc,  # 0x12
    _nc,  # 0x13
    '+',  # 0x14 = CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_0
    '+',  # 0x15 = CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_1
    _nc,  # 0x16
    _nc,  # 0x17
    '+',  # 0x18 = CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_0
    '+',  # 0x19 = CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_1
    _nc,  # 0x1A
    _nc,  # 0x1B
    _nc,  # 0x1C
    _nc,  # 0x1D
    _nc,  # 0x1E
    _nc,  # 0x1F
    '#',  # 0x20 = CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_0
    _nc,  # 0x21
    '#',  # 0x22 = CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_2
    _nc,  # 0x23
    '#',  # 0x24 = CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_0
    _nc,  # 0x25
    '#',  # 0x26 = CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_2
    _nc,  # 0x27
    '#',  # 0x28 = CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_0
    _nc,  # 0x29
    '#',  # 0x2A = CB.LINES_LEFT_0 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_2
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
    '-',  # 0x40 = CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_0
    '+',  # 0x41 = CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_1
    '#',  # 0x42 = CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_2
    _nc,  # 0x43
    '-',  # 0x44 = CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_0
    '+',  # 0x45 = CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_1
    '#',  # 0x46 = CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_2
    _nc,  # 0x47
    _nc,  # 0x48
    _nc,  # 0x49
    _nc,  # 0x4A
    _nc,  # 0x4B
    _nc,  # 0x4C
    _nc,  # 0x4D
    _nc,  # 0x4E
    _nc,  # 0x4F
    '+',  # 0x50 = CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_0
    '+',  # 0x51 = CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_1
    _nc,  # 0x52
    _nc,  # 0x53
    '+',  # 0x54 = CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_0
    '+',  # 0x55 = CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_1
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
    '#',  # 0x60 = CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_0
    _nc,  # 0x61
    '#',  # 0x62 = CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_2
    _nc,  # 0x63
    '#',  # 0x64 = CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_0
    _nc,  # 0x65
    '#',  # 0x66 = CB.LINES_LEFT_1 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_1 | CB.LINES_UP_2
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
    '=',  # 0x80 = CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_0
    '+',  # 0x81 = CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_1
    '#',  # 0x82 = CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_0 | CB.LINES_UP_2
    _nc,  # 0x83
    _nc,  # 0x84
    _nc,  # 0x85
    _nc,  # 0x86
    _nc,  # 0x87
    '=',  # 0x88 = CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_0
    '+',  # 0x89 = CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_1
    '#',  # 0x8A = CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_2
    _nc,  # 0x8B
    _nc,  # 0x8C
    _nc,  # 0x8D
    _nc,  # 0x8E
    _nc,  # 0x8F
    '+',  # 0x90 = CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_0
    '+',  # 0x91 = CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_1
    _nc,  # 0x92
    _nc,  # 0x93
    _nc,  # 0x94
    _nc,  # 0x95
    _nc,  # 0x96
    _nc,  # 0x97
    '+',  # 0x98 = CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_0
    '+',  # 0x99 = CB.LINES_LEFT_2 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_2 | CB.LINES_UP_1
    _nc,  # 0x9A
    _nc,  # 0x9B
    _nc,  # 0x9C
    _nc,  # 0x9D
    _nc,  # 0x9E
    _nc,  # 0x9F
    '#',  # 0xA0 = CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_0
    _nc,  # 0xA1
    '#',  # 0xA2 = CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_0 | CB.LINES_UP_2
    _nc,  # 0xA3
    _nc,  # 0xA4
    _nc,  # 0xA5
    _nc,  # 0xA6
    _nc,  # 0xA7
    '#',  # 0xA8 = CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_0
    _nc,  # 0xA9
    '#',  # 0xAA = CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_2
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

# -------------------------------------------------------------------------
# Unicode (Shadow)
#
# This is really just a placeholder.  Drawing logic does not use
# this except to identify the current character set as being the
# UNICODE_SHADOW set.
# -------------------------------------------------------------------------
_name = 'Unicode [Shadow]'
_temp_dict = gdict_ascii_classification_by_char             # Dummy list (safety for some API functions)
_temp_array = glst_ascii_box_char_lookup_by_classification  # Dummy list (safety for some API functions)
_g_character_sets.append(CharacterSet(_name, _temp_dict, _temp_array))

# -------------------------------------------------------------------------
# ASCII
# -------------------------------------------------------------------------
_name = 'ASCII'
_temp_dict = gdict_ascii_classification_by_char
_temp_array = glst_ascii_box_char_lookup_by_classification
_g_character_sets.append(CharacterSet(_name, _temp_dict, _temp_array))

# Clean up.
del _name, _temp_array, _temp_dict

# Sanity Check
assert len(_g_character_sets) == CharacterSetID.LAST + 1, \
        'CharacterSet enumeration must reflect contents of `_g_character_sets`.'

up_bit_shift_count = Direction.UP    << 1
rt_bit_shift_count = Direction.RIGHT << 1
dn_bit_shift_count = Direction.DOWN  << 1
lf_bit_shift_count = Direction.LEFT  << 1


# =========================================================================
# Data
# =========================================================================

# These two define the current character set.
# Clients of this module use these two properties.
# They get their initial assignments below with the call to
# `advance_to_next_character_set()`.
gdict_classification_by_char = None
glst_box_char_lookup_by_classification = None

# This index allows `advance_to_next_character_set()` to know where to go next.
_gi_current_char_set_id: CharacterSetID = _cfg_initial_character_set_id


def set_current_character_set(id: CharacterSetID, debugging: bool):
    """ Set current character set using `id`. """
    global _gi_current_char_set_id
    _gi_current_char_set_id = id
    debugging = debugging or is_debugging(DebugBit.CHARACTER_SET)
    if debugging:
        name = current_character_set_name()
        print('In set_current_character_set()')
        print(f'  New character set: {id} ({name})')


def is_character_set(id: CharacterSetID):
    """ Does `id` match ID of current character set? """
    return ((id == _gi_current_char_set_id))


def is_shadow_character_set():
    """ Is current character set the shadow set? """
    return ((_gi_current_char_set_id == CharacterSetID.UNICODE_SHADOW))


def current_character_set_id():
    """ Current character set ID """
    return _gi_current_char_set_id


def current_character_set():
    """ Current character set """
    return _g_character_sets[_gi_current_char_set_id]


def current_character_set_name():
    """ Current character lookup array """
    char_set = _g_character_sets[_gi_current_char_set_id]
    return char_set.name


def current_classification_dictionary():
    """ Current classification dictionary """
    char_set = _g_character_sets[_gi_current_char_set_id]
    return char_set.classification_dict


def current_lookup_array():
    """ Current character lookup array """
    char_set = _g_character_sets[_gi_current_char_set_id]
    return char_set.lookup_array


def character_by_classification(classification: int) -> str:
    """ Current character lookup array """
    assert 0 <= classification <= 255, '`classification` must be in range [0-255].'
    char_set = _g_character_sets[_gi_current_char_set_id]
    return char_set.lookup_array[classification]


def character_by_line_counts(up: int, rt: int, dn: int, lf: int) -> str:
    """ Current character lookup array """
    assert 0 <= up <= 2, '`up` must be in range [0-2].'
    assert 0 <= rt <= 2, '`rt` must be in range [0-2].'
    assert 0 <= dn <= 2, '`dn` must be in range [0-2].'
    assert 0 <= lf <= 2, '`lf` must be in range [0-2].'

    up_bit_field = up << up_bit_shift_count
    rt_bit_field = rt << rt_bit_shift_count
    dn_bit_field = dn << dn_bit_shift_count
    lf_bit_field = lf << lf_bit_shift_count
    classification = up_bit_field | rt_bit_field | dn_bit_field | lf_bit_field

    char_set = _g_character_sets[_gi_current_char_set_id]
    print(f'>>>>>>>> charset name = [{current_character_set_name()}]')
    return char_set.lookup_array[classification]

def advance_to_next_character_set(debugging: bool):
    global _gi_current_char_set_id
    _gi_current_char_set_id += 1
    if _gi_current_char_set_id > CharacterSetID.LAST:
        _gi_current_char_set_id = 0
    set_current_character_set(_gi_current_char_set_id, debugging)


# Set initial character set.  This is simply to establish a consistent
# state.  Once the Package is fully loaded, `core.on_package_loaded()`
# gets called, reads the Package settings, and then calls this function
# again setting the character set according to the user-configured
# ``default_character_set_id`` setting.
debugging = is_debugging(DebugBit.CHARACTER_SET)
set_current_character_set(_cfg_initial_character_set_id, debugging)


# =========================================================================
# Character Classification Utilities
# =========================================================================

def line_count(c: str, side: Direction, debugging: bool) -> int:
    r"""
    Number of lines for character `c` on side `side`.

    Only box-drawing characters can have 1 or 2 lines, and most box-drawing
    characters have 0 lines coming out of at least one of their sides.
    All other characters will be considered to have 0 lines on all sides
    because they are not found in the current classification dictionary.

    The current classification dictionary references a dictionary with the
    box-drawing characters as keys.  Which dictionary it references starts
    out (each Sublime Text session) with a user-configured character set
    index controlled by the `default_character_set` setting.

    The integer values contain 4 bit fields that tell us how many lines
    come out of each side of that box-drawing character:

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

    The unsigned integer in each bit field provides the count of lines on
    that side:

    - 0 = 0b00 = no lines
    - 1 = 0b01 = 1 line
    - 2 = 0b10 = 2 lines

    The OR-ed combined values of the 4 bit fields index into a
    character-lookup array for fast character look-up.

    Note that the ``Direction`` IntEnum class is carefully ordered to so
    that the ``side`` can be used to compute the number of bits each
    field is shifted.

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
    curr_classification_dict = current_classification_dictionary()

    if c in curr_classification_dict:
        classification = curr_classification_dict[c]
        shift_bit_count = side << 1
        result = (classification >> shift_bit_count) & 0x03
        if debugging:
            print(f'    classification=0x{classification:02X}')
            print(f'    {shift_bit_count=}')

    if debugging:
        print(f'    {result=}')

    return result


def adjusted_classification(c: str, side: Direction, new_line_count: int, debugging: bool):
    """ Adjusted classification to connect on ``side`` with ``new_line_count``. """
    curr_classification_dict = current_classification_dictionary()
    result = curr_classification_dict[c]
    shift_bit_count = side << 1

    # Remove any old bits.
    mask_out_bits_mask = 0x03 << shift_bit_count
    if debugging:
        print('In adjusted_classification()...')
        print(f'  {c=}')
        print(f'  {side=}')
        print(f'  {new_line_count=}')
        print(f'  Classification     : 0x{result:02X}')
        print(f'  {shift_bit_count=}')
        print(f'  Mask-out bits      : 0x{mask_out_bits_mask:02X}')
    result &= ~mask_out_bits_mask
    if debugging:
        print(f'   Bits masked out   : 0x{result:02X}')

    # Add new bits.
    new_bit_mask = new_line_count << shift_bit_count
    result |= new_bit_mask
    if debugging:
        print(f'   New bit field     : 0x{new_bit_mask:02X}')
        print(f'   Adj classification: 0x{result:02X}')

    return result


