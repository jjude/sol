from distutils.core import setup
import py2exe
import glob
import os

#get the python path from environment variable
#it will be separated by ;
#get the first one
PYTHON_PATH=os.environ['PYTHONPATH'].split(';')[0]

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
        ("files",glob.glob("files\\*.*")),
        ("site_media",glob.glob("site_media\\*.*")),
        ("site_media\\css",glob.glob("site_media\\css\\*.*")),
        ("templates\\admin",glob.glob(PYTHON_PATH+"\\Lib\\site-packages\\django\\contrib\\admin\\templates\\admin\\*.*")),
        ("templates\\admin\\auth\\user",glob.glob(PYTHON_PATH+"\\Lib\site-packages\\django\\contrib\\admin\\templates\\admin\\auth\\user\\*.*")),
        ("templates\\admin_doc",glob.glob(PYTHON_PATH+"\\Lib\\site-packages\\django\\contrib\\admin\\templates\\admin_doc\\*.*")),
        ("templates\\widget",glob.glob(PYTHON_PATH+"\\Lib\\site-packages\\django\\contrib\\admin\\templates\\widget\\*.*")),
        ("templates\\registration",glob.glob(PYTHON_PATH+"\\Lib\\site-packages\\django\\contrib\\admin\\templates\\registration\\*.*")),
        ("adminmedia\\css",glob.glob(PYTHON_PATH+"\\Lib\\site-packages\\django\\contrib\\admin\\media\\css\*.*")),
        ("adminmedia\\js",glob.glob(PYTHON_PATH+"\\Lib\\site-packages\\django\\contrib\\admin\\media\\js\\*.*")),
        ("adminmedia\\img",glob.glob(PYTHON_PATH+"\\Lib\\site-packages\\django\\contrib\\admin\\media\\img\\*.*")),
        ],
    zipfile = None,
    console=['soldemo.py'],
    )