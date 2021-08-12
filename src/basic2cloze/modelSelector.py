from .modelFinder import get_basic_note_types, get_cloze_note_types

import re


clozeHideAllType = "Cloze (Hide all)"


def target_model(note):
    if note.note_type() not in get_basic_note_types():
        return None

    # Cloze (Hide All) type
    for _, val in note.items():
        if re.search(r"\{\{c(\d+)::!", val):
            return clozeHideAllType

    # Basic cloze type
    for _, val in note.items():
        if re.search(r"\{\{c(\d+)::", val):
            return get_cloze_note_types()[0] if get_cloze_note_types() else None

    # None for no-change
    return None
