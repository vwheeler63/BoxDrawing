import sublime_plugin
import sublime
from ...lib.debug import IntFlag, DebugBit, is_debugging
from .. import core
from .. import box_character


class BoxDrawingToggleCharacterSetCommand(sublime_plugin.TextCommand):
    """ Toggle box-drawing character set between ASCII and Unicode. """

    def description(self):
        """ Provide caption for associated menu item when it does not have
            a "caption" entry, or it is empty.
        """
        if box_character.is_ascii_mode():
            curr_char_set = 'ASCII'
        else:
            curr_char_set = 'Unicode'

        return f'Toggle Box Drawing Character Set ({curr_char_set})'

    def run(self, edit):
        """
        Toggle box-drawing character set between ASCII and Unicode.

        :param self:  BoxDrawingToggleCharacterSetCommand object connected to current View
        :param edit:  sublime.Edit connected to current View, needed to edit Buffer
        :return:  None
        """
        debugging = is_debugging(DebugBit.COMMANDS)
        if box_character.is_ascii_mode():
            box_character.set_unicode_mode(debugging)
        else:
            box_character.set_ascii_mode(debugging)

        # Confirm change was actually made.
        if box_character.is_ascii_mode():
            sublime.status_message('Box Drawing:  ASCII')
        else:
            sublime.status_message('Box Drawing:  Unicode')
