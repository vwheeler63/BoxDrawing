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
        if character_set.is_ascii_mode():
            curr_char_set = 'ASCII'
        else:
            curr_char_set = 'Unicode'

        return f'Change Character Set ({curr_char_set})'

    def run(self, edit):
        """
        Toggle box-drawing character set between ASCII and Unicode.

        :param self:  BoxDrawingChangeCharacterSetCommand object connected to current View
        :param edit:  sublime.Edit connected to current View, needed to edit Buffer
        :return:  None
        """
        debugging = is_debugging(DebugBit.COMMANDS)
        if character_set.is_ascii_mode():
            character_set.set_unicode_mode(debugging)
        else:
            character_set.set_ascii_mode(debugging)

        # Confirm change was actually made.
        if character_set.is_ascii_mode():
            sublime.status_message('Box Drawing:  ASCII')
        else:
            sublime.status_message('Box Drawing:  Unicode')
