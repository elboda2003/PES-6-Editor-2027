# PES 6 Editor 2027 AI

A beginner-friendly project targeting Windows 7 (32-bit) and Python 3.8.10 (32-bit).

## Phase 1 application status

The proposed phase-one application shell provides a Dashboard and navigation
for the tools that are actually available:

- **File Browser**, including File Details and Preview & Binary.
- **AFS Inspector**, limited to recognizing the `AFS\0` signature and reporting
  file size until an entry layout is verified.
- **Settings**, with compatibility and safety information.

Players, Teams, Transfers, Competitions, Stadiums, and Graphics are not
implemented for editing. They must be shown as unavailable, not as functional
editors.

The proposed `pes6_editor.core.file_safety` utilities create separate backup,
working, or restored copies. They do not overwrite existing destinations or
modify the source. They do not enable game-file editing.

## Current milestone: read-only archive and file inspection

The desktop application provides a safe, read-only inspection workflow:

- Browse a PES 6 data folder in a tree view.
- Show file details such as name, extension, size, full path, and last modified date.
- Preview the first 256 bytes in hexadecimal.
- Show a text preview only for files conservatively recognized as text.
- Open an AFS archive in a separate inspector window to review its header and entry metadata.
- Never execute, extract, rename, move, delete, or edit game files.

To inspect an AFS file, click **Open AFS...** and choose the archive. The inspector checks the AFS signature and reports the file size. Entry information is not parsed because the supported entry layout is unverified. This action only reads the archive; it does not extract or modify contents.

## Run the source version

1. Install Python 3.8.10 **32-bit (x86)** on Windows and include Tcl/Tk during installation.
2. Open Command Prompt in the repository folder.
3. Run:

   ```bat
   set PYTHONPATH=src
   python -m pes6_editor.app
   ```

4. Select a folder to browse it, or use **Open AFS...** to inspect an archive directly.
5. Select files in the tree to view File Details and Preview & Binary.

## Build the Windows executable

Run `build_windows.bat` from the repository root. It requires exactly Python 3.8.10, 32-bit, and installs/uses PyInstaller 4.10:

```bat
build_windows.bat
```

The script stops with an error if the active Python version or architecture does not match. It also refuses to overwrite an existing executable at the target path.

Expected output (one-file build):

```text
dist\PES6Editor2027\PES6Editor2027.exe
```

The build script uses this same output directory and checks this exact executable path before and after the build.

## Important compatibility notice

A successful build does not guarantee Windows 7 compatibility. The application must be tested on Windows 7 32-bit before claiming it works there. A modern Windows build does not substitute for testing on the target system.

## Run tests

From the repository folder:

```bat
set PYTHONPATH=src
python -m unittest discover -s tests -v
```

The tests exercise the AFS parser and GUI-launch wiring with mocks; they do not require a live interactive GUI.

## Safety rules

- Never execute `.afs` or `.exe` game files.
- Never extract archive contents in this read-only milestone.
- Never modify, rename, move, or delete PES 6 game files.
- Do not claim Windows 7 compatibility until the packaged application has been tested there.
