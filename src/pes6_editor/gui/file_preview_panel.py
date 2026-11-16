"""Read-only preview panel for a small file sample."""

import tkinter as tk
from tkinter import ttk

from pes6_editor.core.file_preview import inspect_file


class FilePreviewPanel(ttk.Frame):
    """Display file classification and bounded hex/text previews."""

    def __init__(self, master):
        ttk.Frame.__init__(self, master, padding=8)
        self._format = tk.StringVar(value="Select a file to inspect.")
        self._size = tk.StringVar(value="—")
        self._build_widgets()

    def _build_widgets(self):
        ttk.Label(self, text="Format:", font=("TkDefaultFont", 9, "bold")).pack(anchor=tk.W)
        ttk.Label(self, textvariable=self._format, wraplength=320).pack(anchor=tk.W, pady=(0, 6))
        ttk.Label(self, text="File size:", font=("TkDefaultFont", 9, "bold")).pack(anchor=tk.W)
        ttk.Label(self, textvariable=self._size).pack(anchor=tk.W, pady=(0, 8))

        hex_frame = ttk.LabelFrame(self, text="First 256 bytes — hexadecimal", padding=5)
        hex_frame.pack(fill=tk.BOTH, expand=True)
        self.hex_text = self._make_read_only_text(hex_frame, height=10)
        self.hex_text.insert("1.0", "Select a file in the tree.")

        text_frame = ttk.LabelFrame(self, text="Text preview (only when recognized as text)", padding=5)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(8, 0))
        self.text_text = self._make_read_only_text(text_frame, height=6, wrap=tk.WORD)
        self.text_text.insert("1.0", "No text preview available.")

    @staticmethod
    def _make_read_only_text(parent, height, wrap=tk.NONE):
        text = tk.Text(parent, height=height, wrap=wrap, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        return text

    @staticmethod
    def _set_text(widget, value):
        widget.configure(state=tk.NORMAL)
        widget.delete("1.0", tk.END)
        widget.insert("1.0", value)
        widget.configure(state=tk.DISABLED)

    def clear(self, message="Select a file to inspect."):
        self._format.set(message)
        self._size.set("—")
        self._set_text(self.hex_text, message)
        self._set_text(self.text_text, "No text preview available.")

    def show_file(self, path):
        """Inspect and show bounded sample data; never execute or write the file."""
        try:
            result = inspect_file(path)
        except (OSError, ValueError) as error:
            self.clear("Preview unavailable: {}".format(error))
            return

        self._format.set(result["format"])
        self._size.set(result["size"])
        self._set_text(self.hex_text, result["hex"])
        if result["text"] is None:
            self._set_text(self.text_text, "No text preview: file is not safely recognized as text.")
        else:
            self._set_text(self.text_text, result["text"])
