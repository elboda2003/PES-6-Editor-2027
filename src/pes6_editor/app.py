"""Read-only application entry point for PES 6 Editor 2027."""

import tkinter as tk

from pes6_editor.gui.folder_browser import FolderBrowser


def main():
    root = tk.Tk()
    root.title("PES 6 Editor 2027")
    root.geometry("1200x700")
    root.minsize(900, 500)

    FolderBrowser(root).pack(fill=tk.BOTH, expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
