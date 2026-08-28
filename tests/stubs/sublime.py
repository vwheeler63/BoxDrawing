"""Minimal stand-in for Sublime Text's `sublime` module, enough to exercise
the BoxDrawing package's pure logic outside of Sublime Text."""
from enum import IntEnum


messages = []


class QueryOperator(IntEnum):
    EQUAL     = 0
    NOT_EQUAL = 1
    REGEX_MATCH = 2


class RegionFlags(IntEnum):
    NONE         = 0
    DRAW_EMPTY   = 1
    DRAW_NO_FILL = 2


class Region:
    def __init__(self, a, b=None):
        self.a = a
        self.b = a if b is None else b

    def __repr__(self):
        return f'Region({self.a}, {self.b})'


class Selection(list):
    def add(self, pt):
        if isinstance(pt, int):
            pt = Region(pt, pt)
        self.append(pt)


class View:
    """Fake View over a plain string buffer."""

    def __init__(self, text='', sheet_id=1):
        self.text = text
        self._sheet_id = sheet_id
        self._sel = Selection()
        self._settings = {}
        self._status = {}

    # -- buffer -----------------------------------------------------------
    def size(self):
        return len(self.text)

    def substr(self, x):
        if isinstance(x, Region):
            lo, hi = sorted((x.a, x.b))
            return self.text[lo:hi]
        return self.text[x:x + 1]

    def rowcol(self, pt):
        pt = max(0, min(pt, len(self.text)))
        head = self.text[:pt]
        row = head.count('\n')
        col = pt - (head.rfind('\n') + 1)
        return (row, col)

    def _line_bounds(self, row):
        lines = self.text.split('\n')
        if row < 0 or row >= len(lines):
            raise IndexError(row)
        start = 0
        for r in range(row):
            start += len(lines[r]) + 1
        return start, start + len(lines[row])

    def text_point(self, row, col, clamp_column=False):
        lines = self.text.split('\n')
        row = max(0, min(row, len(lines) - 1))
        start, end = self._line_bounds(row)
        if clamp_column:
            col = min(col, end - start)
        return min(start + col, len(self.text))

    def line(self, pt):
        if isinstance(pt, Region):
            pt = pt.b
        row, _ = self.rowcol(pt)
        start, end = self._line_bounds(row)
        return Region(start, end)

    def replace(self, edit, region, text):
        lo, hi = sorted((region.a, region.b))
        self.text = self.text[:lo] + text + self.text[hi:]

    def insert(self, edit, pt, text):
        self.text = self.text[:pt] + text + self.text[pt:]
        return len(text)

    # -- misc -------------------------------------------------------------
    def sel(self):
        return self._sel

    def sheet_id(self):
        return self._sheet_id

    def settings(self):
        return _Settings(self._settings)

    def set_status(self, key, value):
        self._status[key] = value

    def erase_status(self, key):
        self._status.pop(key, None)

    def get_status(self, key):
        return self._status.get(key, '')


class _Settings:
    def __init__(self, store):
        self._store = store

    def get(self, key, default=None):
        return self._store.get(key, default)

    def set(self, key, value):
        self._store[key] = value

    def add_on_change(self, tag, fn):
        pass

    def clear_on_change(self, tag):
        pass


class Edit:
    pass


def status_message(msg):
    messages.append(msg)


def message_dialog(msg):
    messages.append(msg)


def load_settings(name):
    return _Settings({})


def set_timeout(fn, delay=0):
    fn()
