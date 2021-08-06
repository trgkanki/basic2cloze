from anki import version as anki_version

ANKI_VERSION_TUPLE = tuple(int(i) for i in anki_version.split("."))

if ANKI_VERSION_TUPLE >= (2, 1, 45):
    from .basic2cloze import main
    main()
else:
    from .basic2cloze_old import main
    main()