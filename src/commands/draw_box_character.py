import sublime_plugin
from sublime import Region
from enum import IntFlag, IntEnum
from ...lib.debug import DebugBit, is_debugging


class BoxDrawingDirection(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class BoxDrawingDrawBoxCharacterCommand(sublime_plugin.TextCommand):
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
            print('In BoxDrawingDrawBoxCharacterCommand()...')
            print(f'  {line_count=}')
            print(f'  {direction=}')
