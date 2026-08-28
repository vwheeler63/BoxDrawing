r"""
Flood Fill
==========

Fills the region connected to the caret with the currently selected fill
brush -- or clears it, when no brush is selected.


The Region
==========

A cell is one literal character in the Buffer, addressed as (row, col).

The region is the set of cells connected to the caret, in the four cardinal
directions, that hold the SAME character as the cell under the caret.  That
character is the "seed".  Every cell in the region is replaced with the
current brush character, or with a space when no brush is selected.

This gives three operations out of one algorithm:

+-------------------+----------------+---------------------------------+
| Seed              | Brush          | Result                          |
+===================+================+=================================+
| ' '  (space)      | e.g. ▓         | fill an empty area              |
+-------------------+----------------+---------------------------------+
| e.g. ▒            | e.g. ▓         | re-shade an already-filled area |
+-------------------+----------------+---------------------------------+
| e.g. ▓            | none           | clear a filled area back to     |
|                   | ([Ctrl-Alt-0]) | spaces                          |
+-------------------+----------------+---------------------------------+


What May Be Seeded
==================

The seed must be a space or one of the fill brush characters.  Anything
else -- text, box-drawing characters, tabs -- cannot be seeded, and the
command declines with a message.

That restriction is the whole reason this command is safe to press.
Without it, a flood on a box border would happily replace every connected
box-drawing character in the drawing, and a flood inside a word would eat
the word.  Neither is ever what the user meant by "fill".

Note that this cuts both ways:  characters that cannot be seeded also
cannot be overwritten, because a cell only joins the region when it holds
the seed character.  A box drawn around an area still bounds the fill
exactly as it did when this command only knew about spaces.


Boundaries Are Walls
====================

The edges of the document and the end of each line bound the region, no
differently than a character that does not match the seed.  Two
consequences, both intended:

- The region is always finite.  Every row's spread stops at that row's own
  EOL, and rows stop at the first and last rows of the Buffer, so the
  region can never exceed the number of characters in the document.  There
  is no longest-line computation and no way for a fill to escape into the
  "virtual space" to the right of a line.

- Document edges are legitimate enclosing sides.  A shape does not have to
  be closed by drawn characters on all four sides:  a box flush against the
  right edge of the document fills correctly, because EOL finishes what the
  missing wall would have.  The same goes for a shape at the top or bottom
  of the Buffer, or one whose left side is column 0.

Note that this is the exact opposite of what ``_virtual_char_at()`` in
``draw_one_char.py`` does.  That helper deliberately reports virtual space
as ' ' for the benefit of line drawing, which is allowed to extend the
Buffer.  Flood fill must not extend the Buffer, so it reads the Buffer
through ``_real_char_at()`` below instead.


All or Nothing
==============

Every way this command can decline to do its job leaves the Buffer
completely untouched:

- the seed cannot be seeded          -> nothing to fill here
- the seed already IS the brush      -> nothing to change
- the region exceeds the budget      -> too large

A half-filled document is worse than an unfilled one, and there is no
partial state for the user to undo.  A fill that does happen is a single
``Edit``, and therefore a single undo step.

Because every cell in the region holds exactly one character and is
replaced by exactly one character, a fill is always length-preserving:  no
line changes length, no Buffer offset shifts, and no line is ever padded.
"""
from collections import deque
from typing import Dict, Optional
import sublime
import sublime_plugin
from sublime import View
from ...lib.debug import DebugBits, is_debugging
from .. import core
from .. import fill_brush


# Returned by `_real_char_at()` for any cell that is not part of a line's
# text:  above BOF, below EOF, left of column 0, or at/past EOL.  Chosen so
# that it can never equal a real Buffer character, and therefore can never
# match a seed.
_cfg_wall = '\x00'

# What the region is replaced with when no fill brush is selected.
_cfg_clear_character = ' '


def _line_text(view: View, row: int, last_row: int, cache: Dict[int, str]) -> Optional[str]:
    """
    Text of `row`, without its line ending;  ``None`` if `row` is outside
    the Buffer.

    Each row is read from the Buffer at most once per command run.  After
    that, every cell test on that row is an index into a string.

    :param view:      current View
    :param row:       row wanted
    :param last_row:  last row in the Buffer
    :param cache:     row -> line text, accumulated across this run
    """
    if row < 0 or row > last_row:
        return None

    result = cache.get(row)

    if result is None:
        bol_pt = view.text_point(row, 0)
        result = view.substr(view.line(bol_pt))
        cache[row] = result

    return result


def _real_char_at(view: View, row: int, col: int, last_row: int, cache: Dict[int, str]) -> str:
    """
    Literal Buffer character at (`row`,`col`), or ``_cfg_wall`` when
    (`row`,`col`) is not part of a line's text.

    Unlike ``draw_one_char._virtual_char_at()``, this reports NOTHING for
    virtual space:  past EOL is a wall, not a space.
    """
    if col < 0:
        return _cfg_wall

    line_text = _line_text(view, row, last_row, cache)

    if line_text is None or col >= len(line_text):
        return _cfg_wall

    return line_text[col]


def _can_be_seeded(c: str) -> bool:
    """
    May a flood fill start on character `c`?

    Only spaces and the fill brush characters.  See "What May Be Seeded" in
    the module docstring for why this is deliberately narrow.
    """
    return ((c == ' ' or fill_brush.is_brush_character(c)))


