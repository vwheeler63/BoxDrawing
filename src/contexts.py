""" -----------------------------------------------------------------------
ProComment Package Context Events
----------------------------------------------------------------------- """
from typing import Union
import sublime
import sublime_plugin
from ..lib.debug import DebugBits, is_debugging
from . import core
from . import fill_brush


class BoxDrawingContextEventListener(sublime_plugin.ViewEventListener):
    """
    Called when Sublime Text sees a key binding context key it does not recognize.

    Context keys implemented here:

    +-----------------------------+--------------------------------------+
    | Key                         | True when                            |
    +=============================+======================================+
    | box_drawing.ok_to_draw      | Sheet-attached View, box drawing ON, |
    |                             | one caret, nothing selected.         |
    +-----------------------------+--------------------------------------+
    | box_drawing.is_on           | Sheet-attached View, box drawing ON. |
    |                             | Deliberately looser than             |
    |                             | ``ok_to_draw``:  selecting a fill    |
    |                             | brush edits nothing, so it need not  |
    |                             | care about the selection.            |
    +-----------------------------+--------------------------------------+
    | box_drawing.ok_to_paint     | ``ok_to_draw`` AND a fill brush is   |
    |                             | selected.  Not used by this          |
    |                             | Package's own key bindings --        |
    |                             | flood fill deliberately works with   |
    |                             | no brush too, where it clears        |
    |                             | instead of filling -- but provided   |
    |                             | for users writing their own          |
    |                             | paint-mode-only bindings.            |
    +-----------------------------+--------------------------------------+
    """

    def on_activated(self):
        """
        Called when this View gains focus.

        The fill brush is global while the status bar field is per View, so
        the field is brought up to date here.  ``core.refresh_status()`` is
        used rather than ``core.notify_status()`` on purpose:  this is a
        passive event, and flashing a transient message every time the user
        switches tabs would be noise, and would stomp on whatever message
        the status line was already showing.
        """
        core.refresh_status(self.view)

    def on_query_context(
            self,
            key      : str,
            operator : sublime.QueryOperator,
            operand  : Union[bool, str, int],
            match_all: bool
            ):
        """
        Called when determining whether to trigger a key binding with the given context
        key.  If the plugin knows how to respond to the context, it should return
        either ``True`` of ``False``.  If the context is unknown, it should
        return ``None``.

        :param self:       BoxDrawingContextEventListener object; self.view == target View
        :param key:        Context key to query. This generally refers to specific
                             state held by a plugin (i.e. what is being tested).
        :param operator:   Operator to check against the operand; whether to
                             check equality, inequality, etc.
                             (default: sublime.QueryOperator.EQUAL)
        :param operand:    Value against which to check using the ``operator``.
                             (default: "true")
        :param match_all:  Indicate whether the context of all carets
                             (selections) must comply with validity criteria.
                             (default: True)
        :returns: ``True`` or ``False`` if the plugin handles this context key
                  and it either does or doesn't match.  If context is unknown
                  return ``None``.
        """
        result = None
        debugging = is_debugging(DebugBits.QUERY_CONTEXT_EVENT)

        if debugging:
            print('In on_query_context()')
            print(f'  {key=}')
            print(f'  {operator=}')
            print(f'  {operand=}')
            print(f'  {type(operand)=}')
            print(f'  {match_all=}')

        if key in (
                'box_drawing.ok_to_draw',
                'box_drawing.is_on',
                'box_drawing.ok_to_paint',
                ):
            result = False

            rhs = bool(operand)

            if key == 'box_drawing.ok_to_draw':
                lhs = core.ok_to_do_box_drawing(self.view, debugging)
            elif key == 'box_drawing.is_on':
                lhs = core.is_state_active_in_sheet(self.view)
            else:  # key == 'box_drawing.ok_to_paint'
                lhs = ((
                            core.ok_to_do_box_drawing(self.view, debugging)
                        and fill_brush.is_brush_active()
                        ))

            if debugging:
                print(f'  {lhs=}')

            if operator == sublime.QueryOperator.EQUAL:
                result = ((lhs == rhs))
            elif operator == sublime.QueryOperator.NOT_EQUAL:
                result = ((lhs != rhs))

        if debugging:
            print(f'  on_query_context() result[{result}]')

        return result
