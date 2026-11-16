@echo off
setlocal

REM Build script for PES 6 Editor 2027
REM Target: Python 3.8.10 32-bit, PyInstaller 4.10, Windows 7 32-bit compatibility target.

REM Do not overwrite existing output unexpectedly.
if exist dist\PES6Editor2027\PES6Editor2027.exe (
    echo ERROR: Output already exists: dist\PES6Editor2027\PES6Editor2027.exe
    echo Delete the file or choose another output name before building.
    exit /b 1
)

python -c "import struct; import sys; print(struct.calcsize('P') * 8)" > __tmp_arch.txt
set /p PYARCH=<__tmp_arch.txt
if "%PYARCH%" NEQ "32" (
    echo ERROR: Python is not 32-bit. Install Python 3.8.10 32-bit and try again.
    del __tmp_arch.txt
    exit /b 1
)

del __tmp_arch.txt

python -m pip install PyInstaller==4.10

set PYTHONPATH=src
python -m PyInstaller --clean --windowed --onefile --name PES6Editor2027 --paths src src\pes6_editor\app.py

if exist dist\PES6Editor2027.exe (
    echo Build complete.
    echo Output: dist\PES6Editor2027.exe
    echo NOTE: Windows 7 compatibility is not guaranteed until the EXE is tested there.
    exit /b 0
)

echo ERROR: Build did not create the expected executable.
exit /b 1
