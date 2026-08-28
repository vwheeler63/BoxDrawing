"""
Exercises the directional painting branch of BoxDrawingDrawOneCharacterCommand,
plus a regression check that line drawing is untouched when no brush is selected.
"""
import importlib
import os
import sys

# This test lives inside the Package, so the Package directory is one level
# up, and the directory that must be on `sys.path` for the Package to be
# importable is one level above that.  The stubs directory shadows Sublime
# Text's own `sublime` / `sublime_plugin` modules, which do not exist outside
# of Sublime Text.
HERE     = os.path.dirname(os.path.abspath(__file__))
PKG_DIR  = os.path.dirname(HERE)
PKG_NAME = os.path.basename(PKG_DIR)

sys.path.insert(0, os.path.join(HERE, 'stubs'))
sys.path.insert(0, os.path.dirname(PKG_DIR))

import sublime                                       # noqa: E402  (the stub)


def _module(name):
    return importlib.import_module(f'{PKG_NAME}.{name}')

core          = _module('src.core')
character_set = _module('src.character_set')
fill_brush    = _module('src.fill_brush')
Direction      = character_set.Direction
CharacterSetID = character_set.CharacterSetID
FillBrushID    = fill_brush.FillBrushID
BoxDrawingDrawOneCharacterCommand = _module('src.commands.draw_one_char').BoxDrawingDrawOneCharacterCommand



failures = []
checks = [0]


def check(label, got, want):
    checks[0] += 1
    if got != want:
        failures.append(f'{label}\n     got: {got!r}\n    want: {want!r}')
        print(f'  FAIL  {label}')
    else:
        print(f'  ok    {label}')


def session(text, row, col, brush_id=FillBrushID.NONE, char_set=CharacterSetID.ASCII):
    """Build a View with box drawing ON and a caret at (row, col)."""
    fill_brush.set_current_brush(brush_id, False)
    character_set.set_current_character_set(char_set, False)
    view = sublime.View(text)
    core.set_drawing_state(view, core.State.ON)
    core.set_last_direction(view, Direction.NONE)
    pt = view.text_point(row, col)
    view.sel().clear()
    view.sel().add(pt)
    return view, BoxDrawingDrawOneCharacterCommand.__new__(BoxDrawingDrawOneCharacterCommand)


def press(view, cmd, line_count, direction):
    """Simulate one key press.  Returns the caret's (row, col) afterwards."""
    cmd.view = view
    cmd.run(sublime.Edit(), line_count, direction)
    return view.rowcol(view.sel()[0].b)


LINE_COUNT_ALT       = 1   # [Alt-Arrow]
LINE_COUNT_ALT_SHIFT = 2   # [Alt-Shift-Arrow]
LINE_COUNT_ERASE     = 0   # [Ctrl-Alt-Shift-Arrow]


# -------------------------------------------------------------------------
print('\npainting — stamp and move')

view, cmd = session('     \n     ', 0, 0, brush_id=FillBrushID.DARK_SHADE)
caret = press(view, cmd, LINE_COUNT_ALT, Direction.RIGHT)
check('[Alt-Right] stamps at the caret', view.text.split('\n')[0][0], '▓')
check('[Alt-Right] then moves right', caret, (0, 1))

caret = press(view, cmd, LINE_COUNT_ALT, Direction.RIGHT)
caret = press(view, cmd, LINE_COUNT_ALT, Direction.RIGHT)
check('a run of three', view.text.split('\n')[0], '▓▓▓  ')
check('caret advanced three', caret, (0, 3))

print('\npainting — stamp in place')

view, cmd = session('     ', 0, 2, brush_id=FillBrushID.FULL_BLOCK)
caret = press(view, cmd, LINE_COUNT_ALT_SHIFT, Direction.RIGHT)
check('[Alt-Shift-Right] stamps', view.text, '  █  ')
check('[Alt-Shift-Right] does not move', caret, (0, 2))

caret = press(view, cmd, LINE_COUNT_ALT_SHIFT, Direction.UP)
check('re-stamping in place is idempotent', view.text, '  █  ')
check('still has not moved', caret, (0, 2))

print('\npainting — every direction')

view, cmd = session('     \n     \n     ', 1, 2, brush_id=FillBrushID.LIGHT_SHADE)
press(view, cmd, LINE_COUNT_ALT, Direction.UP)
check('[Alt-Up] moves up', view.rowcol(view.sel()[0].b), (0, 2))

view, cmd = session('     \n     \n     ', 1, 2, brush_id=FillBrushID.LIGHT_SHADE)
press(view, cmd, LINE_COUNT_ALT, Direction.DOWN)
check('[Alt-Down] moves down', view.rowcol(view.sel()[0].b), (2, 2))

view, cmd = session('     \n     \n     ', 1, 2, brush_id=FillBrushID.LIGHT_SHADE)
press(view, cmd, LINE_COUNT_ALT, Direction.LEFT)
check('[Alt-Left] moves left', view.rowcol(view.sel()[0].b), (1, 1))

