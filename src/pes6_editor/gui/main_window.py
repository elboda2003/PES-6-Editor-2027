"""Main application window with a sidebar and implemented tool pages."""

import tkinter as tk
from tkinter import ttk

from pes6_editor.core.sections import SECTIONS
from pes6_editor.gui.afs_inspector_page import AFSInspectorPage
from pes6_editor.gui.dashboard import Dashboard
from pes6_editor.gui.folder_browser import FolderBrowser


class MainWindow(ttk.Frame):
    """Expandable application shell with explicit section availability."""

    def __init__(self, root):
        ttk.Frame.__init__(self, root)
        self.root = root
        self._active_page = None
        self._build()

    def _build(self):
        self.root.title("PES 6 Editor 2027 — Read-only tools")
        self.root.geometry("1200x720")
        self.root.minsize(900, 560)
        self.pack(fill=tk.BOTH, expand=True)

        header = ttk.Frame(self, padding=(16, 12))
        header.pack(fill=tk.X)

        ttk.Label(
            header,
            text="PES 6 Editor 2027",
            font=("TkDefaultFont", 16, "bold"),
        ).pack(side=tk.LEFT)

        ttk.Label(
            header,
            text="Python 3.8.10 / 32-bit target • Read-only milestone",
        ).pack(side=tk.RIGHT)

        body = ttk.Frame(self)
        body.pack(fill=tk.BOTH, expand=True)

        sidebar = ttk.Frame(body, padding=(10, 8))
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.page_host = ttk.Frame(body, padding=8)
        self.page_host.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(
            sidebar,
            text="SECTIONS",
            font=("TkDefaultFont", 9, "bold"),
        ).pack(anchor=tk.W, pady=(0, 8))

        self.buttons = {}
        for section in SECTIONS:
            button = ttk.Button(
                sidebar,
                text=section["title"],
                command=lambda section_id=section["id"]: self.show_section(
                    section_id
                ),
                width=22,
            )

            if not section["enabled"]:
                button.configure(
                    state=tk.DISABLED,
                    text="{} — unavailable".format(section["title"]),
                )

            button.pack(fill=tk.X, pady=2)
            self.buttons[section["id"]] = button

        self.status = ttk.Label(
            self,
            text="Ready — game files are not modified or executed.",
            anchor=tk.W,
            relief=tk.SUNKEN,
            padding=(8, 4),
        )
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

        self.show_section("dashboard")

    def show_section(self, section_id):
        """Display an implemented section; ignore unavailable sections."""
        section = next(
            (item for item in SECTIONS if item["id"] == section_id),
            None,
        )
        if section is None or not section["enabled"]:
            return

        if self._active_page is not None:
            self._active_page.destroy()
            self._active_page = None

        if section_id == "dashboard":
            page = Dashboard(self.page_host, self.show_section)
        elif section_id == "file_browser":
            page = FolderBrowser(self.page_host)
        elif section_id == "afs_inspector":
            page = AFSInspectorPage(self.page_host, self.root)
        elif section_id == "settings":
            page = self._settings_page()
        else:
            return

        page.pack(fill=tk.BOTH, expand=True)
        self._active_page = page
        self.status.configure(text=section["status"])

    def _settings_page(self):
        page = ttk.Frame(self.page_host, padding=20)

        ttk.Label(
            page,
            text="Settings and compatibility",
            font=("TkDefaultFont", 18, "bold"),
        ).pack(anchor=tk.W, pady=(0, 12))

        details = (
            "Target interpreter: Python 3.8.10, 32-bit.",
            "Target operating system: Windows 7, 32-bit; test there before "
            "claiming compatibility.",
            "Available tools: folder listing, file metadata, bounded preview, "
            "AFS signature check.",
            "Safety: no game files are edited, moved, renamed, deleted, "
            "or executed.",
            "Unsupported editors stay disabled until their formats are verified.",
        )

        for detail in details:
            ttk.Label(
                page,
                text=detail,
                wraplength=760,
            ).pack(anchor=tk.W, pady=4)

        return page


def run():
    """Create the Tk root and start the application event loop."""
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()
