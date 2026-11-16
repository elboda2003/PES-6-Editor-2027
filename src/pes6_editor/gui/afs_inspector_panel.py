"""Read-only AFS archive information panel."""

import tkinter as tk
from tkinter import ttk

from pes6_editor.core.afs_inspector import inspect_afs


class AFSInspectorPanel(ttk.Frame):
    """Show archive metadata and entry-level safety validation."""

    def __init__(self, master):
        ttk.Frame.__init__(self, master, padding=10)
        self._build_widgets()

    def _build_widgets(self):
        ttk.Label(
            self,
            text="AFS archive inspection (read-only): file contents are not extracted, modified, or overwritten.",
            wraplength=500,
            justify=tk.LEFT,
        ).pack(anchor=tk.W, pady=(0, 8))

        columns = ("index", "offset", "size", "real_size", "status", "reason")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("index", text="Index")
        self.tree.heading("offset", text="Offset")
        self.tree.heading("size", text="Size")
        self.tree.heading("real_size", text="Real size")
        self.tree.heading("status", text="Status")
        self.tree.heading("reason", text="Reason")

        self.tree.column("index", width=60, anchor=tk.CENTER)
        self.tree.column("offset", width=100, anchor=tk.CENTER)
        self.tree.column("size", width=100, anchor=tk.CENTER)
        self.tree.column("real_size", width=100, anchor=tk.CENTER)
        self.tree.column("status", width=120, anchor=tk.W)
        self.tree.column("reason", width=220, anchor=tk.W)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.info_label = ttk.Label(self, text="No AFS archive selected.", anchor=tk.W)
        self.info_label.pack(fill=tk.X, pady=(8, 0))

    def clear(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.info_label.configure(text="No AFS archive selected.")

    def inspect_path(self, path):
        """Read-only archive summary and entry listing for a selected AFS file."""
        try:
            result = inspect_afs(path)
        except (OSError, ValueError) as error:
            self.clear()
            self.info_label.configure(text="AFS inspection failed: {}".format(error))
            return

        self.info_label.configure(
            text="Archive valid: {} | Entries: {} | Version: {}".format(
                result["header_valid"], result["entry_count"], result["version"]
            )
        )

        for item in self.tree.get_children():
            self.tree.delete(item)

        for entry in result["entries"]:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    entry["index"],
                    entry["offset"],
                    entry["size"],
                    entry["real_size"],
                    entry["status"],
                    entry["reason"] if entry["reason"] else "ok",
                ),
            )
