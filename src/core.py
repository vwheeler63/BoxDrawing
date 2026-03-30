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


Settings
========

See ``BoxDrawing.sublime-settings`` to see what user-configurable Package
settings there are and what they mean.

- default_character_set ("ASCII" | "Unicode")
- debugging (see ``BoxDrawing.sublime-settings`` for description of valid values)


States
======

This Package has several states that can change during a Sublime Text session:

- Is Box Drawing enabled?  This state is tracked per View.
  ``Tools > Box Drawing Enabled`` shows this state with a checkmark.  At the
  beginning of each Sublime Text session, this state is DISABLED for all Views.

- Which Box Drawing character set is in use:  ASCII or Unicode?
  This state is global (remembered within the loaded Package) and applies
  to all Views at the same time.  Since this can be conveniently switched
  via a single keystroke, there is no need to keep it per View.
  ``Tools > Toggle Box Drawing Character Set (ASCII)`` shows this state
  with the value in parentheses.  At the beginning of each Sublime Text session,
  this state is set to the configured ``default_character_set``.  The memory
  of it is kept within the ``box_character.py`` module and is accessed by
  ``box_character.is_ascii_mode()``, which returns a Boolean value and can
  be used to determine which mode is current.

- Last drawing direction used:  up, right, down, or left?  This state is
  tracked per View.  This state is, by design, only visible internally and is
  used as part of the drawing algorithm in the ``box_drawing_draw_one_character``
  command.


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

See ``box_character.py`` to see which characters are involved.


Keys
====

This Package remembers what drawing mode it is in (``OFF`` vs ``ON``)
through a command to turn box-drawing mode ON and OFF (which the user is free
to map to any key combination he wishes, or simply execute the command via
the Command Palette).  The Package would have a custom ``on_query_context``
implemented to override these normal key combinations when box drawing mode
was ON:

+-------------------------------------+-------------+
| Key Combination                     | Meaning     |
+=====================================+=============+
| alt+(left|right|up|down)            | single line |
+-------------------------------------+-------------+
| alt+shift+(left|right|up|down)      | double line |
+-------------------------------------+-------------+
| ctrl+alt+shift+(left|right|up|down) | erase       |
+-------------------------------------+-------------+

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
from . import box_character


# =========================================================================
# Configuration
# =========================================================================

# Use name of parent directory as `package_name`.
_cfg_pkg_settings_file                  = package_name + '.sublime-settings'

# Track on-settings-changed listener.
_cfg_on_settings_chgd_listener_id       = '_bd_settings_changed_tag'

# Package Settings Names (most are used multiple times throughout this Plugin)
_cfg_stg_name__default_character_set    = 'default_character_set'
_cfg_stg_name__debugging                = 'debugging'

# View settings keys (accessed by multiple external modules).
cfg_view_box_drawing_state_key          = '_box_drawing_state'
cfg_view_box_drawing_last_direction_key = '_box_drawing_last_direction'


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
    _cfg_stg_name__default_character_set: "ASCII",
    _cfg_stg_name__debugging: False
}


# =========================================================================
# Package-Wide Classes
# =========================================================================

class State(IntEnum):
    """
    Whether a particular View is in Box-Drawing Mode or not.
    """
    OFF = 0
    ON  = 1   # In box-drawing mode


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

    # Set initial box-drawing character set.
    debugging = is_debugging(DebugBit.LOAD_UNLOAD)
    is_ascii = ((bd_setting(_cfg_stg_name__default_character_set) == 'ASCII'))
    if is_ascii:
        box_character.set_ascii_mode(debugging)
    else:
        box_character.set_unicode_mode(debugging)

    # Report.
    if debugging:
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