class BoxDrawingFloodFillCommand(sublime_plugin.TextCommand):
    """ Fill, re-shade or clear the region connected to the caret. """

    def is_enabled(self) -> bool:
        """
        Determine whether the associated menu item is enabled.

        Note that this deliberately does NOT require a fill brush to be
        selected:  with no brush, this command clears a filled region back
        to spaces, which is a useful thing to be able to do while in
        ordinary line-drawing mode.
        """
        debugging = is_debugging(DebugBits.COMMANDS)
        return core.ok_to_do_box_drawing(self.view, debugging)

    def description(self, **kwargs) -> str:
        """
        Provide the caption for the associated menu item.

        A greyed-out menu item that does not say why it is greyed out is a
        small mystery for the user to solve.  This command has two quite
        different reasons for being unavailable, so the caption says which
        one is in force rather than leaving the user to guess.

        Debugging is deliberately passed as ``False`` to
        ``ok_to_do_box_drawing()``:  this runs every time the menu is
        opened, and it is not worth a page of console output.
        """
        view = self.view

        if not core.is_state_active_in_sheet(view):
            return 'Flood Fill  (turn Box Drawing ON first)'

        if not core.ok_to_do_box_drawing(view, False):
            return 'Flood Fill  (needs one caret, with nothing selected)'

        return 'Flood Fill'

    def run(self, edit):
        """
        Fill, re-shade or clear the region connected to the caret.

        :param self:  BoxDrawingFloodFillCommand object connected to current View
        :param edit:  sublime.Edit connected to current View, needed to edit Buffer
        :return:  None

        Algorithm:
        ==========

        A.  Read the caret cell:  the "seed".  If it is not a space and not
            a brush character, it cannot be seeded:  report and return
            without editing.

        B.  Work out what the region will be replaced with:  the current
            brush character, or a space when no brush is selected.  If that
            is already the seed character, there is nothing to do:  report
            and return without editing.

        C.  Breadth-first, 4-connected traversal (up, right, down, left --
            no diagonals) over cells holding the seed character,
            accumulating `visited`.  Cells that do not match, including EOL
            and the edges of the Buffer, bound the traversal, so it always
            terminates.

        D.  If `visited` exceeds the ``max_flood_cells`` budget, abandon the
            whole operation without editing.

        E.  Group the visited cells by row and rewrite one line at a time.
            One character replaces one character, so the fill is
            length-preserving:  no line changes length, no Buffer offset
            shifts, and no line is ever padded.

            Rows are still rewritten bottom-up out of caution, though with
            length preserved the order does not affect correctness.

        F.  Restore the caret, which rewriting its line would otherwise
            have moved.
        """
        debugging = is_debugging(DebugBits.COMMANDS | DebugBits.FILL_BRUSH)
        if debugging:
            print('In BoxDrawingFloodFillCommand()...')

        view          = self.view
        live_sel_list = view.sel()
        caret_pt      = live_sel_list[0].b
        row, col      = view.rowcol(caret_pt)
        last_row, _   = view.rowcol(view.size())
        cache         = {}   # row -> line text

        # ---------------------------------------------------------------------
        # A.  What is under the caret, and may it be seeded?
        # ---------------------------------------------------------------------
        seed = _real_char_at(view, row, col, last_row, cache)

        if debugging:
            print(f'  {row=}')
            print(f'  {col=}')
            print(f'  {last_row=}')
            print(f'  {seed=}')

        if not _can_be_seeded(seed):
            if debugging:
                print('  Caret is not on a space or a fill brush character.')
            sublime.status_message('Box Drawing:  nothing to fill here.')
            return

        # ---------------------------------------------------------------------
        # B.  What replaces it?
        # ---------------------------------------------------------------------
        target = fill_brush.current_brush_char() or _cfg_clear_character
        clearing = ((target == _cfg_clear_character))

        if debugging:
            print(f'  {target=}')
            print(f'  {clearing=}')

        if seed == target:
            if debugging:
                print('  Region already holds the target character.')
            if clearing:
                sublime.status_message('Box Drawing:  nothing to clear here.')
            else:
                sublime.status_message(f'Box Drawing:  already filled with {target}')
            return

        # ---------------------------------------------------------------------
        # C.  Traverse.
        # D.  Respect the budget.
        # ---------------------------------------------------------------------
        max_cells = core.max_flood_cells()
        visited   = {(row, col)}
        frontier  = deque(visited)

        while frontier:
            r, c = frontier.popleft()

            for neighbor in ((r - 1, c), (r, c + 1), (r + 1, c), (r, c - 1)):
                if neighbor in visited:
                    continue
                if _real_char_at(view, neighbor[0], neighbor[1], last_row, cache) != seed:
                    continue

                visited.add(neighbor)

                if len(visited) > max_cells:
                    if debugging:
                        print(f'  Budget of {max_cells} cells exceeded.  Nothing filled.')
                    sublime.status_message(
                        f'Box Drawing:  fill area exceeds {max_cells} cells;  nothing filled.'
                        )
                    return

                frontier.append(neighbor)

        if debugging:
            print(f'  {len(visited)} cells to fill.')

        # ---------------------------------------------------------------------
        # E.  Rewrite one line at a time, bottom-up.
        # ---------------------------------------------------------------------
        columns_by_row = {}
        for r, c in visited:
            columns_by_row.setdefault(r, []).append(c)

        for r in sorted(columns_by_row, reverse=True):
            characters = list(cache[r])

            for c in columns_by_row[r]:
                characters[c] = target

            bol_pt   = view.text_point(r, 0)
            line_rgn = view.line(bol_pt)
            view.replace(edit, line_rgn, ''.join(characters))

        # ---------------------------------------------------------------------
        # F.  Restore the caret.
        # ---------------------------------------------------------------------
        live_sel_list.clear()
        live_sel_list.add(caret_pt)

        if clearing:
            sublime.status_message(f'Box Drawing:  cleared {len(visited)} cells')
        else:
            sublime.status_message(f'Box Drawing:  filled {len(visited)} cells with {target}')
