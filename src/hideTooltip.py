"""
Disclaimer: I know this is bad code

This code hides "Warning, cloze deletions will not work until you switch
the type at the top to Cloze." kind of tooltips. This tooltip is handled
on `Editor._onCloze`. Editor._onCloze searches for cloze signature on the
card model with  `re.search`, and if the signature is not found it calls
tooltip with the message above.

1.  Directly replacing _onCloze may break compatibility with other addons
    modifying _onClose function, so that is not an option
2.  We cannot hook `tooltip` function itself  since it is imported directly
    from 'aqt/editor.py', not being indirected with module imports. Of
    cousre we 'can' with help of hyper-complex function metadata / bytecode
    fiddling, but it seems like a massive overkill.

So for alternative measure we hook the following if statement by hooking
`re.search` function, This is hookable, since the `editor.py` code imports
`search` function indirectly via `import re`.

    if not re.search("{{(.*:)*cloze:", self.note.model()["tmpls"][0]["qfmt"]):
        if self.addMode:
            tooltip(
                _("Warning, cloze deletions will not work ...")
            )
        else:
            showInfo(
                _("To make a cloze deletion on an existing note,  ...")
            )
            return

"""

from aqt.editor import Editor
from anki.hooks import wrap
from .modelFinder import getBasicNoteTypeList
import re


def _onClozeNew(self, *, _old):
    basicNoteTypes = getBasicNoteTypeList()
    currentModelName = self.note.model()["name"]
    shouldHookReSearch = (currentModelName in basicNoteTypes) and (not self.addMode)

    if shouldHookReSearch:
        hookReSearch()

    rets = _old(self)

    if shouldHookReSearch:
        unhookReSearch()

    return rets


_oldReSearch = None
_clozeCheckerRegex = "{{(.*:)*cloze:"


def hookReSearch():
    global _oldReSearch

    # Hook this template
    # if not re.search("{{(.*:)*cloze:", self.note.model()["tmpls"][0]["qfmt"]):
    def newSearch(pattern, string, flags=0, *, _old):
        if pattern == _clozeCheckerRegex:
            return True
        return _old(pattern, string, flags)

    _oldReSearch = re.search
    re.search = wrap(re.search, newSearch, "around")


def unhookReSearch():
    global _oldReSearch
    if _oldReSearch:
        re.search = _oldReSearch
        _oldReSearch = None
