from ...boxdrawing import reload
from ...lib.debug import IntFlag, DebugBit, is_debugging
from ...lib.utils import sublime_submodule_name

submodule_name = sublime_submodule_name(__file__, 3)
debugging = is_debugging(DebugBit.IMPORTING)
if debugging:
    print(f'  {submodule_name}  >>> module execution')

reload(submodule_name, ('draw_one_char', 'toggle_drawing', 'change_char_set'))

from .draw_one_char import BoxDrawingDrawOneCharacterCommand
from .toggle_drawing import BoxDrawingToggleDrawingCommand
from .change_char_set import BoxDrawingChangeCharacterSetCommand

__all__ = [
    'BoxDrawingDrawOneCharacterCommand',
    'BoxDrawingToggleDrawingCommand',
    'BoxDrawingChangeCharacterSetCommand',
]

if debugging:
    print(f'  {submodule_name}  <<<')
