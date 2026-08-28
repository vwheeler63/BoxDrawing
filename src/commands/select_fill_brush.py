"""
Select Fill Brush
=================

Selects (or clears) the fill brush, switching the Package between
line-drawing mode and paint mode.

This command changes drawing mode only.  It never modifies the Buffer, and
so it never puts anything on the undo stack.
"""
import sublime_plugin
from ...lib.debug import DebugBits, is_debugging
from .. import core
from .. import character_set
from .. import fill_brush
from ..fill_brush import FillBrushID


class BoxDrawingSelectFillBrushCommand(sublime_plugin.TextCommand):
    """
    Select the fill brush identified by `brush_id`.

    ``brush_id`` 0 clears the brush and returns the Package to ordinary
    BoxDrawing line-drawing mode, preserving the active character set.
    """

    def is_checked(self, brush_id: int = FillBrushID.NONE):
        """
        Determine whether a checkmark appears next to the menu item for
        this brush.
        """
        return ((fill_brush.current_brush_id() == brush_id))

    def run(self, edit, brush_id: int = FillBrushID.NONE):
        """
        Select the fill brush identified by `brush_id`.

        :param self:      BoxDrawingSelectFillBrushCommand object connected to current View
        :param edit:      sublime.Edit connected to current View.  Deliberately
                            unused:  this command modifies no text.
        :param brush_id:  one of the ``FillBrushID`` enumerators (0-8)
        :return:  None
        """
        debugging = is_debugging(DebugBits.COMMANDS | DebugBits.FILL_BRUSH)
        if debugging:
            print('In BoxDrawingSelectFillBrushCommand()...')
            print(f'  {brush_id=}')

        view = self.view

        # Clearing the brush interrupts any line-drawing run that was in
        # progress before painting started, so forget the last direction.
        # Line drawing then starts cleanly rather than trying to continue a
        # run the user has long since walked away from.
        core.set_last_direction(view, character_set.Direction.NONE)

        fill_brush.set_current_brush(brush_id, debugging)

        core.notify_status(view)
