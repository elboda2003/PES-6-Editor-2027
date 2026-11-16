"""Conservative, read-only AFS signature inspection.

No entry-table layout is parsed until a PES 6-compatible layout is verified.
"""

import os
import stat

AFS_MAGIC = b"AFS\x00"


class AFSInspectionError(ValueError):
    """Raised when a file cannot be safely identified as an AFS archive."""


def detect_afs(path):
    """Return True only when the file begins with the AFS magic signature."""
    try:
        with open(path, "rb") as archive:
            return archive.read(len(AFS_MAGIC)) == AFS_MAGIC
    except OSError:
        return False


def inspect_afs(path):
    """Inspect signature and size; deliberately do not guess entry layout."""
    full_path = os.path.abspath(path)
    file_stat = os.stat(full_path, follow_symlinks=False)
    if not stat.S_ISREG(file_stat.st_mode):
        raise AFSInspectionError("The selected path is not a regular file.")

    with open(full_path, "rb") as archive:
        signature = archive.read(len(AFS_MAGIC))

    if signature != AFS_MAGIC:
        raise AFSInspectionError("AFS signature is missing or file is truncated.")

    return {
        "path": full_path,
        "file_size": file_stat.st_size,
        "header_valid": True,
        "format_supported": False,
        "entry_count": None,
        "entries": [],
        "notes": [
            "AFS magic signature recognized.",
            "Entry layout is unverified; entries were not parsed.",
            "No archive contents were extracted or modified.",
        ],
    }
