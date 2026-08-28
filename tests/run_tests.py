"""
BoxDrawing Test Runner
======================

Runs the Package's tests outside of Sublime Text.

    python tests/run_tests.py

The tests import the Package's own modules against the stub `sublime` and
`sublime_plugin` modules in ``tests/stubs/``, which implement just enough of
the Sublime Text API for this Package's logic to run:  a View over a plain
string buffer, Regions, Selections, Settings and the status bar.

That covers everything in the Package that is pure logic -- character
classification, fill brushes, painting and flood fill -- which is the part
worth having automated.  It does not and cannot cover key binding contexts,
menu rendering or anything else that only a live editor can answer.

Exit status is 0 when every check passes, 1 otherwise.
"""
import os
import subprocess
import sys


HERE = os.path.dirname(os.path.abspath(__file__))

TESTS = [
    'test_fill.py',
    'test_paint.py',
]


def main():
    # The test output is full of box-drawing and block characters, which a
    # Windows console will not encode by default.
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    failed = []

    for name in TESTS:
        print(f'\n{"=" * 72}\n{name}\n{"=" * 72}')
        result = subprocess.run(
                [sys.executable, os.path.join(HERE, name)],
                env=env
                )
        if result.returncode != 0:
            failed.append(name)

    print(f'\n{"=" * 72}')

    if failed:
        print('FAILED: ' + ', '.join(failed))
        return 1

    print(f'All {len(TESTS)} test modules passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
