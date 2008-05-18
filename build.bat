rd /s /q build
rd /s /q soldemo
python -OO setup.py py2exe --b 2 --optimize 2 --dist-dir soldemo
rd /s /q build
cd soldemo
rename soldemo.db sol.db
cd ..