"""Read-only AFS inspector window launcher."""

import os
import tkinter as tk
from tkinter import messagebox

from pes6_editor.core.afs_inspector import detect_afs
from pes6_editor.gui.afs_inspector_panel import AFSInspectorPanel


def open_afs_inspector(file_path, parent):
    """Open a separate inspector window for a valid-signature AFS file.

    This action reads archive metadata only. It never extracts, executes, or
    modifies the selected archive.
    """
    if not os.path.isfile(file_path):
        messagebox.showerror(
            "Cannot inspect AFS file",
            "The selected path is not a regular file.",
            parent=parent,
        )
        return None
    if not detect_afs(file_path):
        messagebox.showerror(
            "Cannot inspect AFS file",
            "The file does not have a recognized AFS signature.",
            parent=parent,
        )
        return None

    window = tk.Toplevel(parent)
    window.title("AFS Inspector — {}".format(os.path.basename(file_path)))
    window.geometry("850x450")
    window.minsize(600, 300)

    panel = AFSInspectorPanel(window)
    panel.pack(fill=tk.BOTH, expand=True)
    panel.inspect_path(file_path)
    return window
