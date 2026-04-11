from ..boxdrawing import reload
from ..lib.debug import IntFlag, DebugBits, is_debugging

debugging = is_debugging(DebugBits.IMPORTING)
if debugging:
    print(f'{__package__}  >>> module execution')

reload(__package__, ('core','contexts', 'character_set'))
reload(__package__ + '.commands')  # Recurse into .commands/ subpackage.

from . import core
from .contexts import *
from .commands import *

__all__ = [
    'core',

    # events/contexts
    "BoxDrawingContextEventListener",

    # commands/*
    "BoxDrawingDrawOneCharacterCommand",
    'BoxDrawingToggleDrawingCommand',
    'BoxDrawingChangeCharacterSetCommand',
]

if debugging:
    print(f'{__package__}  <<<')
