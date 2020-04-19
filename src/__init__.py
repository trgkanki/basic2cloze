# -*- mode: Python ; coding: utf-8 -*-
#
# Copyright © 2017 Hyun Woo Park (phu54321@naver.com)
#
# Lots of code from "Quick note and deck buttons" written by Roland Sieker
#
# Provenance from original plugin.
#   The idea, original version and large parts of this code
#   written by Steve AW <steveawa@gmail.com>
#
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#

from aqt import mw
from aqt.addcards import AddCards
from anki.hooks import wrap
from anki.hooks import addHook, runHook
from aqt.utils import tooltip
from anki.lang import _

from .modelFinder import (
    getBasicNoteTypeList,
    getClozeNoteType
)
from .modelChanger import changeModelTo

import re
from typing import Union

def targetModelSelector(note) -> Union[str, None]:
    if note.model()['name'] not in getBasicNoteTypeList():
        return None

    # Basic cloze type
    for name, val in note.items():
        if re.search(r'\{\{c(\d+)::', val):
            return getClozeNoteType()

    # None for no-change
    return None


def newAddCards(self, _old):
    note = self.editor.note
    targetModelName = targetModelSelector(note)
    if targetModelName:
        oldModelName = None

        def cb1():
            nonlocal oldModelName
            oldModelName = note.model()['name']
            changeModelTo(self.modelChooser, targetModelName)
            self.editor.saveNow(cb2)

        def cb2():
            nonlocal oldModelName
            self._addCards()
            changeModelTo(self.modelChooser, oldModelName)
            tooltip(_('[Basic2Cloze] %s -> %s' %
                      (oldModelName, targetModelName)))

        self.editor.saveNow(cb1)
    else:
        return _old(self)


AddCards.addCards = wrap(AddCards.addCards, newAddCards, "around")
