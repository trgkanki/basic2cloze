from anki.hooks import runHook


def changeModelTo(modelChooser, targetModelName):
    """Change to model with name targetModelName"""
    # Mostly just a copy and paste from the bottom of onModelChange()
    m = modelChooser.deck.models.byName(targetModelName)
    modelChooser.deck.conf["curModel"] = m["id"]
    cdeck = modelChooser.deck.decks.current()
    cdeck["mid"] = m["id"]
    modelChooser.deck.decks.save(cdeck)
    runHook("currentModelChanged")
    modelChooser.mw.reset()
