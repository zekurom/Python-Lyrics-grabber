@echo off
python -m pip install -U nuitka
python -m pip install zstandard
python -m pip install ordered-set
set "currentDirectory=%cd%"
for /f "skip=1 delims=" %%A in (
  'wmic computersystem get name'
) do for /f "delims=" %%B in ("%%A") do set "compName=%%A"


cd /D %currentDirectory%
start "Builder" /B /D "%currentDirectory%" /REALTIME /WAIT "python" -m nuitka --onefile --windows-disable-console --windows-icon-from-ico=Soup.ico --enable-plugin=numpy --enable-plugin=tk-inter Main.py
pause