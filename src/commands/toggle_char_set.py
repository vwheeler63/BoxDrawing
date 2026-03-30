import sublime_plugin
from ...lib.debug import IntFlag, DebugBit, is_debugging
from .. import core
from .. import box_character


class BoxDrawingToggleCharacterSetCommand(sublime_plugin.TextCommand):
    """ Switch box-drawing character set (mode) between ASCII and Unicode. """

    def description(self):
        """ Provide caption for associated menu item when it does not have
            a "caption" entry, or it is empty.
        """
        if box_character.is_ascii_mode():
            curr_char_set = 'ASCII'
        else:
            curr_char_set = 'Unicode'

        return f'Toggle Box Drawing Character Set (Current: {curr_char_set})'

    def run(self, edit):
        """
        Set BoxDrawing Package to ON mode.

        :param self:        BoxDrawingToggleCharacterSetCommand object connected to current View
        :param edit:        sublime.Edit passed by Sublime Text connected to current View
        :return:  None
        """
        debugging = is_debugging(DebugBit.COMMANDS)
        if box_character.is_ascii_mode():
            box_character.set_unicode_mode(debugging)
        else:
            box_character.set_ascii_mode(debugging)
