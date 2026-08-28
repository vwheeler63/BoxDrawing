"""Minimal stand-in for Sublime Text's `sublime_plugin` module."""


class TextCommand:
    def __init__(self, view):
        self.view = view

    def run(self, edit, **kwargs):
        raise NotImplementedError


class WindowCommand:
    def __init__(self, window):
        self.window = window


class EventListener:
    pass


class ViewEventListener:
    def __init__(self, view):
        self.view = view
