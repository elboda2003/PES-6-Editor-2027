"""Read-only file and folder browser built with Tkinter."""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from pes6_editor.core.file_info import format_size, get_extension, get_file_details
from pes6_editor.gui.file_preview_panel import FilePreviewPanel


class FolderBrowser(ttk.Frame):
    """Show a selected folder's tree and read-only file metadata/previews."""

    def __init__(self, master):
        ttk.Frame.__init__(self, master, padding=10)
        self._root_path = None
        self._loaded_directories = set()
        self._detail_values = {}
        self._build_widgets()

    def _build_widgets(self):
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, pady=(0, 8))

        self.select_button = ttk.Button(
            toolbar, text="Select PES 6 Data Folder...", command=self.select_folder
        )
        self.select_button.pack(side=tk.LEFT)

        self.refresh_button = ttk.Button(
            toolbar, text="Refresh", command=self.refresh, state=tk.DISABLED
        )
        self.refresh_button.pack(side=tk.LEFT, padx=(8, 0))

        ttk.Label(
            self,
            text="Read-only inspection: files are never changed or executed; previews read at most 256 bytes.",
        ).pack(anchor=tk.W, pady=(0, 8))

        content = ttk.Panedwindow(self, orient=tk.HORIZONTAL)
        content.pack(fill=tk.BOTH, expand=True)

        table_frame = ttk.Frame(content)
        columns = ("extension", "size", "path")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="tree headings",
            selectmode="browse",
        )
        self.tree.heading("#0", text="Name", anchor=tk.W)
        self.tree.heading("extension", text="Extension", anchor=tk.W)
        self.tree.heading("size", text="Size", anchor=tk.W)
        self.tree.heading("path", text="Full path", anchor=tk.W)

        self.tree.column("#0", width=180, minwidth=120, stretch=True)
        self.tree.column("extension", width=85, minwidth=70, stretch=False)
        self.tree.column("size", width=135, minwidth=110, stretch=False)
        self.tree.column("path", width=300, minwidth=160, stretch=True)

        vertical_scroll = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        horizontal_scroll = ttk.Scrollbar(
            table_frame, orient=tk.HORIZONTAL, command=self.tree.xview
        )
        self.tree.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set,
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        vertical_scroll.grid(row=0, column=1, sticky="ns")
        horizontal_scroll.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)
        content.add(table_frame, weight=3)

        side_panel = ttk.Notebook(content)
        details_frame = ttk.Frame(side_panel, padding=10)
        self._build_details_panel(details_frame)
        side_panel.add(details_frame, text="File Details")
        self.preview_panel = FilePreviewPanel(side_panel)
        side_panel.add(self.preview_panel, text="Preview & Binary")
        content.add(side_panel, weight=2)

        self.tree.bind("<<TreeviewOpen>>", self._on_tree_open)
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        self.status = ttk.Label(self, text="Choose a game-data folder to begin.", anchor=tk.W)
        self.status.pack(fill=tk.X, pady=(8, 0))

    def _build_details_panel(self, parent):
        """Create read-only labels for the selected file's metadata."""
        fields = (
            ("name", "File name"),
            ("extension", "Extension"),
            ("size", "Size"),
            ("path", "Full path"),
            ("modified", "Last modified"),
        )
        for row, (key, title) in enumerate(fields):
            ttk.Label(parent, text=title + ":", font=("TkDefaultFont", 9, "bold")).grid(
                row=row * 2, column=0, sticky=tk.W, pady=(5, 0)
            )
            value = tk.StringVar(value="Select a file in the tree.")
            self._detail_values[key] = value
            value_label = ttk.Label(
                parent,
                textvariable=value,
                wraplength=260 if key == "path" else 300,
                justify=tk.LEFT,
            )
            value_label.grid(row=row * 2 + 1, column=0, sticky=tk.W)
        parent.columnconfigure(0, weight=1)

    def _clear_details(self, message="Select a file in the tree."):
        for value in self._detail_values.values():
            value.set(message)

    def _show_file_details(self, path):
        try:
            details = get_file_details(path)
        except (OSError, ValueError) as error:
            self._clear_details("File details unavailable: {}".format(error))
            self.preview_panel.clear("Preview unavailable for this selection.")
            self.status.configure(text="Cannot inspect file: {}".format(path))
            return

        for key, value in details.items():
            self._detail_values[key].set(value)
        self.preview_panel.show_file(path)
        self.status.configure(text="Selected file (read-only): {}".format(details["path"]))

    def select_folder(self):
        """Ask the user to select a folder; do not write to it."""
        selected = filedialog.askdirectory(
            title="Select PES 6 game-data folder",
            mustexist=True,
        )
        if selected:
            self._set_root_folder(selected)

    def _set_root_folder(self, folder_path):
        self._root_path = os.path.abspath(folder_path)
        self._loaded_directories.clear()
        for item_id in self.tree.get_children(""):
            self.tree.delete(item_id)

        name = os.path.basename(os.path.normpath(self._root_path)) or self._root_path
        root_id = self.tree.insert(
            "",
            tk.END,
            text=name,
            values=("Folder", "—", self._root_path),
            tags=("directory",),
            open=True,
        )
        self.tree.insert(root_id, tk.END, text="Expand to list contents", tags=("placeholder",))
        self.refresh_button.configure(state=tk.NORMAL)
        self._clear_details("Select a file in the tree.")
        self.preview_panel.clear("Select a file to inspect.")
        self.status.configure(text="Selected folder: {}".format(self._root_path))
        self.tree.focus(root_id)
        self.tree.selection_set(root_id)
        self.tree.event_generate("<<TreeviewOpen>>")

    def refresh(self):
        """Reload the selected folder's listing (read-only)."""
        if self._root_path and os.path.isdir(self._root_path):
            self._set_root_folder(self._root_path)
        elif self._root_path:
            messagebox.showerror(
                "Folder unavailable",
                "The selected folder is no longer available:\n{}".format(self._root_path),
                parent=self,
            )

    def _on_tree_open(self, _event):
        item_id = self.tree.focus()
        if not item_id or item_id in self._loaded_directories:
            return
        if "directory" not in self.tree.item(item_id, "tags"):
            return

        path = self.tree.set(item_id, "path")
        self._loaded_directories.add(item_id)
        for child_id in self.tree.get_children(item_id):
            self.tree.delete(child_id)

        try:
            entries = list(os.scandir(path))
            entries.sort(
                key=lambda entry: (
                    not entry.is_dir(follow_symlinks=False), entry.name.lower()
                )
            )
        except OSError as error:
            self.tree.insert(
                item_id,
                tk.END,
                text="Cannot read folder: {}".format(error),
                values=("", "", path),
                tags=("error",),
            )
            return

        for entry in entries:
            self._insert_entry(item_id, entry)

        if not entries:
            self.tree.insert(item_id, tk.END, text="(empty folder)", values=("", "", path))

    def _insert_entry(self, parent_id, entry):
        """Add one filesystem entry without opening or changing its contents."""
        path = entry.path
        try:
            is_directory = entry.is_dir(follow_symlinks=False)
        except OSError:
            is_directory = False

        if is_directory:
            item_id = self.tree.insert(
                parent_id,
                tk.END,
                text=entry.name,
                values=("Folder", "—", path),
                tags=("directory",),
            )
            self.tree.insert(item_id, tk.END, text="Expand to list contents", tags=("placeholder",))
            return

        try:
            file_stat = entry.stat(follow_symlinks=False)
            size_text = format_size(file_stat.st_size)
        except OSError:
            size_text = "Unavailable"

        self.tree.insert(
            parent_id,
            tk.END,
            text=entry.name,
            values=(get_extension(entry.name), size_text, path),
            tags=("file",),
        )

    def _on_tree_select(self, _event):
        selected = self.tree.selection()
        if not selected:
            return

        item_id = selected[0]
        tags = self.tree.item(item_id, "tags")
        path = self.tree.set(item_id, "path")
        if "file" in tags and path:
            self._show_file_details(path)
        elif "directory" in tags:
            self._clear_details("Select a file in the tree.")
            self.preview_panel.clear("Select a file to inspect.")
            self.status.configure(text="Selected folder: {}".format(path))
