debugging = True
if debugging:
    print(f'{__name__}  >>> module execution....')

from . import debug  # noqa: E402

__all__ = [
    'debug',
]

if debugging:
    print(f'{__name__}  <<<')
