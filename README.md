# PES 6 Editor 2027 AI

A beginner-friendly project targeting Windows 7 (32-bit) and Python 3.8.10 (32-bit).

## Current milestone: read-only folder and file inspector

Select a PES 6 game-data folder and browse its folders and files in a tree. The **File Details** panel shows the selected file's name, extension, size, full path, and last modified date and time. The separate **Preview & Binary** panel shows the file format classification, total size, and a hexadecimal view of the first 256 bytes.

A text preview is displayed only when the sample passes a conservative text check. Known binary-oriented extensions (`.afs`, `.bin`, `.dat`, `.img`, `.exe`) are classified by extension and are not given a text preview. These extension labels are informative only; the app does not parse the actual PES 6 container formats. Executable files are never run.

This milestone is strictly read-only. The preview code opens files in binary read-only mode and reads at most 256 bytes; it does not load large files into memory, modify, rename, move, or delete files, or extract archive contents. No editing, filtering, or extraction features are included.

## Run the application

1. Install Python 3.8.10 **32-bit (x86)** on Windows and include Tcl/Tk during installation.
2. Open Command Prompt in the repository folder.
3. Set the source folder and launch the app:

   ```bat
   set PYTHONPATH=src
   python -m pes6_editor.app
   ```

4. Click **Select PES 6 Data Folder...** and choose the game-data folder.
5. Expand folders in the tree. Click a file to see its details and preview. Select **Preview & Binary** to view the hex/text sections.

The GUI uses Python's built-in Tkinter, so no third-party runtime dependency is needed.

## Run tests

From the repository folder:

```bat
set PYTHONPATH=src
python -m unittest discover -s tests -v
```

Tests cover metadata, extension classification, bounded sample reads, hexadecimal rendering, and conservative text detection. For a manual GUI check, select a text file and a binary PES-related file, confirm the preview changes appropriately, then verify the source files remain unchanged.

## Windows 7 32-bit packaging

PyInstaller is an optional build-time dependency. With the 32-bit Python 3.8.10 interpreter, install the pinned candidate and build an onedir application:

```bat
python -m pip install PyInstaller==4.10
set PYTHONPATH=src
python -m PyInstaller --clean --windowed --name PES6Editor2027 --paths src src\pes6_editor\app.py
```

The output is under `dist\PES6Editor2027\`. A successful build on a newer Windows version does not guarantee Windows 7 compatibility. Test the packaged app on a clean Windows 7 32-bit machine or virtual machine, and verify all bundled components and runtime requirements there.

## Project goals

Future milestones may add verified PES 6 data inspection and editing tools, player and team management, asset support, compatible archive support, an assistant, and safe backups before any future modifications. Those features are not part of this read-only milestone.
