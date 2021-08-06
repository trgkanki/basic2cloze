from anki.hooks import addHook
from aqt import mw
from aqt.utils import tooltip, tr

_basic_note_types = []
_cloze_note_types = []


def get_models():
    """Prepare note type"""
    global _basic_note_types
    global _cloze_note_types

    _basic_note_types = [mw.col.models.by_name(x) for x in ["Basic", tr.notetypes_basic_name()] if x]
    _cloze_note_types = [mw.col.models.by_name(x) for x in ["Cloze", tr.notetypes_cloze_name()] if x]

    if not _basic_note_types:
        tooltip("[Automatic Basic to Cloze] Cannot find source 'Basic' model")

    if not _cloze_note_types:
        tooltip("[Automatic Basic to Cloze] Cannot find target 'Cloze' model")


addHook("profileLoaded", get_models)


def get_basic_note_types():
    return _basic_note_types


def get_cloze_note_types():
    return _cloze_note_types
