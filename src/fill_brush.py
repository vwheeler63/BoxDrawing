r"""
Fill Brush
==========

This logic pertains to the "fill brush":  the block/shade character that,
when selected, turns BoxDrawing from a line-drawing tool into a painting
tool.

By design, this module knows nothing about Sublime Text, Views, View
settings, etc..  Only these characters and their identities.  The Package
settings that can influence it (the startup brush and the user-overridable
character table) are read by ``core`` and handed to this module, keeping
this module free of any dependency on Sublime Text.


The Brushes
===========

Eight brushes, in the order they are bound to [Ctrl-Alt-1] .. [Ctrl-Alt-8]:

- shade characters:
    - ░  light shade         U+2591
    - ▒  medium shade        U+2592
    - ▓  dark shade          U+2593
    - █  full block          U+2588

- half-block characters:
    - ▀  upper half block    U+2580
    - ▄  lower half block    U+2584
    - ▌  left half block     U+258C
    - ▐  right half block    U+2590

Brush 0 is not a character.  It is the absence of a brush, i.e. ordinary
BoxDrawing line-drawing mode, and is bound to [Ctrl-Alt-0].


Independence from the Character Set
===================================

The selected brush and the selected box-drawing character set are wholly
independent of each other.  Changing one never changes the other.  This is
deliberate:  a brush is a property of the tool in the user's hand, not a
property of the line-drawing alphabet.

Note that none of the brush characters appear in the character-set
classification dictionaries (see ``character_set.py``), so
``character_set.line_count()`` reports 0 lines for all of them.  Line
drawing therefore never tries to connect through painted areas, and painted
areas act as walls for flood fill.  That behavior falls out of the existing
design; no classification entries are needed for these characters.


@version  Current revision:  @(#) v1.0  20-Aug-2026
@version  1.0  20-Aug-2026 jr  - Created
"""
from enum import IntEnum
from typing import List
from ..lib.debug import DebugBits, is_debugging


# =========================================================================
# Classes
# =========================================================================

class FillBrushID(IntEnum):
    """
    Fill Brush Enumeration

    The enumerator values are deliberately identical to the digit each
    brush is bound to, so that the keymaps, the Command Palette entries and
    the menu items can all pass the digit straight through as ``brush_id``
    with no lookup table anywhere.

    Maintenance Note:  when this class changes, also change the
    documentation in ``BoxDrawing.sublime-settings``.
    """
    NONE         = 0   # No brush:  ordinary BoxDrawing line-drawing mode.
    LIGHT_SHADE  = 1   # ░
    MEDIUM_SHADE = 2   # ▒
    DARK_SHADE   = 3   # ▓
    FULL_BLOCK   = 4   # █
    UPPER_HALF   = 5   # ▀
    LOWER_HALF   = 6   # ▄
    LEFT_HALF    = 7   # ▌
    RIGHT_HALF   = 8   # ▐
    LAST         = 8
    COUNT        = 9


# =========================================================================
# Configuration
# =========================================================================

# Brush characters, indexed by `FillBrushID`.  Index 0 is the empty string
# because `FillBrushID.NONE` is the absence of a brush, not a character.
# This alignment lets `brush_id` index this list directly.
_cfg_default_brush_characters: List[str] = [
    '',    # 0  NONE
    '░',   # 1  LIGHT_SHADE     U+2591
    '▒',   # 2  MEDIUM_SHADE    U+2592
    '▓',   # 3  DARK_SHADE      U+2593
    '█',   # 4  FULL_BLOCK      U+2588
    '▀',   # 5  UPPER_HALF      U+2580
    '▄',   # 6  LOWER_HALF      U+2584
    '▌',   # 7  LEFT_HALF       U+258C
    '▐',   # 8  RIGHT_HALF      U+2590
]

# Brush names, indexed by `FillBrushID`.
_cfg_brush_names: List[str] = [
    'None',
    'Light Shade',
    'Medium Shade',
    'Dark Shade',
    'Full Block',
    'Upper Half Block',
    'Lower Half Block',
    'Left Half Block',
    'Right Half Block',
]

# Initial brush.  This is simply to establish a consistent state.  Once the
# Package is fully loaded, `core.on_plugin_loaded()` reads the Package
# settings and calls `set_current_brush()` with the user-configured
# ``default_fill_brush_id`` setting.
_cfg_initial_brush_id: FillBrushID = FillBrushID.NONE


# Sanity Checks
assert len(_cfg_default_brush_characters) == FillBrushID.COUNT, \
        '`_cfg_default_brush_characters` must have one entry per `FillBrushID`.'
assert len(_cfg_brush_names) == FillBrushID.COUNT, \
        '`_cfg_brush_names` must have one entry per `FillBrushID`.'


# =========================================================================
# Data
# =========================================================================

# Live brush character table.  Replaced wholesale by `set_brush_characters()`
# when the user overrides it in the Package settings.
_g_brush_characters: List[str] = list(_cfg_default_brush_characters)

