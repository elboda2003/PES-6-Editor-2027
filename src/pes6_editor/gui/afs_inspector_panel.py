"""Read-only AFS signature and format-status panel."""

import tkinter as tk
from tkinter import ttk

from pes6_editor.core.afs_inspector import inspect_afs


class AFSInspectorPanel(ttk.Frame):
    """Display confirmed signature status without assuming an entry layout."""

    def __init__(self, master):
        ttk.Frame.__init__(self, master, padding=10)
        self._build()

    def _build(self):
        ttk.Label(
            self,
            text=(
                "AFS inspection is read-only. No contents are extracted, "
                "executed, or modified."
            ),
            wraplength=680,
            justify=tk.LEFT,
        ).pack(anchor=tk.W, pady=(0, 8))

        self.info_label = ttk.Label(
            self,
            text="No AFS archive selected.",
            anchor=tk.W,
            justify=tk.LEFT,
            wraplength=680,
        )
        self.info_label.pack(fill=tk.X, pady=(8, 0))

        columns = ("index", "offset", "size", "status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for column, title in (
            ("index", "Index"),
            ("offset", "Offset"),
            ("size", "Size"),
            ("status", "Status"),
        ):
            self.tree.heading(column, text=title)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

    def clear(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.info_label.configure(text="No AFS archive selected.")

    def inspect_path(self, path):
        """Check the signature and report that the entry layout is unverified."""
        try:
            result = inspect_afs(path)
        except (OSError, ValueError) as error:
            self.clear()
            self.info_label.configure(text="AFS inspection failed: {}".format(error))
            return

        self.clear()
        self.info_label.configure(
            text=(
                "AFS signature: recognized\n"
                "File size: {} bytes\n"
                "Entry layout: not verified — entries were not parsed."
            ).format(result["file_size"])
        )
