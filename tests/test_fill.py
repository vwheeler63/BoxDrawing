"""
Exercises the BoxDrawing fill-brush logic outside of Sublime Text, using the
stub `sublime` / `sublime_plugin` modules next to this file.

Covers the fill brush module, and the flood fill cases that do not require a
live editor:  filling, re-shading, clearing, what may be seeded, the walls,
the budget, and the refusals.
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

core        = _module('src.core')
fill_brush  = _module('src.fill_brush')
FillBrushID = fill_brush.FillBrushID
BoxDrawingFloodFillCommand = _module('src.commands.flood_fill').BoxDrawingFloodFillCommand



failures = []
checks = [0]


def check(label, got, want):
    checks[0] += 1
    if got != want:
        failures.append(f'{label}\n     got: {got!r}\n    want: {want!r}')
        print(f'  FAIL  {label}')
    else:
        print(f'  ok    {label}')


def make_view(text, caret_row, caret_col):
    view = sublime.View(text)
    pt = view.text_point(caret_row, caret_col)
    view.sel().clear()
    view.sel().add(pt)
    return view


def flood(text, caret_row, caret_col, brush_id=FillBrushID.MEDIUM_SHADE, budget=100000):
    """Run a flood fill and return (resulting text, last status message)."""
    fill_brush.set_current_brush(brush_id, False)
    core.bd_setting.obj = sublime._Settings({'max_flood_cells': budget})
    view = make_view(text, caret_row, caret_col)
    cmd = BoxDrawingFloodFillCommand(view)
    del sublime.messages[:]
    cmd.run(sublime.Edit())
    msg = sublime.messages[-1] if sublime.messages else ''
    return view.text, msg, view


# -------------------------------------------------------------------------
# fill_brush module
# -------------------------------------------------------------------------
print('\nfill_brush module')

fill_brush.set_current_brush(FillBrushID.NONE, False)
check('NONE is not active', fill_brush.is_brush_active(), False)
check('NONE has no character', fill_brush.current_brush_char(), '')
check('NONE name', fill_brush.current_brush_name(), 'None')

for bid, want in ((1, '░'), (2, '▒'), (3, '▓'), (4, '█'), (5, '▀'), (6, '▄'), (7, '▌'), (8, '▐')):
    fill_brush.set_current_brush(bid, False)
    check(f'brush {bid} -> {want}', fill_brush.current_brush_char(), want)

fill_brush.set_current_brush(3, False)
check('brush 3 is active', fill_brush.is_brush_active(), True)
check('brush 3 name', fill_brush.current_brush_name(), '▓ Dark Shade')
check('brush character recognized', fill_brush.is_brush_character('▓'), True)
check('space is not a brush character', fill_brush.is_brush_character(' '), False)
check('empty is not a brush character', fill_brush.is_brush_character(''), False)
check('box char is not a brush character', fill_brush.is_brush_character('│'), False)

fill_brush.set_current_brush(99, False)
check('out-of-range id clears brush', fill_brush.current_brush_id(), FillBrushID.NONE)
fill_brush.set_current_brush('nonsense', False)
check('non-numeric id clears brush', fill_brush.current_brush_id(), FillBrushID.NONE)
fill_brush.set_current_brush(True, False)
check('bool id clears brush', fill_brush.current_brush_id(), FillBrushID.NONE)

check('bad table rejected', fill_brush.set_brush_characters(['x'], False), False)
check('bad table falls back', fill_brush.brush_char(1), '░')
check('good table accepted', fill_brush.set_brush_characters(list('12345678'), False), True)
check('override applied', fill_brush.brush_char(1), '1')
fill_brush.set_brush_characters(None, False)
check('built-in table restored', fill_brush.brush_char(1), '░')


# -------------------------------------------------------------------------
# Flood fill
# -------------------------------------------------------------------------
print('\nflood fill — closed box')

box = (
    '┌───┐\n'
    '│   │\n'
    '│   │\n'
    '└───┘'
)
got, msg, _ = flood(box, 1, 2)
check('interior filled, walls intact', got, (
    '┌───┐\n'
    '│▒▒▒│\n'
    '│▒▒▒│\n'
    '└───┘'
))
check('reports 6 cells', msg, 'Box Drawing:  filled 6 cells with ▒')
check('length preserved', len(got), len(box))

print('\nflood fill — boundaries are walls, not failures')

# Right side of the shape is EOL, not a drawn wall.
ragged = (
    '┌────\n'
    '│   \n'
    '│  \n'
    '└────'
)
got, msg, _ = flood(ragged, 1, 2)
check('fills to each row\'s own EOL', got, (
    '┌────\n'
    '│▒▒▒\n'
    '│▒▒\n'
    '└────'
))
check('no line grew', [len(x) for x in got.split('\n')],
                      [len(x) for x in ragged.split('\n')])

# Bottom of the shape is EOF.
no_bottom = (
    '┌───┐\n'
    '│   │'
)
got, _, _ = flood(no_bottom, 1, 2)
check('EOF is the missing bottom wall', got, (
    '┌───┐\n'
    '│▒▒▒│'
))

# Left side of the shape is column 0.
no_left = (
    '────┐\n'
    '    │\n'
    '────┘'
)
got, _, _ = flood(no_left, 1, 0)
check('column 0 is the missing left wall', got, (
    '────┐\n'
    '▒▒▒▒│\n'
    '────┘'
))

# Top of the shape is BOF.
no_top = (
    '│   │\n'
    '└───┘'
)
got, _, _ = flood(no_top, 0, 2)
check('BOF is the missing top wall', got, (
    '│▒▒▒│\n'
    '└───┘'
))

print('\nflood fill — leaks and walls')

# A gap in the right wall, with the way out plugged by already-painted cells.
blocked = (
    '┌───┐  \n'
    '│   │  \n'
    '│    ▒▒\n'
    '└───┘  '
)
got, _, _ = flood(blocked, 1, 2)
check('existing brush chars wall off the gap', got, (
    '┌───┐  \n'
    '│▒▒▒│  \n'
    '│▒▒▒▒▒▒\n'
    '└───┘  '
))

# The same gap, unplugged:  the fill escapes and takes the outside with it.
leaky = (
    '┌───┐  \n'
    '│   │  \n'
    '│      \n'
    '└───┘  '
)
got, _, _ = flood(leaky, 1, 2)
check('leaks through an open gap', got, (
    '┌───┐▒▒\n'
    '│▒▒▒│▒▒\n'
    '│▒▒▒▒▒▒\n'
    '└───┘▒▒'
))

tabbed = '│ \t │'
got, msg, _ = flood(tabbed, 0, 1)
check('tab is a wall', got, '│▒\t │')

print('\nflood fill — refusals leave the buffer untouched')

got, msg, _ = flood(box, 0, 0)
check('caret on a wall: unchanged', got, box)
check('caret on a wall: message', msg, 'Box Drawing:  nothing to fill here.')

got, msg, _ = flood(box, 1, 5)
check('caret past EOL: unchanged', got, box)
check('caret past EOL: message', msg, 'Box Drawing:  nothing to fill here.')

got, msg, _ = flood('', 0, 0)
check('empty buffer: unchanged', got, '')
check('empty buffer: message', msg, 'Box Drawing:  nothing to fill here.')

print('\nflood fill — replace and clear')

filled = (
    '┌───┐\n'
    '│▒▒▒│\n'
    '│▒▒▒│\n'
    '└───┘'
)

# Seed on an existing fill, with a different brush:  re-shade it.
got, msg, _ = flood(filled, 1, 2, brush_id=FillBrushID.DARK_SHADE)
check('re-shades an already-filled area', got, (
    '┌───┐\n'
    '│▓▓▓│\n'
    '│▓▓▓│\n'
    '└───┘'
))
check('re-shade reports the new brush', msg, 'Box Drawing:  filled 6 cells with ▓')

# Seed on an existing fill with no brush selected:  clear it.
got, msg, _ = flood(filled, 1, 2, brush_id=FillBrushID.NONE)
check('clears a filled area back to spaces', got, (
    '┌───┐\n'
    '│   │\n'
    '│   │\n'
    '└───┘'
))
check('clear reports cleared', msg, 'Box Drawing:  cleared 6 cells')
check('clear is length-preserving', len(got), len(filled))

# Clearing only takes the connected run of that one character.
mixed = (
    '┌─────┐\n'
    '│▒▒░░░│\n'
    '└─────┘'
)
got, _, _ = flood(mixed, 1, 1, brush_id=FillBrushID.NONE)
check('clear stops at a different fill character', got, (
    '┌─────┐\n'
    '│  ░░░│\n'
    '└─────┘'
))

got, _, _ = flood(mixed, 1, 3, brush_id=FillBrushID.FULL_BLOCK)
check('re-shade stops at a different fill character', got, (
    '┌─────┐\n'
    '│▒▒███│\n'
    '└─────┘'
))

# No-ops:  the region already holds the target character.
got, msg, _ = flood(filled, 1, 2, brush_id=FillBrushID.MEDIUM_SHADE)
check('same brush: unchanged', got, filled)
check('same brush: message', msg, 'Box Drawing:  already filled with ▒')

got, msg, _ = flood(box, 1, 2, brush_id=FillBrushID.NONE)
check('clearing bare space: unchanged', got, box)
check('clearing bare space: message', msg, 'Box Drawing:  nothing to clear here.')

# Text and box-drawing characters still cannot be seeded.
got, msg, _ = flood(filled, 0, 2, brush_id=FillBrushID.DARK_SHADE)
check('box character cannot be seeded', got, filled)
check('box character: message', msg, 'Box Drawing:  nothing to fill here.')

words = 'hello world'
got, msg, _ = flood(words, 0, 1, brush_id=FillBrushID.DARK_SHADE)
check('text cannot be seeded', got, words)

# ...but the space between words can, and it stops at the words.
got, _, _ = flood(words, 0, 5, brush_id=FillBrushID.DARK_SHADE)
check('the space between words fills', got, 'hello▓world')


big = '\n'.join([' ' * 40] * 40)          # 1600 fillable cells
got, msg, _ = flood(big, 10, 10, budget=100)
check('over budget: buffer untouched', got, big)
check('over budget: message', msg, 'Box Drawing:  fill area exceeds 100 cells;  nothing filled.')

got, msg, _ = flood(big, 10, 10, budget=100000)
check('within budget: all 1600 cells filled', got.count('▒'), 1600)
check('within budget: length preserved', len(got), len(big))


print('\nflood fill — caret is restored')
_, _, view = flood(box, 1, 2)
check('caret still at (1,2)', view.rowcol(view.sel()[0].b), (1, 2))

print('\nflood fill — the menu caption explains itself')

def caption(text, row, col, state=None, sel_count=1, selected=False, sheet_id=1):
    """Build a View in a given condition and ask the command for its caption."""
    view = sublime.View(text, sheet_id=sheet_id)
    core.set_drawing_state(view, core.State.ON if state else core.State.OFF)
    pt = view.text_point(row, col)
    view.sel().clear()
    if selected:
        view.sel().add(sublime.Region(pt, pt + 1))
    else:
        view.sel().add(pt)
    if sel_count > 1:
        view.sel().add(view.text_point(row, col + 2))
    cmd = BoxDrawingFloodFillCommand(view)
    return cmd.description(), cmd.is_enabled()

text = '┌───┐\n│   │\n└───┘'

cap, enabled = caption(text, 1, 2, state=True)
check('drawing ON, one caret: plain caption', cap, 'Flood Fill')
check('drawing ON, one caret: enabled', enabled, True)

cap, enabled = caption(text, 1, 2, state=False)
check('drawing OFF: caption says to turn it on', cap,
      'Flood Fill  (turn Box Drawing ON first)')
check('drawing OFF: disabled', enabled, False)

cap, enabled = caption(text, 1, 2, state=True, selected=True)
check('text selected: caption says why', cap,
      'Flood Fill  (needs one caret, with nothing selected)')
check('text selected: disabled', enabled, False)

cap, enabled = caption(text, 1, 2, state=True, sel_count=2)
check('multiple carets: caption says why', cap,
      'Flood Fill  (needs one caret, with nothing selected)')
check('multiple carets: disabled', enabled, False)

cap, _ = caption(text, 1, 2, state=True, sheet_id=0)
check('panel/overlay view: caption says to turn it on', cap,
      'Flood Fill  (turn Box Drawing ON first)')




# -------------------------------------------------------------------------
# Status text
# -------------------------------------------------------------------------
print('\nstatus bar')

character_set = _module('src.character_set')

character_set.set_current_character_set(character_set.CharacterSetID.UNICODE_ROUND_CORNERS, False)

view = sublime.View('hello')
fill_brush.set_current_brush(FillBrushID.NONE, False)

core.set_state_off(view)
check('OFF: field erased', view.get_status('box_drawing'), '')
check('OFF: persistent text empty', core.status_text(view), '')

core.set_state_on(view)
check('ON: field set', view.get_status('box_drawing'),
      'Box Drawing ON (Unicode [Round Corners])')

fill_brush.set_current_brush(FillBrushID.RIGHT_HALF, False)
core.refresh_status(view)
check('ON + brush: field shows fill', view.get_status('box_drawing'),
      'Box Drawing ON (Unicode [Round Corners]) | Fill: ▐')

del sublime.messages[:]
core.refresh_status(view)
check('refresh_status flashes nothing', sublime.messages, [])

core.notify_status(view)
check('notify_status flashes once', len(sublime.messages), 1)

core.set_state_off(view)
check('OFF again: field erased even with a brush', view.get_status('box_drawing'), '')


# -------------------------------------------------------------------------
print()
if failures:
    print(f'{len(failures)} of {checks[0]} checks FAILED:\n')
    for f in failures:
        print(' -', f)
    sys.exit(1)

print(f'All {checks[0]} checks passed.')
