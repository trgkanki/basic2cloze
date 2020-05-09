from aqt import mw
from anki.hooks import addHook
from aqt.utils import tooltip
from anki.lang import _


def modelExists(model_name):
    return bool(mw.col.models.byName(model_name))


_basicNoteTypeList = []
_clozeNoteType = None


def _findModelName():
    """Prepare note type"""
    global _basicNoteTypeList
    global _clozeNoteType

    _basicNoteTypeList = list(filter(modelExists, ["Basic", _("Basic")]))
    clozeNoteTypeList = list(filter(modelExists, ["Cloze", _("Cloze")]))

    if not _basicNoteTypeList:
        tooltip("[Automatic basic to cloze] Cannot find source 'Basic' model")
        _basicNoteTypeList = []

    if not clozeNoteTypeList:
        tooltip("[Automatic basic to cloze] Cannot find target 'Cloze' model")
        _clozeNoteType = None

    else:
        _clozeNoteType = clozeNoteTypeList[0]


addHook("profileLoaded", _findModelName)


def getBasicNoteTypeList():
    return _basicNoteTypeList


def getClozeNoteType():
    return _clozeNoteType
