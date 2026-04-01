from ..boxdrawing import reload
from .debug import IntFlag, DebugBit, is_debugging

debugging = is_debugging(DebugBit.IMPORTING)
if debugging:
    print(f'{__package__}  >>> module execution')

reload(__package__, ('debug', 'utils'))

from . import utils

__all__ = [
    'debug',
    'utils'
]

if debugging:
    print(f'{__package__}  <<<')
