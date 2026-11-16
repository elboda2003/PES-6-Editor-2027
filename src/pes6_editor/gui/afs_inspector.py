"""Read-only integration point for AFS archive inspection."""

import os

from pes6_editor.core.afs_inspector import detect_afs
from pes6_editor.gui.afs_inspector_panel import AFSInspectorPanel


def maybe_show_afs_inspector(file_path, parent):
    """Show AFS inspection metadata when a file is recognized as AFS.

    This function only inspects and does not extract or modify the archive.
    """
    if not os.path.isfile(file_path):
        return
    if not detect_afs(file_path):
        return

    panel = AFSInspectorPanel(parent)
    panel.pack(fill="both", expand=True)
    panel.inspect_path(file_path)
    return panel
