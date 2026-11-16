# Current phase status

This section describes the proposed phase-one application. Where older
milestone notes below disagree with it, use this current status.

## Requirements

- Python 3.8.10, 32-bit (x86), with Tcl/Tk.
- Windows 7 32-bit is the compatibility target. Compatibility is not verified
  until the application is run on Windows 7.

## Start the application

From the repository root in Command Prompt:

```bat
set PYTHONPATH=src
python -m pes6_editor.app
```

The compatibility entry point is also intended to start the same application:

```bat
set PYTHONPATH=src
python -m pes6_editor.main
```

The proposed main window includes Dashboard, File Browser, AFS Inspector, and
Settings. File Browser retains File Details and Preview & Binary. Players,
Teams, Transfers, Competitions, Stadiums, and Graphics are unavailable for
editing because those editors are not implemented.

AFS inspection is limited to signature recognition and file size. The entry
layout is unverified; the app must not guess entry counts, offsets, or sizes.

# Getting started: PES 6 Editor 2027 first milestone

This milestone is a **read-only folder inspector**. It lets you choose a PES 6 game-data folder and browse its folders and files. It displays each item's name, extension, size, and full path. The program does not open file contents or write to the selected game folder.

## Requirements

- Windows 7, 32-bit (x86)
- Python 3.8.10, 32-bit, with Tcl/Tk selected during Python installation
- No third-party runtime packages are required. The GUI uses Python's built-in Tkinter library.

## Run the application

1. Install Python 3.8.10 **32-bit** and make sure Tkinter is included.
2. Open Command Prompt and change directory to the project folder.
3. Check that Python is 32-bit:

   ```bat
   python -c "import struct; print(struct.calcsize('P') * 8)"
   ```

   It should print `32`.
4. Check Tkinter is available:

   ```bat
   python -m tkinter
   ```

   A small test window should open. Close it.
5. Start the app from the project folder:

   ```bat
   set PYTHONPATH=src
   python -m pes6_editor.app
   ```
6. Click **Select PES 6 Data Folder...**, choose a folder, and expand rows in the tree to browse it. **Refresh** relists the selected folder.

## Run the tests

From the project folder, run:

```bat
set PYTHONPATH=src
python -m unittest discover -s tests -v
```

The tests cover the pure file-name and size-formatting helpers. The GUI also needs a manual check: choose a test folder containing a few nested folders and files, verify the displayed names/extensions/sizes/paths, and confirm the files are unchanged.

## Read-only safety

This milestone uses directory listing and file metadata only. It does not open file contents and contains no code for creating, changing, renaming, moving, or deleting game files. Try it on a copy or test folder first. Do not use this milestone to edit game data; editing features are not included.

## Optional: build a Windows executable

Build on Windows with the **32-bit Python 3.8.10** interpreter. PyInstaller is only needed for packaging; it is not needed to run the Python source. A Windows 7 32-bit test is required because a successful build on another version of Windows does not prove Windows 7 compatibility.

```bat
python -m pip install PyInstaller==4.10
set PYTHONPATH=src
python -m PyInstaller --clean --windowed --name PES6Editor2027 --paths src src\pes6_editor\app.py
```

The onedir build is written under `dist\PES6Editor2027\`. Test it on a clean Windows 7 32-bit machine or virtual machine. Check that Python and all bundled components are 32-bit and that Windows 7 has any required runtime components. PyInstaller 4.10 is pinned as the proposed legacy-compatible packaging tool; verify it and its requirements in the actual build environment before distribution.
