# Checklist to Add New Character Set

1.  Modify list at top of `character_set.py`.

2.  Build and append new character set to `character_set._g_character_sets` in the correct sequence.

3.  Modify `character_set.CharacterSetID` enumeration class.
    - Add enumeration name and value to match new sequence.
    - Ensure LAST enumeration contains value of new last value.

4.  Modify `BoxDrawing.sublime-settings`:
    - documentation of `CharacterSetID` class (lists valid values for setting);
    - `default_character_set_id` setting integer to match whatever integer is now associated with ASCII.

5.  Open the console window ([Ctrl-\`])

6.  Reload the Package (can be done by saving `boxdrawing.py`).  Observe in the Console Panel that there are no error messages.

7.  Test by turning ON and OFF Box Drawing and use key binding to progress through new list of character sets.  Check status bar and `Tools > BoxDrawing` submenu to ensure the names are as intended.

8.  Test actual drawing to confirm things are coming out as intended.  Fix if not.
