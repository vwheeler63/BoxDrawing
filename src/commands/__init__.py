from ...boxdrawing import reload
from ...lib.debug import IntFlag, DebugBit, is_debugging
from ...lib.utils import sublime_submodule_name

submodule_name = sublime_submodule_name(__file__, 3)
debugging = is_debugging(DebugBit.IMPORTING)
if debugging:
    print(f'  {submodule_name}  >>> module execution')

reload(submodule_name, ('draw_box_character', 'turn_on_box_drawing',
        'turn_off_box_drawing', 'toggle_box_drawing'))

from .draw_box_character import BoxDrawingDrawBoxCharacterCommand
from .turn_on_box_drawing import BoxDrawingTurnOnBoxDrawingCommand
from .turn_off_box_drawing import BoxDrawingTurnOffBoxDrawingCommand
from .toggle_box_drawing import BoxDrawingToggleActiveCommand

__all__ = [
    'BoxDrawingDrawBoxCharacterCommand',
    'BoxDrawingTurnOnBoxDrawingCommand',
    'BoxDrawingTurnOffBoxDrawingCommand',
    'BoxDrawingToggleActiveCommand',
]

if debugging:
    print(f'  {submodule_name}  <<<')
