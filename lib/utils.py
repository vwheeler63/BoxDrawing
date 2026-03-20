""" -----------------------------------------------------------------------
General Python utilities.
----------------------------------------------------------------------- """
import os
from typing import Iterable


_cfg_compressed_pkg_ext = '.sublime-package'


def largest_string_length(items: Iterable[str]) -> int:
    """
    Length of longest string in `items`

    :param items:   Iterable of strings
    :return:  Longest length among all elements
    """
    longest_len = 0

    for s in items:
        s_len = len(s)
        if s_len > longest_len:
            longest_len = s_len

    return longest_len


def sublime_submodule_name(file_path: str, subpackage_depth: int):
    """
    Convert `file_path` to the indicated imported Python Module name.  Example
    given `subpackage_depth` == 2:

    file_path: == '/path/to/Sublime Text/Packages/ProComment/src/__init__.py'
    Result: 'ProComment.src'

    file_path: == '/path/to/Sublime Text/Packages/ProComment.sublime-package/src/__init__.py'
    Result: 'ProComment.src'

    file_path: == '/path/to/Sublime Text/Packages/ProComment/src/core.py'
    Result: 'ProComment.src.core'

    :param file_path:         `__file__` for each module calling this function.
    :param subpackage_depth:  Number of directories below `Sublime Text/Packages/`
    """
    module_list = []
    working_path, _ = os.path.splitext(file_path)

    for i in range(subpackage_depth + 1):
        remaining, submodule = os.path.split(working_path)
        include = True

        if submodule == '__init__':
            include = False
        elif i == subpackage_depth and submodule.endswith(_cfg_compressed_pkg_ext):
            submodule = submodule[:-len(_cfg_compressed_pkg_ext)]

        if include:
            module_list.append(submodule)

        working_path = remaining

    return '.'.join(reversed(module_list))


