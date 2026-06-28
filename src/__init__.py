debugging = True
if debugging:
    print(f'{__name__}  >>> module execution....')

from . import core       # noqa: E402
from .contexts import *  # noqa: E402
from .commands import *  # noqa: E402

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
    print(f'{__name__}  <<<')
