# PES 6 Editor 2027 AI

A beginner-friendly project targeting Windows 7 (32-bit) and Python 3.8.10 (32-bit).

## Current milestone: read-only AFS archive inspection

This milestone adds a safe AFS archive inspector. The application can detect AFS files, validate the archive header, count entries, and inspect metadata such as entry index, offset, size, and status without extracting archive contents.

The inspector performs boundary validation and flags malformed or corrupted archives without modifying them. It does not extract files, overwrite data, or rewrite archive structure. The implementation deliberately avoids reading the full archive into memory and only reads the header, entry table, and validated metadata needed for inspection.

## AFS archive features

- Detects AFS archive files by magic signature
- Reads and validates the AFS header
- Checks entry table size and bounds
- Reports entry index, offset, size, and validity status
- Handles malformed or truncated archives safely
- Keeps all operations read-only
- Shows archive metadata in the GUI when an `.afs` file is selected

## Run the application

1. Install Python 3.8.10 **32-bit (x86)** on Windows and include Tcl/Tk during installation.
2. Open Command Prompt in the repository folder.
3. Run:

   ```bat
   set PYTHONPATH=src
   python -m pes6_editor.app
   ```
4. Select a folder containing `.afs` files.
5. Click an AFS archive in the tree to inspect it.
6. Use the AFS inspector panel to review archive metadata and entry validation.

## Run tests

From the repository folder:

```bat
set PYTHONPATH=src
python -m unittest discover -s tests -v
```

This includes the AFS synthetic-file tests and the earlier metadata tests.

## Windows 7 32-bit packaging

PyInstaller remains optional and build-time only. Build with Python 3.8.10 32-bit and PyInstaller 4.10:

```bat
python -m pip install PyInstaller==4.10
set PYTHONPATH=src
python -m PyInstaller --clean --windowed --name PES6Editor2027 --paths src src\pes6_editor\app.py
```

Test the packaged app on a clean Windows 7 32-bit machine or virtual machine before distributing it. A successful build on newer Windows versions does not guarantee Windows 7 compatibility.

## Safety rules

- Never execute `.afs` or `.exe` files.
- Never extract archive contents.
- Never modify, rename, move, or overwrite files.
- Only read metadata and verified header/table bounds.
