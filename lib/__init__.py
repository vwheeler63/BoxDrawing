from ..boxdrawing import reload
from .debug import IntFlag, DebugBits, is_debugging

debugging = is_debugging(DebugBits.IMPORTING)
if debugging:
    print(f'{__package__}  >>> module execution')

reload(__package__, ('debug'))

__all__ = [
    'debug'
]

if debugging:
    print(f'{__package__}  <<<')
