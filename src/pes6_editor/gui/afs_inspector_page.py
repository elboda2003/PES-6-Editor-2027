"""Main-window page for launching the separate read-only AFS inspector."""

import tkinter as tk
from tkinter import filedialog, ttk

from pes6_editor.gui.afs_inspector import open_afs_inspector


class AFSInspectorPage(ttk.Frame):
    """Offer a real archive chooser and launch the existing AFS inspector."""

    def __init__(self, master, parent_window):
        ttk.Frame.__init__(self, master, padding=20)
        self.parent_window = parent_window
        self._build()

    def _build(self):
        ttk.Label(
            self,
            text="AFS Inspector",
            font=("TkDefaultFont", 18, "bold"),
        ).pack(anchor=tk.W)

        ttk.Label(
            self,
            text=(
                "Select an archive for a read-only signature check. Entry-layout "
                "parsing is unavailable until a supported layout is verified. "
                "Nothing is extracted, executed, or modified."
            ),
            wraplength=760,
            justify=tk.LEFT,
        ).pack(anchor=tk.W, pady=(8, 16))

        ttk.Button(
            self,
            text="Open AFS file...",
            command=self.open_file,
        ).pack(anchor=tk.W)

    def open_file(self):
        """Choose a file and pass it to the existing signature-checking window."""
        path = filedialog.askopenfilename(
            parent=self,
            title="Select AFS archive for read-only inspection",
            filetypes=(("AFS archives", "*.afs"), ("All files", "*.*")),
        )
        if path:
            open_afs_inspector(path, self.parent_window)
