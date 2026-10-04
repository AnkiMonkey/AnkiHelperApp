@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PY=python
where python >nul 2>nul || set PY=py
echo Kontrolujem kniznice...
%PY% -m pip install --quiet --disable-pip-version-check -r requirements.txt
if errorlevel 1 (
  echo.
  echo Python sa nenasiel alebo instalacia zlyhala. Nainstaluj Python z python.org ^(zaskrtni "Add to PATH"^).
  pause
  exit /b 1
)
%PY% anki_gui.py
if errorlevel 1 pause
