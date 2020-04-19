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

from aqt.addcards import AddCards
from anki.hooks import wrap

from .modelFinder import modelExists
from .modelSelector import targetModelSelector
from .modelChanger import changeModelTo

import re

def newAddCards(self, _old):
    note = self.editor.note
    oldModelName = None
    targetModelName = None

    def cb1():
        nonlocal oldModelName, targetModelName

        targetModelName = targetModelSelector(note)
        if not modelExists(targetModelName):
            targetModelName = None

        if targetModelName is None:
            return _old(self)

        oldModelName = note.model()['name']
        changeModelTo(self.modelChooser, targetModelName)
        self.editor.saveNow(cb2)

    def cb2():
        nonlocal oldModelName
        self._addCards()
        changeModelTo(self.modelChooser, oldModelName)

    self.editor.saveNow(cb1)



AddCards.addCards = wrap(AddCards.addCards, newAddCards, "around")
