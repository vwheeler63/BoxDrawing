"""
Menu Label
==========

A command that exists only so that a menu item can be shown greyed out.

Sublime Text greys out a menu item whose command reports
``is_enabled() == False``, so pointing a menu item at this command turns it
into a label:  visible, un-clickable, and incapable of modifying anything.

This is used for the drawing key combinations in
``Tools > BoxDrawing``, which have no single command to bind a menu item to
-- each direction is a separate invocation of
``box_drawing_draw_one_character`` with different arguments -- and so cannot
be represented as ordinary menu items at all.  Listing them as labels keeps
the key combinations discoverable from the menu, which is where a user
looks first.

Note that Sublime Text only displays a key binding next to a menu item when
a binding matches that item's command AND its arguments.  Since these
labels stand in for four bindings each (one per arrow key), the key
combination is written into the caption instead, in the same parenthesised
style already used by ``Change Character Set (ASCII)``.
"""
import sublime_plugin


class BoxDrawingMenuLabelCommand(sublime_plugin.TextCommand):
    """ Never enabled;  does nothing.  See the module docstring. """

    def is_enabled(self, **kwargs) -> bool:
        """ Always ``False``, so the menu item is always greyed out. """
        return False

    def is_visible(self, **kwargs) -> bool:
        """ Always ``True``:  greyed out, but never hidden. """
        return True

    def run(self, edit, **kwargs):
        """
        Unreachable:  Sublime Text does not run a command whose
        ``is_enabled()`` is ``False``.  Defined because a TextCommand must
        have a ``run()``.
        """
        pass
