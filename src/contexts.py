""" -----------------------------------------------------------------------
ProComment Package Context Events
----------------------------------------------------------------------- """
from typing import Union
import sublime
import sublime_plugin
from ..lib.debug import IntFlag, DebugBit, is_debugging
from . import core


class BoxDrawingContextEventListener(sublime_plugin.ViewEventListener):
    """
    Called when Sublime Text sees a key binding context key it does not recognize.
    """
    def on_query_context(
            self,
            key      : str,
            operator : sublime.QueryOperator,
            operand  : Union[bool, str, int],
            match_all: bool
            ):
        """
        Called when determining to trigger a key binding with the given context
        key.  If the plugin knows how to respond to the context, it should return
        either ``True`` of ``False``.  If the context is unknown, it should
        return ``None``.

        :param self:       ViewEventListener object; self.view == target View
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
        debugging = is_debugging(DebugBit.QUERY_CONTEXT_EVENT)

        if debugging:
            print('In on_query_context()')
            print(f'  {key=}')
            print(f'  {operator=}')
            print(f'  {operand=}')
            print(f'  {type(operand)=}')
            print(f'  {match_all=}')

        if key == 'box_drawing.ok_to_draw':
            result = False

            rhs = bool(operand)

            # ---------------------------------------------------------------------
            # Is there only 1 selection (caret)?
            # And state = ON?
            # ---------------------------------------------------------------------
            if debugging:
                print(f'  {core.g_state=}')
                print(f'  is_state_active()=>[{core.is_state_active()}]')

            lhs = core.ok_to_do_box_drawing(self.view)

            if debugging:
                print(f'  {lhs=}')

            if operator == sublime.QueryOperator.EQUAL:
                result = ((lhs == rhs))
            elif operator == sublime.QueryOperator.NOT_EQUAL:
                result = ((lhs != rhs))

        if debugging:
            print(f'  result[{result}]')

        return result
