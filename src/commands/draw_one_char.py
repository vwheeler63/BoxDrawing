import sublime_plugin
import sublime
from sublime import Region, View
from sublime_types import Point
from ...lib.debug import IntFlag, DebugBit, is_debugging
from .. import core
from ..core import Direction, State


up_char = ' '
rt_char = ' '
dn_char = ' '
lf_char = ' '
up_ln_cnt = 0
rt_ln_cnt = 0
dn_ln_cnt = 0
lf_ln_cnt = 0


def _append_spaces_if_needed(view: View, edit, row: int, col: int, debugging: bool):
    """
    Append spaces to `row` if it does not yet have `col`.
    `row` is clamped to 1 past last actual row in buffer.

    :param view:       View of interest
    :param edit:       View's edit (required to change Buffer)
    :param row:        row being examined; may not be negative
    :param col:        column being examined; may not be negative
    :param debugging:  Are we debugging?
    :returns:  space_count

    @pre row >= 0, non-negative row
    @pre col >= 0, non-negative col
    @pre row can be at most last row + 1.
    """
    if debugging:
        print('In _append_spaces_if_needed()')
        print(f'  {row=}')
        print(f'  {col=}')

    assert row >= 0, f'Expected non-negative row, got {row}.'
    assert col >= 0, f'Expected non-negative col, got {col}.'

    last_pt = view.size()
    last_row, last_col = view.rowcol(last_pt)

    # Does row exist?
    if row > last_row:
        # row does not exist yet.
        if debugging:
            print(f'  Row {row} does not exist yet.')
        view.insert(edit, last_pt, '\n' + ' ' * (col + 1))
    else:
        # row exists.  Does col exist?
        if debugging:
            print(f'  Row {row} exists.')
        bol_pt = view.text_point(row, 0)
        line_rgn = view.line(bol_pt)   # Region without line ending
        line_len = line_rgn.b - line_rgn.a

        if col > line_len:
            # col is past EOL.
            if debugging:
                print(f'  Col {col} is past EOL.  Inserting {col - line_len + 1} spaces.')
            view.insert(edit, line_rgn.b, ' ' * (col - line_len + 1))
        elif col == line_len:
            # col is at EOL.
            if debugging:
                print(f'  Col {col} is at EOL.  Inserting 1 space.')
            view.insert(edit, line_rgn.b, ' ')
        else:
            if debugging:
                print(f'  Col {col} exists.')


def _virtual_char_at(view: View, row: int, col: int) -> str:
    """
    Character at (row,col).

    :param view:       current View
    :param row:        row being examined
    :param col:        column being examined
    :param debugging:  Are we debugging?

    :returns:
        - char at (row,col) (can be '\n' when (row,col) is at EOL and not EOF);
        - ' ' if is in "virtual space" (to right of text in a line or beyond EOF), and
        - '\x00' if above or to the left of Buffer boundaries.
    """
    result = '\x00'

    if row >= 0 and col >= 0:
        result = ' '
        last_pt = view.size()
        real_pt = view.text_point(row, col, clamp_column=True)

        if real_pt < last_pt:
            unk_pt = view.text_point(row, col, clamp_column=False)

            if unk_pt == real_pt:
                result = view.substr(real_pt)

    return result


def _look_around(view: View, row: int, col: int, debugging: bool):
    """
    Populate `XX_char` and `XX_ln_cnt` based on chars around `row` and `col`.
    """
    global up_char
    global rt_char
    global dn_char
    global lf_char
    global up_ln_cnt
    global rt_ln_cnt
    global dn_ln_cnt
    global lf_ln_cnt

    debugging = is_debugging(DebugBit.BOX_DRAWING)
    if debugging:
        print('In _look_around()...')
        print(f'  {row=}')
        print(f'  {col=}')

    up_char = _virtual_char_at(view, row - 1, col    )
    rt_char = _virtual_char_at(view, row    , col + 1)
    dn_char = _virtual_char_at(view, row + 1, col    )
    lf_char = _virtual_char_at(view, row    , col - 1)

    if debugging:
        print('  _look_around() results')
        print(f'  {up_char=}')
        print(f'  {rt_char=}')
        print(f'  {dn_char=}')
        print(f'  {lf_char=}')

    up_ln_cnt = core.line_count(up_char, Direction.DOWN , debugging)
    rt_ln_cnt = core.line_count(rt_char, Direction.LEFT , debugging)
    dn_ln_cnt = core.line_count(dn_char, Direction.UP   , debugging)
    lf_ln_cnt = core.line_count(lf_char, Direction.RIGHT, debugging)


