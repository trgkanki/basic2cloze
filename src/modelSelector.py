from .modelFinder import (
    getBasicNoteTypeList,
    getClozeNoteType
)

import re


clozeHideAllType = 'Cloze (Hide all)'

def targetModelSelector(note):
    if note.model()['name'] not in getBasicNoteTypeList():
        return None

    # Cloze (Hide All) type
    for name, val in note.items():
        if re.search(r'\{\{c(\d+)::!', val):
            return clozeHideAllType

    # Basic cloze type
    for name, val in note.items():
        if re.search(r'\{\{c(\d+)::', val):
            return getClozeNoteType()

    # None for no-change
    return None
