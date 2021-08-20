import re

from aqt import mw

from .modelFinder import get_basic_note_type_ids, get_cloze_note_type_ids

clozeHideAllType = "Cloze (Hide all)"


def target_model(note):
    if note.note_type()['id'] not in get_basic_note_type_ids():
        return None

    # Cloze (Hide All) type
    for _, val in note.items():
        if re.search(r"\{\{c(\d+)::!", val):
            return clozeHideAllType

    # Basic cloze type
    for _, val in note.items():
        if re.search(r"\{\{c(\d+)::", val):
            return mw.col.models.get(get_cloze_note_type_ids()[0]) if get_cloze_note_type_ids() else None

    # None for no-change
    return None
