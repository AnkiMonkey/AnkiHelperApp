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

rem 1. pokus: GUI s oknom
%PY% anki_gui.py
if not errorlevel 1 exit /b 0

rem 2. pokus: GUI spadlo -^> konzolova verzia
echo.
echo ==================================================
echo  GUI sa nepodarilo spustit, chyba je vypisana vyssie.
echo  Spustam konzolovu verziu (anki_app.py)...
echo ==================================================
echo.
%PY% anki_app.py
pause
