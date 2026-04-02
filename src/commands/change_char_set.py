import sublime_plugin
import sublime
from ...lib.debug import IntFlag, DebugBit, is_debugging
from .. import core
from .. import character_set


class BoxDrawingChangeCharacterSetCommand(sublime_plugin.TextCommand):
    """ Toggle box-drawing character set between ASCII and Unicode. """

    def description(self):
        """ Provide caption for associated menu item when it does not have
            a "caption" entry, or it is empty.
        """
        name = character_set.current_character_set_name()
        return f'Change Character Set ({name})'

    def run(self, edit):
        """
        Toggle box-drawing character set between ASCII and Unicode.

        :param self:  BoxDrawingChangeCharacterSetCommand object connected to current View
        :param edit:  sublime.Edit connected to current View, needed to edit Buffer
        :return:  None
        """
        debugging = is_debugging(DebugBit.COMMANDS | DebugBit.CHARACTER_SET)
        character_set.advance_to_next_character_set(debugging)

        # Confirm change was actually made.
        name = character_set.current_character_set_name()

        if core.is_state_active(self.view):
            state = 'ON'
        else:
            state = 'OFF'

        sublime.status_message(f'Box Drawing {state} ({name})')
