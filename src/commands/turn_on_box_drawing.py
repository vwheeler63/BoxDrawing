import sublime_plugin
from ...lib.debug import IntFlag, DebugBit, is_debugging
from .. import core


class BoxDrawingTurnOnBoxDrawingCommand(sublime_plugin.TextCommand):
    def is_enabled(self) -> bool:
        return not core.is_state_active()


    def run(self, edit):
        """
        Set BoxDrawing Package to ACTIVE mode.

        :param self:        BoxDrawingTurnOnBoxDrawingCommand object connected to current View
        :param edit:        sublime.Edit passed by Sublime Text connected to current View
        :return:  None
        """
        debugging = is_debugging(DebugBit.COMMANDS)
        if debugging:
            print('In BoxDrawingTurnOnBoxDrawingCommand()...')

        core.set_state_active()