# Currently selected brush.
_gi_current_brush_id: FillBrushID = _cfg_initial_brush_id


# =========================================================================
# Brush Table
# =========================================================================

def set_brush_characters(characters, debugging: bool) -> bool:
    """
    Replace the brush character table with a user-supplied one.

    The supplied value must be a list of exactly 8 strings, each exactly one
    character long, in [Ctrl-Alt-1] .. [Ctrl-Alt-8] order.  Anything else is
    rejected in favor of the built-in table:  a bad setting must never keep
    the Package from loading.

    :param characters:  candidate list of 8 single-character strings,
                          or ``None`` to restore the built-in table
    :param debugging:   Are we debugging?
    :returns:  ``True`` if `characters` was accepted, ``False`` otherwise.
    """
    global _g_brush_characters
    debugging = debugging or is_debugging(DebugBits.FILL_BRUSH)
    if debugging:
        print('In set_brush_characters()')
        print(f'  {characters=}')

    brush_count = FillBrushID.COUNT - 1   # Brush 0 is not a character.

    if characters is None:
        _g_brush_characters = list(_cfg_default_brush_characters)
        if debugging:
            print('  Built-in brush characters restored.')
        return True

    valid = (
            isinstance(characters, list)
        and len(characters) == brush_count
        and all(isinstance(c, str) and len(c) == 1 for c in characters)
        )

    if not valid:
        print(
            'BoxDrawing:  "fill_brush_characters" setting must be a list of '
            f'{brush_count} single-character strings.  Using built-in brushes.'
            )
        _g_brush_characters = list(_cfg_default_brush_characters)
        return False

    _g_brush_characters = [''] + list(characters)
    if debugging:
        print(f'  Brush characters replaced: {_g_brush_characters[1:]}')

    return True


# =========================================================================
# Brush Selection
# =========================================================================

def set_current_brush(id: FillBrushID, debugging: bool):
    """
    Select the brush identified by `id`.

    An out-of-range `id` selects ``FillBrushID.NONE`` rather than raising:
    this is reachable from user-editable keymaps, menus and the Command
    Palette, and dropping back to line-drawing mode is the safe outcome.

    :param id:         brush to select
    :param debugging:  Are we debugging?
    """
    global _gi_current_brush_id
    debugging = debugging or is_debugging(DebugBits.FILL_BRUSH)

    if isinstance(id, bool):
        print(f'BoxDrawing:  fill brush id {id!r} is not a number;  clearing brush.')
        id = FillBrushID.NONE

    try:
        id = int(id)
    except (TypeError, ValueError):
        print(f'BoxDrawing:  fill brush id {id!r} is not a number;  clearing brush.')
        id = FillBrushID.NONE

    if not (FillBrushID.NONE <= id <= FillBrushID.LAST):
        print(f'BoxDrawing:  fill brush id {id} out of range;  clearing brush.')
        id = FillBrushID.NONE

    _gi_current_brush_id = FillBrushID(id)

    if debugging:
        print('In set_current_brush()')
        print(f'  New fill brush: {int(_gi_current_brush_id)} ({current_brush_name()})')


def clear_current_brush(debugging: bool):
    """ Return to ordinary BoxDrawing line-drawing mode. """
    set_current_brush(FillBrushID.NONE, debugging)


# =========================================================================
# Queries
# =========================================================================

def current_brush_id() -> FillBrushID:
    """ Currently selected brush ID. """
    return _gi_current_brush_id


def current_brush_char() -> str:
    """ Currently selected brush character;  '' when no brush is selected. """
    return _g_brush_characters[_gi_current_brush_id]


def current_brush_name() -> str:
    """ Currently selected brush as e.g. '▓ Dark Shade', or 'None'. """
    return brush_name(_gi_current_brush_id)


def is_brush_active() -> bool:
    """ Is a fill brush selected, i.e. is the Package in paint mode? """
    return ((_gi_current_brush_id != FillBrushID.NONE))


def is_brush_character(c: str) -> bool:
    """ Is `c` one of the eight brush characters? """
    return ((c != '' and c in _g_brush_characters))


def brush_char(id: FillBrushID) -> str:
    """ Character for brush `id`;  '' for `NONE` or an out-of-range `id`. """
    if not (FillBrushID.NONE <= id <= FillBrushID.LAST):
        return ''
    return _g_brush_characters[id]


def brush_name(id: FillBrushID) -> str:
    """
    Name for brush `id`, with its character prepended, e.g. '▓ Dark Shade'.
    `FillBrushID.NONE` is simply 'None'.
    """
    if not (FillBrushID.NONE <= id <= FillBrushID.LAST):
        return _cfg_brush_names[FillBrushID.NONE]
    if id == FillBrushID.NONE:
        return _cfg_brush_names[FillBrushID.NONE]
    return f'{_g_brush_characters[id]} {_cfg_brush_names[id]}'
