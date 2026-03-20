from ..boxdrawing import reload
from ..lib.debug import IntFlag, DebugBit, is_debugging
from ..lib.utils import sublime_submodule_name

submodule_name = sublime_submodule_name(__file__, 2)
debugging = is_debugging(DebugBit.IMPORTING)
if debugging:
    print(f'{submodule_name}  >>> module execution')

reload(submodule_name, ('core','contexts'))
reload(submodule_name + '.commands')  # Recurse into .commands/ subpackage.

from . import core
from .contexts import *
from .commands import *

__all__ = [
    'core',

    # events/contexts
    "BoxDrawingContextEventListener",

    # commands/*
    "BoxDrawingDrawOneCharacterCommand",
    'BoxDrawingTurnOnCommand',
    'BoxDrawingTurnOffCommand',
    'BoxDrawingToggleCommand',
]

if debugging:
    print(f'{submodule_name}  <<<')
