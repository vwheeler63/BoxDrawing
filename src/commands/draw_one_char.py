import sublime_plugin
from sublime import Region
from enum import IntFlag, IntEnum
from ...lib.debug import DebugBit, is_debugging
from .. import core


class BoxDrawingDirection(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class BoxDrawingDrawOneCharacterCommand(sublime_plugin.TextCommand):
    def is_enabled(self) -> bool:
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
        return core.is_state_active()


    def run(self, edit, line_count: int, direction: BoxDrawingDirection):
        """
        Draw box character with specified line count in specified direction.

        :param edit:        sublime.View.Edit
        :param direction:   Direction drawing will proceed (see BoxDrawingDirection)
        :param line_count:  0 = erase, 1 = single, 2 = double
        :return:  None
        """
        debugging = is_debugging(DebugBit.COMMANDS)
        if debugging:
            print('In BoxDrawingDrawOneCharacterCommand()...')
            print(f'  {line_count=}')
            print(f'  {direction=}')
