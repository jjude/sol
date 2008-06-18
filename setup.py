from distutils.core import setup
import py2exe
import glob
import os


setup(
    options = {"py2exe": {"compressed": 1,
                          "optimize": 2,
                          "ascii": 1,
                          "bundle_files": 1,
                          "packages":["encodings"],
                           "excludes" : ["pywin", "pywin.debugger", "pywin.debugger.dbgcon","pywin.dialogs",
                                       "pywin.dialogs.list","Tkconstants","Tkinter","tcl"],

                            }},
    #these are the data files like templates, site media and admin media
    data_files = [(".",["soldemo.db"]),
        ("templates\\sol",glob.glob("templates\\sol\\*.*")),
        ("templates\\feeds",glob.glob("templates\\feeds\\*.*")),
        ("media\\files",glob.glob("media\\files\\sol_avatar.jpg")),
        ("media",glob.glob("media\\*.*")),
        ("media\\css",glob.glob("media\\css\\*.*")),
        ("templates\\admin",glob.glob("templates\\admin\\*.*")),
        ("templates\\admin\\auth\\user",glob.glob("templates\\admin\\auth\\user\\*.*")),
        ("templates\\admin_doc",glob.glob("templates\\admin_doc\\*.*")),
        ("templates\\widget",glob.glob("templates\\widget\\*.*")),
        ("templates\\registration",glob.glob("templates\\registration\\*.*")),
        ("media\\css",glob.glob("templates\\admin\\media\\css\*.*")),
        ("media\\js",glob.glob("templates\\admin\\media\\js\\*.*")),
        ("media\\img",glob.glob("templates\\admin\\media\\img\\*.*")),
        ],
    zipfile = None,
    console=['soldemo.py'],
    )