def _move_caret(view: View, edit, row: int, col: int, direction: Direction, debugging: bool):
    """
    Move caret from (`row`,`col`) in `direction`; add spaces as needed.
    Do not move if UP is requested on row 0, or LEFT in col 0.
    Only move on recognized directions.

    @pre row and col must be valid.
    @pre (Direction.UP <= direction <= Direction.LEFT)

    :returns  resulting (row, col); movement may not have been possible.
    """
    assert (Direction.UP <= direction <= Direction.LEFT), f'`Direction` {direction} not recognized.'

    if debugging:
        print('In _move_caret()')
        print(f'  {row=}')
        print(f'  {col=}')
        print(f'  {direction=}')

    do_move = False

    if direction == Direction.UP:
        if row > 0:
            row -= 1
            do_move = True
    elif direction == Direction.RIGHT:
        col += 1
        do_move = True
    elif direction == Direction.DOWN:
        row += 1
        do_move = True
    elif direction == Direction.LEFT:
        if col > 0:
            col -= 1
            do_move = True

    if do_move:
        _append_spaces_if_needed(view, edit, row, col, debugging)

        # Move selection to (row,col).
        pt = view.text_point(row, col)
        sel_list = view.sel()
        sel_list.clear()
        sel_list.add(pt)

    return row, col


def _compute_and_place_drawing_char(
        view          : View,
        edit          : sublime.Edit,
        row           : int,
        col           : int,
        new_line_count: int,
        direction     : Direction,
        debugging     : bool
        ):
    """
    Compute character:
        - use surrounding chars to assemble a characterization
        - use characterization to index into the appropriate lookup array:
            - One of these 2 arrays will be referenced by
              glst_box_char_lookup_by_characterization:
                - glst_unicode_box_char_lookup_by_characterization
                - glst_ascii_box_char_lookup_by_characterization

    Uses globals:

        up_ln_cnt
        rt_ln_cnt
        dn_ln_cnt
        lf_ln_cnt

    Note that the ``Direction`` IntEnum class is carefully ordered to so that
    each ``side`` can be used to compute the number of bits to shift to place
    the least 2 significant bits into their respective bit fields.

        UP    = 0   # << 1 = number of bits to shift
        RIGHT = 1   # << 1 = number of bits to shift
        DOWN  = 2   # << 1 = number of bits to shift
        LEFT  = 3   # << 1 = number of bits to shift

    :param view:            current View
    :param row:             target row
    :param col:             target column
    :param new_line_count:  number of lines indicated by user's key combination
                              1, 2 or 0 = erase
    :param direction:       direction indicated by user's key combination
                              (one of the ``Direction`` enumerators)
    :param debugging:       Are we debugging?
    """
    global up_ln_cnt
    global rt_ln_cnt
    global dn_ln_cnt
    global lf_ln_cnt

    _look_around(view, row, col, debugging)

    up_shift_amt = Direction.UP    << 1
    rt_shift_amt = Direction.RIGHT << 1
    dn_shift_amt = Direction.DOWN  << 1
    lf_shift_amt = Direction.LEFT  << 1

    if up_ln_cnt + rt_ln_cnt + dn_ln_cnt + lf_ln_cnt == 0:
        # We're starting fresh---no surrounding box-drawing characters.
        if direction == Direction.UP or direction == Direction.DOWN:
            up_ln_cnt = new_line_count
            dn_ln_cnt = new_line_count
        elif direction == Direction.RIGHT or direction == Direction.LEFT:
            rt_ln_cnt = new_line_count
            lf_ln_cnt = new_line_count
    else:
        # There is at least one surrounding box-drawing character.  Now we
        # compute how `direction` and `new_line_count` are going to influence that.
        if direction == Direction.UP:
            up_ln_cnt = new_line_count
        elif direction == Direction.RIGHT:
            rt_ln_cnt = new_line_count
        elif direction == Direction.DOWN:
            dn_ln_cnt = new_line_count
        elif direction == Direction.LEFT:
            lf_ln_cnt = new_line_count

    up_bit_field = up_ln_cnt << up_shift_amt
    rt_bit_field = rt_ln_cnt << rt_shift_amt
    dn_bit_field = dn_ln_cnt << dn_shift_amt
    lf_bit_field = lf_ln_cnt << lf_shift_amt

    characterization = up_bit_field | rt_bit_field | dn_bit_field | lf_bit_field

    c = core.glst_box_char_lookup_by_characterization[characterization]

    # Replace `cur_char` with computed character.
    pt = view.text_point(row, col)
    dest_char_rgn = Region(pt, pt + 1)
    cur_char = view.substr(dest_char_rgn)

    # Insert if at EOL, replace otherwise.
    if cur_char == '\n':
        view.insert(edit, pt, c)
        # Move caret back to where it was.
        sel_list = view.sel()
        sel_list.clear()
        sel_list.add(pt)
    else:
        view.replace(edit, dest_char_rgn, c)