print('\npainting — buffer edges')

view, cmd = session('     ', 0, 0, brush_id=FillBrushID.LIGHT_SHADE)
caret = press(view, cmd, LINE_COUNT_ALT, Direction.UP)
check('[Alt-Up] on row 0 stamps but cannot move', view.text, '░    ')
check('[Alt-Up] on row 0 leaves the caret', caret, (0, 0))

caret = press(view, cmd, LINE_COUNT_ALT, Direction.LEFT)
check('[Alt-Left] in column 0 leaves the caret', caret, (0, 0))

view, cmd = session('abc', 0, 2, brush_id=FillBrushID.LIGHT_SHADE)
caret = press(view, cmd, LINE_COUNT_ALT, Direction.RIGHT)
check('painting at EOL extends the line', view.text, 'ab░ ')
check('caret moved into the new space', caret, (0, 3))

view, cmd = session('abc', 0, 1, brush_id=FillBrushID.LIGHT_SHADE)
caret = press(view, cmd, LINE_COUNT_ALT, Direction.DOWN)
check('painting past the last row creates a row', view.text.split('\n')[1][1], ' ')
check('caret moved to the new row', caret, (1, 1))

print('\npainting — erase still works with a brush selected')

view, cmd = session('░░░░░', 0, 1, brush_id=FillBrushID.LIGHT_SHADE)
caret = press(view, cmd, LINE_COUNT_ERASE, Direction.RIGHT)
check('[Ctrl-Alt-Shift-Right] erases', view.text, '░ ░░░')
check('[Ctrl-Alt-Shift-Right] moves on', caret, (0, 2))

print('\npainting — the brush beats the Shadow character set')

view, cmd = session('     ', 0, 0,
                    brush_id=FillBrushID.RIGHT_HALF,
                    char_set=CharacterSetID.UNICODE_SHADOW)
press(view, cmd, LINE_COUNT_ALT, Direction.RIGHT)
check('brush wins over the Shadow set', view.text[0], '▐')

print('\npainting — last direction is reset')

view, cmd = session('     ', 0, 0, brush_id=FillBrushID.LIGHT_SHADE)
press(view, cmd, LINE_COUNT_ALT, Direction.RIGHT)
check('painting resets last direction', core.last_direction(view), Direction.NONE)


# -------------------------------------------------------------------------
print('\nregression — no brush selected, line drawing is untouched')

view, cmd = session('     \n     ', 0, 0)
press(view, cmd, LINE_COUNT_ALT, Direction.RIGHT)
press(view, cmd, LINE_COUNT_ALT, Direction.RIGHT)
press(view, cmd, LINE_COUNT_ALT, Direction.RIGHT)
first_line = view.text.split('\n')[0]
check('ASCII single line drawn', first_line, '---  ')
check('no brush characters written',
      any(c in first_line for c in '░▒▓█▀▄▌▐'), False)

view, cmd = session('     \n     ', 0, 0)
press(view, cmd, LINE_COUNT_ALT_SHIFT, Direction.RIGHT)
press(view, cmd, LINE_COUNT_ALT_SHIFT, Direction.RIGHT)
check('ASCII double line drawn', view.text.split('\n')[0], '==   ')

view, cmd = session('     \n     ', 0, 0, char_set=CharacterSetID.UNICODE_ROUND_CORNERS)
press(view, cmd, LINE_COUNT_ALT, Direction.RIGHT)
press(view, cmd, LINE_COUNT_ALT, Direction.RIGHT)
press(view, cmd, LINE_COUNT_ALT, Direction.DOWN)
check('Unicode corner still forms', view.text.split('\n')[0], '─╮   ')

view, cmd = session('     ', 0, 0, char_set=CharacterSetID.UNICODE_SHADOW)
press(view, cmd, LINE_COUNT_ALT, Direction.RIGHT)
press(view, cmd, LINE_COUNT_ALT_SHIFT, Direction.RIGHT)
check('Shadow set still works with no brush', view.text[:2], '░▒')



# -------------------------------------------------------------------------
print('\nmenu label — the greyed-out drawing hints')

BoxDrawingMenuLabelCommand = _module('src.commands.menu_label').BoxDrawingMenuLabelCommand

view, _ = session('     ', 0, 0)
label = BoxDrawingMenuLabelCommand.__new__(BoxDrawingMenuLabelCommand)
label.view = view

check('label is never enabled, drawing ON', label.is_enabled(), False)
check('label is visible', label.is_visible(), True)

core.set_drawing_state(view, core.State.OFF)
check('label is never enabled, drawing OFF', label.is_enabled(), False)

before = view.text
label.run(sublime.Edit())
check('label modifies nothing if ever run', view.text, before)


# -------------------------------------------------------------------------
print()
if failures:
    print(f'{len(failures)} of {checks[0]} checks FAILED:\n')
    for f in failures:
        print(' -', f)
    sys.exit(1)

print(f'All {checks[0]} checks passed.')
