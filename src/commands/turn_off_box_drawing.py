import sublime_plugin
from ...lib.debug import IntFlag, DebugBit, is_debugging
from ..core import set_state_idle


class BoxDrawingTurnOffBoxDrawingCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        """
        Set BoxDrawing Package to ACTIVE mode.

        :param self:        BoxDrawingTurnOnBoxDrawingCommand object connected to current View
        :param edit:        sublime.Edit passed by Sublime Text connected to current View
        :return:  None
        """
        debugging = is_debugging(DebugBit.COMMANDS)
        if debugging:
            print('In BoxDrawingTurnOffBoxDrawingCommand()...')

        set_state_idle()
