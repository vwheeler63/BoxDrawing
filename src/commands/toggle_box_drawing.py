import sublime_plugin
from ...lib.debug import IntFlag, DebugBit, is_debugging
from .. import core


class BoxDrawingToggleActiveCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        """ Determine whether associated menu item is enabled. """
        return True


    def is_checked(self):
        return core.is_state_active()


    # def description(self):
    #     """ Provide caption for associated menu item when it does not have
    #         a "caption" entry, or it is empty.
    #     """
    #     result = 'Turn Box Drawing ON'

    #     if core.is_state_active():
    #         result = 'Turn Box Drawing OFF'

    #     return result


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

        core.toggle_state()
