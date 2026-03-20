from ..boxdrawing import reload
from .debug import IntFlag, DebugBit, is_debugging
from .utils import sublime_submodule_name

submodule_name = sublime_submodule_name(__file__, 2)
debugging = is_debugging(DebugBit.IMPORTING)
if debugging:
    print(f'{submodule_name}  >>> module execution')

reload(submodule_name, ('debug', 'utils'))

from . import utils

__all__ = [
    'debug',
    'utils'
]

if debugging:
    print(f'{submodule_name}  <<<')
