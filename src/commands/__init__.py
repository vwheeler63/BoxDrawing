from ...boxdrawing import reload
from ...lib.debug import IntFlag, DebugBit, is_debugging
from ...lib.utils import sublime_submodule_name

submodule_name = sublime_submodule_name(__file__, 3)
debugging = is_debugging(DebugBit.IMPORTING)
if debugging:
    print(f'  {submodule_name}  >>> module execution')

reload(submodule_name, ('draw_one_char', 'turn_on', 'turn_off', 'toggle_drawing'))

from .draw_one_char import BoxDrawingDrawOneCharacterCommand
from .turn_on import BoxDrawingTurnOnCommand
from .turn_off import BoxDrawingTurnOffCommand
from .toggle_drawing import BoxDrawingToggleDrawingCommand

__all__ = [
    'BoxDrawingDrawOneCharacterCommand',
    'BoxDrawingTurnOnCommand',
    'BoxDrawingTurnOffCommand',
    'BoxDrawingToggleDrawingCommand',
]

if debugging:
    print(f'  {submodule_name}  <<<')