class BoxDrawingDrawOneCharacterCommand(sublime_plugin.TextCommand):

    def __init__(self, view):
        """ Add box-drawing state to View's settings. """
        super().__init__(view)
        # self.view is now attached to ``view``.
        view_settings = view.settings()
        view_settings.set(core.cfg_view_box_drawing_state_key, State.OFF)
        view_settings.set(core.cfg_view_box_drawing_last_direction_key, Direction.NONE)

    def is_enabled(self) -> bool:
        """
        Determine whether associated menu item is enabled.

        Returning `False` from `is_enabled()` queries that were mapped to commands
        apparently used to have a down side that it would block Sublime Text from
        continuing to look for other possible key bindings to use.  However, testing
        with build 4200 shows that this is no longer the case when there is also an
        ``on_query_context()`` also active and functioning properly.  When BoxDrawing
        is turned OFF for a particular View, [Alt+Left] and [Alt+Right] still perform
        their default bindings:  move by sub-words.
        """
        debugging = is_debugging(DebugBit.BOX_DRAWING)
        return core.ok_to_do_box_drawing(self.view, debugging)

    def run(self, edit, line_count: int, direction: Direction):
        """
        Draw box character with specified line count in specified direction.

        :param edit:        sublime.Edit object, needed for editing Buffer
        :param direction:   Direction drawing will proceed (see Direction)
        :param line_count:  0 = erase, 1 = single, 2 = double
        :return:  None


        Algorithm:
        ==========

        A.  Box-drawing ONLY applies if:
            - box drawing is ON,
            - there is a single selection (caret), and
            - no text is selected.

        B.  Terms:
            - A single caret with no text selected gives us the concept of a single
              "current character":  `cur_char`.

            - `src_char` is `cur_char` before optional movement.

            - `dest_char` is `cur_char` after optional movement.

        C.  last_drawing_direction == Direction.NONE after:
            - BoxDrawing Package is loaded, and
            - box drawing is turned OFF.

        D.  last_drawing_direction = direction of previous box-draw operation, (UP|RIGHT|DOWN|LEFT)
            or NONE if op = ERASE.

        E.  If no movement takes place, `src_char` and `dest_char` point to
            same character.

        F.  If `src_char` is not a box-drawing character, then no movement takes place.
            The cursor stays in place to write the single box-drawing character
            indicated by the key combination.

        G.  If `src_char` is a box-drawing character, but line exiting character on side
            of indicated movement does agree with line count, no movement takes place.
            The cursor stays in place to write the single box-drawing character
            indicated by the key combination.

        H.  If direction changes, no movement takes place.
            The cursor stays in place to write the single box-drawing character
            indicated by the key combination.

        I.  Movement takes place when:
            - drawing continues in same direction
            - AND `src_char` is a box-drawing character
            - AND line exiting char on side of indicated movement agrees with line count.

        J.  `dest_char` has the characters around it examined by calling `look_around()`.
            (See below for details on what this populates.)

        K.  `dest_char` is made to "fit in" (i.e. connect with) the box-drawing
            characters around it, taking into account the indicated direction.

        L.  Enhancement to save keystrokes, as well as gracefully finishing box corners:

            L.1.  When arriving at a box corner that will be finished, compute
                  character to just finish the box corner, but not extend it.

            L.2.  When the last op caused a box-drawing character to be created
                  (e.g. which closed the corner of a box) such that proceeding in the
                  same direction does not find an "agreeing" line count on the side
                  of the character in the indicated direction, then movement DOES
                  occur and the `src_char` is "back adjusted" to add the exiting
                  line to the box-drawing character already there.


        Pseudocode to carry out above algorithm:
        ========================================

        if line_count == 0:  # erase:
            write SPACE at current location
            move in `direction`
            last_drawing_direction = Direction.NONE
        else:
            if same_direction and `src_char` is a box-drawing character:
                move in `direction`:
                    - If char does not exist in that direction, add enough spaces to
                      end of line so that a space character exists there to support
                      a "view.replace()" on that character.
                    - Move selection to that character.

            last_drawing_direction = direction of keypress

            look_around()  # "involved" means "on side of cur_char".
                - populate:
                    - up_char = char above (char above line 0 = None)
                    - dn_char = char below
                    - lf_char = char on left (char left of col 0 = None)
                    - rt_char = char on right
                    - up_ln_cnt = 0=not a box char, 1=1 vert line involved, 2=2 vert lines involved.
                    - dn_ln_cnt = 0=not a box char, 1=1 vert line involved, 2=2 vert lines involved.
                    - lf_ln_cnt = 0=not a box char, 1=1 horiz line involved, 2=2 horiz lines involved.
                    - rt_ln_cnt = 0=not a box char, 1=1 horiz line involved, 2=2 horiz lines involved.

            If condition (L) above (same direction and disagreeing existing line):
                "back adjust" `src_char`.

            Compute character based on surrounding characters:
                - use surrounding chars to assemble a characterization
                - use characterization to index into the appropriate lookup array:
                    - One of these 2 arrays will be referenced by
                      glst_box_char_lookup_by_characterization:
                        - glst_unicode_box_char_lookup_by_characterization
                        - glst_ascii_box_char_lookup_by_characterization

            Replace `cur_char` with computed character.
        """
        debugging = is_debugging(DebugBit.COMMANDS | DebugBit.BOX_DRAWING)
        if debugging:
            print('In BoxDrawingDrawOneCharacterCommand()...')
            print(f'  {line_count=}')
            print(f'  {direction=}')

        view = self.view
        view_settings = view.settings()
        view_settings.get(core.cfg_view_box_drawing_state_key)
        last_drawing_direction = view_settings.get(core.cfg_view_box_drawing_last_direction_key)
        live_sel_list = view.sel()
        src_caret_rgn = live_sel_list[0]
        src_char_pt   = src_caret_rgn.b
        src_char_rgn  = Region(src_char_pt, src_char_pt + 1)

        # if line_count == 0:  # erase:
        #     write SPACE at current location
        #     move in `direction`
        #     last_drawing_direction = Direction.NONE
        if line_count == 0:
            # Erase.
            if debugging:
                print('Erase...')
            view.replace(edit, src_char_rgn, ' ')
            _move_caret(direction)
            last_drawing_direction = Direction.NONE
            view_settings.set(core.cfg_view_box_drawing_last_direction_key, last_drawing_direction)
        else:
            # Draw something.
            row, col = view.rowcol(src_char_pt)
            if debugging:
                if line_count > 1:
                    plural_suffix = 's'
                else:
                    plural_suffix = ''
                print(f'Draw {line_count} line{plural_suffix}...')
                print(f'  {row=}')
                print(f'  {col=}')
            # if same_direction and `src_char` is a box-drawing character:
            if last_drawing_direction == direction:
                if debugging:
                    print('  Same direction.')
                # move in `direction`:
                #     - If char does not exist in that direction, add enough spaces to
                #       end of line so that a space character exists there to support
                #       a "view.replace()" on that character.
                #     - Move selection to that character.
                row, col = _move_caret(view, edit, row, col, direction, debugging)

            # last_drawing_direction = direction of keypress
            last_drawing_direction = direction
            view_settings.set(core.cfg_view_box_drawing_last_direction_key, last_drawing_direction)

            # look_around()  # "involved" means "on side of cur_char".
            #     - populates:
            #         - up_char = char above (char above line 0 = None)
            #         - dn_char = char below
            #         - lf_char = char on left (char left of col 0 = None)
            #         - rt_char = char on right
            #         - up_ln_cnt = 0=not a box char, 1=1 vert line involved, 2=2 vert lines involved.
            #         - dn_ln_cnt = 0=not a box char, 1=1 vert line involved, 2=2 vert lines involved.
            #         - lf_ln_cnt = 0=not a box char, 1=1 horiz line involved, 2=2 horiz lines involved.
            #         - rt_ln_cnt = 0=not a box char, 1=1 horiz line involved, 2=2 horiz lines involved.
            #
            # If condition (L.2) above (same direction and disagreeing existing line):
            #     "back adjust" `src_char`.
            #
            # Compute character:
            #     - use surrounding chars to assemble a characterization
            #     - use characterization to index into the appropriate lookup array:
            #         - One of these 2 arrays will be referenced by
            #           `glst_box_char_lookup_by_characterization`:
            #             - glst_unicode_box_char_lookup_by_characterization
            #             - glst_ascii_box_char_lookup_by_characterization
            _compute_and_place_drawing_char(
                    view,
                    edit,
                    row,
                    col,
                    line_count,
                    direction,
                    debugging
                    )
