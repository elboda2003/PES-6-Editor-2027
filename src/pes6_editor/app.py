"""Read-only starter application for PES 6 Editor 2027."""

import tkinter as tk

from pes6_editor.gui.folder_browser import FolderBrowser


def main():
    root = tk.Tk()
    root.title("PES 6 Editor 2027 — Read-only Folder Inspector")
    root.geometry("1050x650")
    root.minsize(720, 420)

    FolderBrowser(root).pack(fill=tk.BOTH, expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
