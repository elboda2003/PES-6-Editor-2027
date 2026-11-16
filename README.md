# PES 6 Editor 2027 AI

A beginner-friendly project targeting Windows 7 (32-bit) and Python 3.8.10 (32-bit).

## Current milestone: read-only folder inspector

The desktop application lets you select a PES 6 game-data folder, browse its folders and files in a tree, and view metadata for a selected file. The **File Details** panel shows the file name, extension, size, full path, and last modified date and time.

This milestone is strictly read-only. It lists directory entries and obtains filesystem metadata; it does not open file contents or modify, rename, move, or delete game files. It does not yet edit PES 6 data.

## Run the application

1. Install Python 3.8.10 **32-bit (x86)** on Windows and include Tcl/Tk during installation.
2. Open Command Prompt in the repository folder.
3. Set the source folder and launch the app:

   ```bat
   set PYTHONPATH=src
   python -m pes6_editor.app
   ```

4. Click **Select PES 6 Data Folder...** and choose the game-data folder.
5. Expand folders in the tree. Click a file to see its details in the panel.

The GUI uses Python's built-in Tkinter, so no third-party runtime dependency is needed.

## Run tests

From the repository folder:

```bat
set PYTHONPATH=src
python -m unittest discover -s tests -v
```

The tests cover the read-only metadata helpers. For a manual GUI check, choose a test folder and verify that the displayed metadata is accurate and the files remain unchanged.

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
