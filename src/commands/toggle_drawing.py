import sublime_plugin
from ...lib.debug import IntFlag, DebugBit, is_debugging
from .. import core


class BoxDrawingToggleDrawingCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        """
        Determine whether associated menu item is enabled.

        Returning `False` from `is_enabled()` queries that were mapped to commands
        apparently used to have a down side that it would block Sublime Text from
        continuing to look for other possible key bindings to use.  However, testing
        with build 4200 shows that this is no longer the case when there is also an
        ``on_query_context()`` also active and functioning properly.  When BoxDrawing
        is turned OFF for a particular View, [Alt+Left] and [Alt+Right] still perform
        their default bindings:  move by sub-words.

        Since the inherited implementation of `is_enabled()` returns `True`,
        this method could be removed without consequence.
        """
        return True


    def is_checked(self):
        """ Determine whether a checkmark appears next to menu item. """
        return core.is_state_active(self.view)


    # def description(self):
    #     """ Provide caption for associated menu item when it does not have
    #         a "caption" entry, or it is empty.
    #     """
    #     result = 'Turn Box Drawing ON'

    #     if core.is_state_active(self.view):
    #         result = 'Turn Box Drawing OFF'

    #     return result


    def run(self, edit):
        """
        Set BoxDrawing Package to ON mode.

        :param self:        BoxDrawingTurnOnCommand object connected to current View
        :param edit:        sublime.Edit passed by Sublime Text connected to current View
        :return:  None
        """
        debugging = is_debugging(DebugBit.COMMANDS)
        if debugging:
            print('In BoxDrawingToggleDrawingCommand()...')

        core.toggle_state(self.view)
