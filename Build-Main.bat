@echo off
python -m pip install -U nuitka
python -m pip install zstandard
python -m pip install ordered-set
set "currentDirectory=%cd%"
for /f "skip=1 delims=" %%A in (
  'wmic computersystem get name'
) do for /f "delims=" %%B in ("%%A") do set "compName=%%A"

set /p ver=What app version?  
cd /D %currentDirectory%
set "splash=%cd%\Splash-Screen.png"
start "Builder" /B /D "%currentDirectory%" /REALTIME /WAIT "python" -m nuitka --onefile --onefile-windows-splash-screen-image="%splash%" --windows-product-version=%ver% --windows-product-name="Python App" --windows-company-name="SnakeWorks" --windows-disable-console --windows-icon-from-ico=Soup.ico --enable-plugin=numpy --enable-plugin=tk-inter App.py
pause