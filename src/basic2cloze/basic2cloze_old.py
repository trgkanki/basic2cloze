# -*- coding: utf-8 -*-
#
# basic2cloze v20.5.4i8
#
# Lots of code from "Quick note and deck buttons" written by Roland Sieker
#
# Provenance from original plugin.
#   The idea, original version and large parts of this code
#   written by Steve AW <steveawa@gmail.com>
#
# Copyright: trgk (phu54321@naver.com)
# License: GNU AGPL, version 3 or later;
# See http://www.gnu.org/licenses/agpl.html

from anki.hooks import wrap
from aqt.addcards import AddCards
from aqt.editor import Editor

from .hideTooltip import _onClozeNew
from .modelChanger import changeModelTo
from .modelSelector import target_model

def main():
    def newAddCards(self, _old):
        note = self.editor.note
        oldModelName = None
        targetModelName = None

        def cb1():
            nonlocal oldModelName, targetModelName

            target_model_ = target_model(note)
            if not target_model_:
                return _old(self)

            targetModelName = target_model_['name']
            oldModelName = note.model()["name"]
            changeModelTo(self.modelChooser, targetModelName)
            self.editor.saveNow(cb2)

        def cb2():
            nonlocal oldModelName
            self._addCards()
            changeModelTo(self.modelChooser, oldModelName)

        self.editor.saveNow(cb1)


    AddCards.addCards = wrap(AddCards.addCards, newAddCards, "around")
    Editor._onCloze = wrap(Editor._onCloze, _onClozeNew, "around")
