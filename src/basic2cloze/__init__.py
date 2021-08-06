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

from .modelFinder import get_basic_note_type_list, get_cloze_note_type

def convert_basic_to_cloze(problem, note):
    if not (
        note._note_type['name'] in get_basic_note_type_list() and 
        problem == tr.adding_cloze_outside_cloze_notetype()
    ):
        return problem

    if not get_cloze_note_type():
        tooltip("[Automatic Basic to Cloze] Cannot find target 'Cloze' model")
        return problem

    if note['Back'] != "":
        return "[Automatic Basic to Cloze] 'Back' must be empty"

    text = note['Front']
    note.__init__(mw.col, get_cloze_note_type())
    note['Text'] = text

    return None
gui_hooks.add_cards_will_add_note.append(convert_basic_to_cloze)


def change_notetype_from_cloze_to_basic_in_addcards_dialog(addcards: AddCards):
    try:
        if addcards.notetype_chooser.selected_notetype_id == get_cloze_note_type()['id']:
            addcards.notetype_chooser.selected_notetype_id = get_basic_note_type_list()[0]['id']
            addcards.notetype_chooser.show()
    except Exception as e:
        print(e)
        pass # don't cause an error when note types are missing or this code becomes outdated
gui_hooks.add_cards_did_init.append(change_notetype_from_cloze_to_basic_in_addcards_dialog)

