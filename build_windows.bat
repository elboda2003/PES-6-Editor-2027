@echo off
setlocal

REM Build PES 6 Editor 2027 for Python 3.8.10 32-bit.
set "PYTHON_VERSION="
set "PYTHON_BITS="
for /f "tokens=1,2" %%A in ('python -c "import struct,sys; print('{}.{}.{} {}'.format(sys.version_info[0], sys.version_info[1], sys.version_info[2], struct.calcsize('P') * 8))" 2^>^&1') do (
    set "PYTHON_VERSION=%%A"
    set "PYTHON_BITS=%%B"
)

if not "%PYTHON_VERSION%"=="3.8.10" (
    echo ERROR: Python 3.8.10 is required. Detected: %PYTHON_VERSION%
    echo Install and activate Python 3.8.10, then run this script again.
    exit /b 1
)
if not "%PYTHON_BITS%"=="32" (
    echo ERROR: 32-bit Python is required. Detected architecture: %PYTHON_BITS%-bit
    echo Install and activate Python 3.8.10 32-bit, then run this script again.
    exit /b 1
)

set "OUTPUT_EXE=dist\PES6Editor2027\PES6Editor2027.exe"
if exist "%OUTPUT_EXE%" (
    echo ERROR: Output already exists: %OUTPUT_EXE%
    echo Move or remove that build output yourself before rebuilding.
    exit /b 1
)

python -m pip install PyInstaller==4.10
if errorlevel 1 (
    echo ERROR: Could not install PyInstaller 4.10.
    exit /b 1
)

set "PYTHONPATH=src"
python -m PyInstaller --clean --windowed --onefile --name PES6Editor2027 --paths src --distpath dist\PES6Editor2027 --workpath build\work --specpath build\spec src\pes6_editor\app.py
if errorlevel 1 (
    echo ERROR: PyInstaller build failed.
    exit /b 1
)

if exist "%OUTPUT_EXE%" (
    echo Build complete: %OUTPUT_EXE%
    echo NOTE: Windows 7 compatibility is not verified until tested on Windows 7 32-bit.
    exit /b 0
)

echo ERROR: Expected output was not created: %OUTPUT_EXE%
exit /b 1
