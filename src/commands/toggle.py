import sublime_plugin
from ...lib.debug import IntFlag, DebugBit, is_debugging
from .. import core


class BoxDrawingToggleCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        """
        Determine whether associated menu item is enabled.

        Returning `False` has a down side:  If this command is mapped to a
        key combination, if this returns `False` Sublime Text will NOT
        continue looking for other possible key bindings to use.  The answer
        to this is to have this method return `True` and have
        `on_query_context()` listener make the determination.

        Since the inherited implementation of `is_enabled()` returns `True`,
        this method could be removed without consequence.
        """
        return True


    def is_checked(self):
        """ Determine whether a checkmark appears next to menu item. """
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
        Set BoxDrawing Package to ON mode.

        :param self:        BoxDrawingTurnOnCommand object connected to current View
        :param edit:        sublime.Edit passed by Sublime Text connected to current View
        :return:  None
        """
        debugging = is_debugging(DebugBit.COMMANDS)
        if debugging:
            print('In BoxDrawingTurnOffCommand()...')

        core.toggle_state()
