@echo off
setlocal

set VENV_DIR=.venv
set SCRIPT=main.py

REM Create the virtual environment if it does not exist
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
)

REM Activate the virtual environment
call "%VENV_DIR%\Scripts\activate.bat"

REM install requirements if needed
pip install -r requirements.txt

REM Run the prgram
echo Running %SCRIPT% in virtual environment...
python %SCRIPT%

endlocal