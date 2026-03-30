import sublime_plugin
from ...lib.debug import IntFlag, DebugBit, is_debugging
from .. import core


class BoxDrawingTurnOffCommand(sublime_plugin.TextCommand):
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
        return core.is_state_active(self.view)


    def run(self, edit):
        """
        Set BoxDrawing Package to ON mode.

        :param self:        BoxDrawingTurnOffCommand object connected to current View
        :param edit:        sublime.Edit passed by Sublime Text connected to current View
        :return:  None
        """
        debugging = is_debugging(DebugBit.COMMANDS)
        if debugging:
            print('In BoxDrawingTurnOffCommand()...')

        core.set_state_off(self.view)
