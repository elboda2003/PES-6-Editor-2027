"""Dashboard showing current tool status and working navigation."""

import tkinter as tk
from tkinter import ttk

from pes6_editor.core.sections import SECTIONS


class Dashboard(ttk.Frame):
    """Display actual tool availability; do not imply unimplemented features work."""

    def __init__(self, master, navigate):
        ttk.Frame.__init__(self, master, padding=18)
        self._navigate = navigate
        self._build()

    def _build(self):
        ttk.Label(
            self,
            text="PES 6 Editor 2027",
            font=("TkDefaultFont", 20, "bold"),
        ).pack(anchor=tk.W)

        ttk.Label(
            self,
            text=(
                "Development build. Available file tools are read-only; "
                "unimplemented editors are unavailable."
            ),
            wraplength=800,
        ).pack(anchor=tk.W, pady=(4, 16))

        table = ttk.Treeview(
            self,
            columns=("status",),
            show="tree headings",
            height=len(SECTIONS),
        )
        table.heading("#0", text="Section")
        table.heading("status", text="Current status")
        table.column("#0", width=190, minwidth=150)
        table.column("status", width=540, minwidth=300)
        table.pack(fill=tk.BOTH, expand=True)

        for section in SECTIONS:
            table.insert(
                "",
                tk.END,
                iid=section["id"],
                text=section["title"],
                values=(section["status"],),
            )

        actions = ttk.Frame(self)
        actions.pack(fill=tk.X, pady=(14, 0))

        ttk.Button(
            actions,
            text="Open File Browser",
            command=lambda: self._navigate("file_browser"),
        ).pack(side=tk.LEFT)

        ttk.Button(
            actions,
            text="Open AFS Inspector",
            command=lambda: self._navigate("afs_inspector"),
        ).pack(side=tk.LEFT, padx=(8, 0))
