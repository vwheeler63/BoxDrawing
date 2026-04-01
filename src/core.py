r""" ***********************************************************************
Box Drawing
===========================================================================

Box Drawing is Sublime Text package enabling the user to use

- [Alt-Arrow]             (single line)
- [Alt-Shift-Arrow]       (double line), or
- [Ctrl-Alt-Shift-Arrow]  (erase)

to draw lines and boxes in their text like these:

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

See ``README.md`` for more details.


States
======

This Package has several states that can change during a Sublime Text session:

- Is Box Drawing enabled?  This state is tracked per View.
  ``Tools > Box Drawing Enabled`` shows the state for the current View with a
  checkmark.  At the beginning of each Sublime Text session, this state is
  DISABLED for all Views.

- Which Box Drawing character set is in use:  ASCII or Unicode?
  This state is global (remembered within the loaded Package) and applies to
  all Views at the same time.  Since this can be conveniently switched via a
  single keystroke, there is no use case that justifies keeping it per View.
  ``Tools > Toggle Box Drawing Character Set (ASCII)`` shows this state
  with the value in parentheses.  At the beginning of each Sublime Text session,
  this state is set to the configured ``default_character_set``.  The memory
  of it is kept within the ``character_set.py`` module and is accessed by
  ``character_set.is_ascii_mode()``, which returns a Boolean value and is used
  throughout the Package to determine which character set is current.

- Last drawing direction used:  up, right, down, or left?
  This state is tracked per View, and by design is only visible
  internally. It is used as part of the box-drawing algorithm in
  the ``box_drawing_draw_one_character`` command.


Keys
====

This Package remembers what drawing mode it is in (``OFF`` vs ``ON``) per View
through a command to turn box-drawing mode ON and OFF (which the user is free
to map to any key combination he wishes, or simply execute the command via
the Command Palette).  The Package has a custom ``on_query_context``
implemented to override these normal key combinations when box drawing
mode is ON:

+-------------------------------------+-------------+
| Key Combination                     | Meaning     |
+=====================================+=============+
| alt+(left|right|up|down)            | single line |
+-------------------------------------+-------------+
| alt+shift+(left|right|up|down)      | double line |
+-------------------------------------+-------------+
| ctrl+alt+shift+(left|right|up|down) | erase       |
+-------------------------------------+-------------+

When ``contexts.on_query_context()`` returns ``True``, they key bindings
shown above override the normal bindings for the arrow keys.

[alt+(left|right)] are mapped by default to "move left/right by subwords"
with "extending selection" when the [Shift] key is held down.

[alt+(up|down)] are mapped by default in the reStructuredText Package to
"move up/down by 1 section", with a possible [Shift] modifier limiting
the move to only the same level of section or higher.

When Box Drawing is OFF for the current View, ``contexts.on_query_context()``
returns ``False`` or ``None`` as appropriate, and Sublime Text uses the
normal bindings for these keys.
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
from . import character_set


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
        view_settings.set(cfg_view_box_drawing_last_direction_key, character_set.Direction.NONE)
        sublime.status_message('Box Drawing OFF')
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
        sublime.status_message('Box Drawing ON')
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
        character_set.set_ascii_mode(debugging)
    else:
        character_set.set_unicode_mode(debugging)

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
