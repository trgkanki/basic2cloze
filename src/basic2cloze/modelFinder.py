from anki.hooks import addHook
from aqt import mw
from aqt.utils import tooltip, tr

_basic_note_type_ids = []
_cloze_note_type_ids = []


def get_models():
    """Prepare note type"""
    global _basic_note_type_ids
    global _cloze_note_type_ids

    _basic_note_type_ids = [mw.col.models.by_name(x)['id'] for x in ["Basic", tr.notetypes_basic_name()] if x]
    _cloze_note_type_ids = [mw.col.models.by_name(x)['id'] for x in ["Cloze", tr.notetypes_cloze_name()] if x]

    if not _basic_note_type_ids:
        tooltip("[Automatic Basic to Cloze] Cannot find source 'Basic' model")

    if not _cloze_note_type_ids:
        tooltip("[Automatic Basic to Cloze] Cannot find target 'Cloze' model")


addHook("profileLoaded", get_models)


def get_basic_note_type_ids():
    return _basic_note_type_ids


def get_cloze_note_type_ids():
    return _cloze_note_type_ids
