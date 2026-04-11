from ...boxdrawing import reload
from ...lib.debug import IntFlag, DebugBits, is_debugging

debugging = is_debugging(DebugBits.IMPORTING)
if debugging:
    print(f'  {__package__}  >>> module execution')

reload(__package__, ('draw_one_char', 'toggle_drawing', 'change_char_set'))

from .draw_one_char import BoxDrawingDrawOneCharacterCommand
from .toggle_drawing import BoxDrawingToggleDrawingCommand
from .change_char_set import BoxDrawingChangeCharacterSetCommand

__all__ = [
    'BoxDrawingDrawOneCharacterCommand',
    'BoxDrawingToggleDrawingCommand',
    'BoxDrawingChangeCharacterSetCommand',
]

if debugging:
    print(f'  {__package__}  <<<')
