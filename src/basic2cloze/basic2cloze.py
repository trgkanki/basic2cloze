import re

from aqt import gui_hooks, mw
from aqt.addcards import AddCards
from aqt.utils import KeyboardModifiersPressed, tooltip, tr

from .modelFinder import get_basic_note_types, get_cloze_note_types
from .modelSelector import target_model


def main():
    def convert_basic_to_cloze(problem, note):
        if not (
            note._note_type in get_basic_note_types() and
            problem == tr.adding_cloze_outside_cloze_notetype()
        ):
            return problem

        if not target_model(note):
            tooltip("[Automatic Basic to Cloze] Cannot find target 'Cloze' model")
            return problem

        old_model = mw.col.models.get(note.mid)
        front = note[old_model['flds'][0]['name']]
        back = note[old_model['flds'][1]['name']]

        new_model = target_model(note)
        note.__init__(mw.col, new_model)
        note[new_model['flds'][0]['name']] = front
        note[new_model['flds'][1]['name']] = back

        return None
    gui_hooks.add_cards_will_add_note.append(convert_basic_to_cloze)

    def change_notetype_from_cloze_to_basic_in_addcards_dialog(addcards: AddCards):
        try:
            if addcards.notetype_chooser.selected_notetype_id in [x['id'] for x in get_cloze_note_types()]:
                addcards.notetype_chooser.selected_notetype_id = get_basic_note_types()[
                    0]['id']
                addcards.notetype_chooser.show()
        except Exception as e:
            print(e)
            pass  # don't cause an error when note types are missing or this code becomes outdated
    gui_hooks.add_cards_did_init.append(
        change_notetype_from_cloze_to_basic_in_addcards_dialog)

    def add_cloze_shortcut_that_works_on_basic_notes(shortcuts, editor):

        # code adapted from original onCloze and _onCloze
        def myOnCloze(self):
            self.call_after_note_saved(
                lambda: _myOnCloze(editor), keepFocus=True)

        def _myOnCloze(self):
            if self.note.model() not in get_basic_note_types():
                return
            # find the highest existing cloze
            highest = 0
            for name, val in list(self.note.items()):
                m = re.findall(r"\{\{c(\d+)::", val)
                if m:
                    highest = max(highest, sorted([int(x) for x in m])[-1])
            # reuse last?
            if not KeyboardModifiersPressed().alt:
                highest += 1
            # must start at 1
            highest = max(1, highest)
            self.web.eval("wrap('{{c%d::', '}}');" % highest)

        shortcuts.append(("Ctrl+Shift+C", lambda: myOnCloze(editor)))
        shortcuts.append(("Ctrl+Shift+Alt+C", lambda: myOnCloze(editor)))

    gui_hooks.editor_did_init_shortcuts.append(
        add_cloze_shortcut_that_works_on_basic_notes)