from aqt import mw
from anki.hooks import addHook
from aqt.utils import tooltip
from anki.lang import _
from typing import List, Union


def _modelExists(model_name):
    return bool(mw.col.models.byName(model_name))


_basicNoteTypeList: List[str] = []
_clozeNoteType: Union[str, None] = None


def _findModelName():
    """Prepare note type"""
    global _basicNoteTypeList
    global _clozeNoteType

    _basicNoteTypeList = list(filter(_modelExists, ['Basic', _('Basic')]))
    clozeNoteTypeList = list(filter(_modelExists, ['Cloze', _('Cloze')]))

    if not _basicNoteTypeList:
        tooltip('[Automatic basic to cloze] Cannot find source \'Basic\' model')
        _basicNoteTypeList = []

    if not clozeNoteTypeList:
        tooltip('[Automatic basic to cloze] Cannot find target \'Cloze\' model')
        _clozeNoteType = None

    else:
        _clozeNoteType = clozeNoteTypeList[0]


addHook("profileLoaded", _findModelName)

def getBasicNoteTypeList() -> List[str]:
    return _basicNoteTypeList

def getClozeNoteType() -> Union[str, None]:
    return _clozeNoteType
