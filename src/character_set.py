"""
Box Character Set
=================

This logic pertains to box-character drawing logic, and its ability to become
"attached" to different character sets, namely:

- ASCII
- Unicode (Square Corners)
- Unicode (Round Corners)
- Shadows

By design, this module knows nothing about Sublime Text, Views, View settings, etc..
Only these sets of characters and their characteristics/classifications.


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

┌─┬┐  ╔═╦╗  ╓─╥╖  ╒═╤╕    +------------+----------------+
│ ││  ║ ║║  ║ ║║  │ ││    | Column One | Column Two     |
├─┼┤  ╠═╬╣  ╟─╫╢  ╞═╪╡    +============+================+
└─┴┘  ╚═╩╝  ╙─╨╜  ╘═╧╛    |            |                |
┌───────────────────┐     +------------+----------------+
│  ╔═══╗ Some Text  │     |            |                |
│  ╚═╦═╝ in the box │     +------------+----------------+
╞═╤══╩══╤═══════════╡     |            |                |
│ ├──┬──┤           │     +------------+----------------+
│ └──┴──┘           │     |            |                |
└───────────────────┘     +------------+----------------+



Character Classification
========================

See docstring in ``line_count()`` function below.
"""
from enum import IntFlag, IntEnum


# =========================================================================
# Configuration
# =========================================================================

# Neutral character in look-up arrays.
_cfg_neutral_character = '·'
# Abbreviation to make the various look-up arrays more readable.
_nc = _cfg_neutral_character


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


# =========================================================================
# Constants
# =========================================================================

# -------------------------------------------------------------------------
# Classifications by Box-Drawing Character
#
# Note:  not all bit combinations are represented.  Some bit-field
# combinations do not appear in the Unicode box-drawing character set,
# so they are not represented below.  Such combinations are caught within
# the box-drawing logic before they are used.  Also, many fonts only have
# a subset of the full set of Unicode box-drawing characters (including
# Sublime Text) so only the normally-supported character set is used.
#
# Columns are in bit order left-to-right (most-significant to least):
#       LEFT   BOTTOM   RIGHT   TOP
# -------------------------------------------------------------------------
gdict_unicode_classification_by_char = {
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

gdict_ascii_classification_by_char = {
    '|': CB.LINES_LEFT_0 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_0 | CB.LINES_UP_1,  # 0x11
    '-': CB.LINES_LEFT_1 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_1 | CB.LINES_UP_0,  # 0x44
    '+': CB.LINES_LEFT_1 | CB.LINES_DOWN_1 | CB.LINES_RIGHT_1 | CB.LINES_UP_1,  # 0x55
    '=': CB.LINES_LEFT_2 | CB.LINES_DOWN_0 | CB.LINES_RIGHT_2 | CB.LINES_UP_0,  # 0x88
    '#': CB.LINES_LEFT_2 | CB.LINES_DOWN_2 | CB.LINES_RIGHT_2 | CB.LINES_UP_2,  # 0xAA
}

# -------------------------------------------------------------------------
# The following used the above Unicode classification dictionary
# to generate this ASCII lookup array for manual editing.  The
# finished array is here.  It is indexed by classification as is
# ``glst_unicode_box_char_lookup_by_classification`` which is
# populated programmatically below.  The result looks a great deal
# like this lookup array.
# -------------------------------------------------------------------------
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

# Pre-allocate array with 256 elements with _nc (middle dot U+00B7) as placeholder.
glst_unicode_box_char_lookup_by_classification = [_nc] * 256

# Populate Unicode look-up array using `gdict_unicode_classification_by_char`.
for c in gdict_unicode_classification_by_char:
    classif_idx = gdict_unicode_classification_by_char[c]
    glst_unicode_box_char_lookup_by_classification[classif_idx] = c

up_bit_shift_count = Direction.UP    << 1
rt_bit_shift_count = Direction.RIGHT << 1
dn_bit_shift_count = Direction.DOWN  << 1
lf_bit_shift_count = Direction.LEFT  << 1


# =========================================================================
# Data
# =========================================================================

gdict_classification_by_char = gdict_ascii_classification_by_char
glst_box_char_lookup_by_classification = glst_ascii_box_char_lookup_by_classification


def is_ascii_mode() -> bool:
    return ((gdict_classification_by_char == gdict_ascii_classification_by_char))


def set_ascii_mode(debugging: bool):
    global gdict_classification_by_char
    global glst_box_char_lookup_by_classification
    gdict_classification_by_char = gdict_ascii_classification_by_char
    glst_box_char_lookup_by_classification = glst_ascii_box_char_lookup_by_classification
    if debugging:
        print('  Active Character Set:  ASCII.')


def set_unicode_mode(debugging: bool):
    global gdict_classification_by_char
    global glst_box_char_lookup_by_classification
    gdict_classification_by_char = gdict_unicode_classification_by_char
    glst_box_char_lookup_by_classification = glst_unicode_box_char_lookup_by_classification
    if debugging:
        print('  Active Character Set:  Unicode.')


# =========================================================================
# Character Classification Utilities
# =========================================================================

def line_count(c: str, side: Direction, debugging: bool) -> int:
    r"""
    Number of lines for character `c` on side `side`.

    Only box-drawing characters can have 1 or 2 lines, and most box-drawing
    characters have 0 lines coming out of at least one of their sides.

    All other characters will be considered to have 0 lines on all sides
    because they are not found in global ``gdict_classification_by_char``.

    ``gdict_classification_by_char`` references a dictionary with the box-drawing
    characters as keys.  Which dictionary it references is starts out (each
    Sublime Text session) matching the "default_character_set" Package setting:
    ASCII or Unicode.

    The integer values contain bit fields that tell us how many lines come out
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
        print(f'  Classification     : 0x{classification:02X}')
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


