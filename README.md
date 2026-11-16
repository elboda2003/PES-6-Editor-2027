# PES 6 Editor 2027 AI

A beginner-friendly project targeting Windows 7 (32-bit) and Python 3.8.10 (32-bit).

## Current milestone: read-only archive and file inspection

The desktop application provides a safe, read-only inspection workflow:

- Browse a PES 6 data folder in a tree view.
- Show file details such as name, extension, size, full path, and last modified date.
- Preview the first 256 bytes in hexadecimal.
- Show a text preview only for files that are conservatively recognized as text.
- Inspect `.afs` archives without extracting or modifying their contents.
- Never execute, rename, move, delete, or edit files.

This project is a tool for investigation and analysis, not a file-writer or game mod installer.

## Run the source version

1. Install Python 3.8.10 **32-bit (x86)** on Windows and include Tcl/Tk during installation.
2. Open Command Prompt in the repository folder.
3. Run:

   ```bat
   set PYTHONPATH=src
   python -m pes6_editor.app
   ```

4. Select a folder containing game files or archives.
5. Use the tree, details panel, preview panel, and AFS inspector.

## Build the Windows executable

The repository includes `build_windows.bat`, which is intended to produce a standalone executable named `PES6Editor2027.exe`.

Requirements:

- Windows machine or Windows environment
- Python 3.8.10 32-bit
- PyInstaller 4.10

Run:

```bat
build_windows.bat
```

Expected target output:

```text
dist\PES6Editor2027.exe
```

The build is designed to place the executable in the standard PyInstaller output folder, but the script checks for a previous output before attempting to build. It does not overwrite an existing executable.

## Important compatibility notice

A successful build does not guarantee Windows 7 compatibility. The application must be tested on Windows 7 32-bit before any claim is made that it works there. A modern Windows environment can build the application even though it may still fail on Windows 7 due to dependency, runtime, or API differences.

## Run tests

From the repository folder:

```bat
set PYTHONPATH=src
python -m unittest discover -s tests -v
```

## Safety rules

- Never execute `.afs` or `.exe` files.
- Never modify, rename, move, or delete game data files.
- Keep all current features inspection-only.
- Do not rely on packaged output until it has been tested on a clean Windows 7 32-bit machine.
