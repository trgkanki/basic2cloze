from anki.hooks import addHook
from aqt import mw
from aqt.utils import tooltip, tr

_basicNoteTypeList = []
_clozeNoteType = None


def get_models():
    """Prepare note type"""
    global _basicNoteTypeList
    global _clozeNoteType

    _basicNoteTypeList = [mw.col.models.by_name(x) for x in ["Basic", tr.notetypes_basic_name()] if x]
    clozeNoteTypeList = [mw.col.models.by_name(x) for x in ["Cloze", tr.notetypes_cloze_name()] if x]

    if not _basicNoteTypeList:
        tooltip("[Automatic Basic to Cloze] Cannot find source 'Basic' model")
        _basicNoteTypeList = []

    if not clozeNoteTypeList:
        tooltip("[Automatic Basic to Cloze] Cannot find target 'Cloze' model")
        _clozeNoteType = None

    else:
        _clozeNoteType = clozeNoteTypeList[0]


addHook("profileLoaded", get_models)


def get_basic_note_type_list():
    return _basicNoteTypeList


def get_cloze_note_type():
    return _clozeNoteType
