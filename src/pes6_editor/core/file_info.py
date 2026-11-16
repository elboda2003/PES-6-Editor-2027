"""Read-only helpers for inspecting file metadata."""

import os
import stat
from datetime import datetime


def get_extension(filename):
    """Return a filename's extension, or '(none)' when it has none."""
    extension = os.path.splitext(filename)[1]
    return extension if extension else "(none)"


def format_size(size_in_bytes):
    """Format a non-negative file size in bytes and a readable unit."""
    size = float(size_in_bytes)
    units = ("bytes", "KB", "MB", "GB", "TB")
    unit_index = 0

    while size >= 1024.0 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1

    if unit_index == 0:
        return "{} bytes".format(int(size_in_bytes))
    return "{:.1f} {} ({} bytes)".format(size, units[unit_index], size_in_bytes)


def get_file_details(path):
    """Return basic metadata for a regular file without reading its contents.

    This function only asks the operating system for file metadata. It does not
    open the file for reading or writing.
    """
    full_path = os.path.abspath(path)
    file_stat = os.stat(full_path, follow_symlinks=False)
    if not stat.S_ISREG(file_stat.st_mode):
        raise ValueError("The selected path is not a regular file.")

    filename = os.path.basename(full_path)
    modified = datetime.fromtimestamp(file_stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    return {
        "name": filename,
        "extension": get_extension(filename),
        "size": format_size(file_stat.st_size),
        "path": full_path,
        "modified": modified,
    }
