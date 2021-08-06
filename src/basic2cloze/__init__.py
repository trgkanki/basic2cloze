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

from aqt import gui_hooks, mw
from aqt.addcards import AddCards
from aqt.utils import tooltip, tr

# the dialog for adding cards
addcards = None

# indicates if the most recent card that was added was converted from basic to cloze
# used for setting the notetype back to Basic after editor was closed and reopened
# because by default it seems to be set to the note type of the most recent added card
just_did_this = False 

def convert_basic_to_cloze(problem, note):
    global just_did_this

    if not (note._note_type['name']  == 'Basic' and problem == tr.adding_cloze_outside_cloze_notetype()):
        just_did_this = False
        return problem

    if note['Back'] != "":
        just_did_this = False
        return "Automatic Basic to Cloze: \"Back\" must be empty"

    just_did_this = True

    text = note['Front']
    note.__init__(mw.col, mw.col.models.by_name('Cloze'))
    note['Text'] = text

    return None
gui_hooks.add_cards_will_add_note.append(convert_basic_to_cloze)


def on_addcards_init(addcards: AddCards):
    global addcards_
    addcards_ = addcards

    if just_did_this:
        addcards.notetype_chooser.selected_notetype_id = mw.col.models.id_for_name('Basic')
        addcards.notetype_chooser.show()
gui_hooks.add_cards_did_init.append(on_addcards_init)

