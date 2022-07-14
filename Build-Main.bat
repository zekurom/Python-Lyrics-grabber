python -m pip install -U nuitka
python -m pip install ordered-set
python -m nuitka --onefile --windows-icon-from-ico=Soup.ico ----windows-icon-template-exe=Soup.ico --enable-plugin=numpy --enable-plugin=tk-inter Main.py