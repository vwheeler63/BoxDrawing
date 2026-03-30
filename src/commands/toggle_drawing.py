import sublime_plugin
from ...lib.debug import IntFlag, DebugBit, is_debugging
from .. import core


class BoxDrawingToggleDrawingCommand(sublime_plugin.TextCommand):
    """ Switch box-drawing state between ON and OFF. """

    def is_checked(self):
        """ Determine whether a checkmark appears next to menu item. """
        return core.is_state_active(self.view)

    def run(self, edit):
        """
        Set BoxDrawing Package to ON mode.

        :param self:        BoxDrawingToggleDrawingCommand object connected to current View
        :param edit:        sublime.Edit passed by Sublime Text connected to current View
        :return:  None
        """
        debugging = is_debugging(DebugBit.COMMANDS)
        if debugging:
            print('In BoxDrawingToggleDrawingCommand()...')

        core.toggle_state(self.view)
