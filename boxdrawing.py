""" ***********************************************************************
Box Drawing
===========================================================================

Box Drawing is Sublime Text package enabling the user to use

- [Alt-Arrow]             (single line)
- [Alt-Shift-Arrow]       (double line), or
- [Ctrl-Alt-Shift-Arrow]  (erase)

to draw lines and boxes in their text like these:

┌─┬┐  ╔═╦╗  ╓─╥╖  ╒═╤╕
│ ││  ║ ║║  ║ ║║  │ ││
├─┼┤  ╠═╬╣  ╟─╫╢  ╞═╪╡
└─┴┘  ╚═╩╝  ╙─╨╜  ╘═╧╛┌─────────────┐
┌───────────────────┐ │    ╔═══════╕│            ┌───┐
│  ╔═══╗ Some Text  │ │╓───╫┐ ╔══╗ ││ ┌──┬───┐  ┌┴┬┐ │
│  ╚═╦═╝ in the box │ │║   ║│ ║  ║ ││ ╞══╡   │  ├─┼┼─┘
╞═╤══╩══╤═══════════╡ │║   ║│ ║  ║ ││ │  │   │  │ ││
│ ├──┬──┤           │ │╙───╫┘ ╚══╝ ││ └──┴───┘  └─┴┘
│ └──┴──┘           │ └────╫───────┼┘
└───────────────────┘      ╙───────┘

+-----+-+-+-+-----------------------------------------------------+
|Key  |S|C|A| Command                                             |
+=====+=+=+=+=====================================================+
|Up   | |x| | stop side-by-side editing                           |
+-----+-+-+-+-----------------------------------------------------+
|Left | |x| | deselect Sheet to the left                          |
+-----+-+-+-+-----------------------------------------------------+
|Left |x|x| | select Sheet to the left                            |
+-----+-+-+-+-----------------------------------------------------+
|Right| |x| | deselect Sheet to the right,                        |
+-----+-+-+-+-----------------------------------------------------+
|Right|x|x| | select Sheet to the right                           |
+-----+-+-+-+-----------------------------------------------------+
|PgUp | |x| | move focus to selected Sheet to the left            |
+-----+-+-+-+-----------------------------------------------------+
|PgDn | |x| | move focus to selected Sheet to the right           |
+-----+-+-+-+-----------------------------------------------------+
|j    | |x| | open message box explaining `ctrl+j` mapping change |
+-----+-+-+-+-----------------------------------------------------+

See `README.md` and `src/core.py` for more details.



@version  1.0  30-Mar-2026 17:55 vw  - Created
*********************************************************************** """
import importlib
import sys
import os
from typing import Tuple


# =========================================================================
# Data
# =========================================================================

_cfg_compressed_pkg_ext = '.sublime-package'

# Use name of parent directory as `package_name`.
module_path, _ = os.path.splitext(os.path.realpath(__file__))
parent_dir, submodule_name = os.path.split(module_path)
_, package_name = os.path.split(parent_dir)
if package_name.endswith(_cfg_compressed_pkg_ext):
    package_name = package_name[:-len(_cfg_compressed_pkg_ext)]
del _
this_module_name = f'{package_name}.{submodule_name}'
_reload_indent_level = -1

# Can't use `debugging = is_debugging(DebugBit.IMPORTING)` here because
# the import required to support it causes a circular import.
debugging = True
if debugging:
    print(f'{this_module_name}  >>> module execution')


# =========================================================================
# Load / Reload
# =========================================================================

def reload(dotted_subpkg: str, submodules: Tuple[str, ...] = ()):
    """
    Reload each module in `submodules` only if previously loaded.  This is a
    precondition of calling ``importlib.reload()`` but is also for efficiency:

    - if Sublime Text is just starting, nothing important happens here (because
      the cached modules will not have been added to ``sys.modules`` yet), and
      and the various ``import`` statements do the loading in the usual way;

    - if ``Package Control`` is updating this Package (or the central Plugin
      was just saved during development), then this function recursively
      reloads each loaded module, and the ``import`` statements then do
      nothing since each target module will already be in ``sys.modules``.

    Note:  The below works on the basis◘ that ``<sublime_data>/Packages``
           directory was placed in ``sys.path`` by Sublime Text.  So the
           module names being constructed below have to look like this:

               MyPackage.subdir.module
               MyPackage.subdir.subdir.module
               etc.

    :param dotted_subpkg:  dotted directory portion of module names that
                             will be found in the keys of ``sys.modules``.
                             Example:  'MyPackage.src.commands'
    :param submodules:     tuple of submodule names
    """
    global _reload_indent_level
    _reload_indent_level += 1
    indent = '  ' * _reload_indent_level
    if debugging:
        if _reload_indent_level == 0:
            print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
        print(f'{indent}reload():  >>> {dotted_subpkg=} {submodules=}')

    if not submodules:
        # Called from top-level Plugin.
        module_name = dotted_subpkg
        if module_name in sys.modules:
            if debugging:
                print(f'{indent}Reloading({module_name})')
            importlib.reload(sys.modules[module_name])
    else:
        # Called from subpackage.
        for submodule in submodules:
            module_name = f'{dotted_subpkg}.{submodule}'
            if module_name in sys.modules:
                if debugging:
                    print(f'{indent}Reloading({module_name})')
                importlib.reload(sys.modules[module_name])

    if debugging:
        print(f'{indent}reload():  <<<')
        if _reload_indent_level == 0:
            print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')

    _reload_indent_level -= 1


reload(package_name + '.lib')  # Recurse into .lib/ subpackage.
reload(package_name + '.src')  # Recurse into .src/ subpackage.

from .lib import *
from .src import *


# =========================================================================
# Events
# =========================================================================

def plugin_loaded():
    core.on_plugin_loaded()


def plugin_unloaded():
    core.on_plugin_unloaded()


if debugging:
    print(f'{this_module_name}  <<<')
