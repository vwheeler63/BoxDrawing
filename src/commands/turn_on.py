import sublime_plugin
from ...lib.debug import IntFlag, DebugBit, is_debugging
from .. import core


class BoxDrawingTurnOnCommand(sublime_plugin.TextCommand):
    def is_enabled(self) -> bool:
        """
        Determine whether associated menu item is enabled.

        Returning `False` has a down side:  If this command is mapped to a key
        combination (which it is not), if this returns `False` Sublime Text will
        NOT continue looking for other possible key bindings to use.  Since this
        command is not normally mapped to a key, this caveat does not apply.
        """
        return not core.is_state_active()


    def run(self, edit):
        """
        Set BoxDrawing Package to ACTIVE mode.

        :param self:        BoxDrawingTurnOnCommand object connected to current View
        :param edit:        sublime.Edit passed by Sublime Text connected to current View
        :return:  None
        """
        debugging = is_debugging(DebugBit.COMMANDS)
        if debugging:
            print('In BoxDrawingTurnOnCommand()...')

        core.set_state_active()
