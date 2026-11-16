"""Safe, read-only AFS archive inspection for PES 6 style archives."""

import os
import struct
import stat

AFS_HEADER_SIZE = 12
AFS_MAGIC = b"AFS\x00"


class AFSInspectionError(ValueError):
    """Raised for malformed, truncated, or inconsistent archive content."""


def detect_afs(path):
    """Return True when the file looks like an AFS archive by signature."""
    try:
        with open(path, "rb") as archive:
            header = archive.read(AFS_HEADER_SIZE)
    except OSError:
        return False
    return len(header) == AFS_HEADER_SIZE and header[:4] == AFS_MAGIC


def _read_exact(path, offset, length):
    """Safely read a bounded slice without loading the whole archive into memory."""
    with open(path, "rb") as archive:
        archive.seek(offset)
        data = archive.read(length)
    return data


def _parse_optional_entries(path, file_size):
    """Read only the AFS header and the minimal table metadata needed for inspection."""
    if file_size < AFS_HEADER_SIZE:
        raise AFSInspectionError("File is too small to contain an AFS header.")

    header = _read_exact(path, 0, AFS_HEADER_SIZE)
    if len(header) != AFS_HEADER_SIZE:
        raise AFSInspectionError("Failed to read the full AFS header.")
    if header[:4] != AFS_MAGIC:
        raise AFSInspectionError("AFS header signature is invalid.")

    version = struct.unpack_from("<I", header, 4)[0]
    entry_count = struct.unpack_from("<I", header, 8)[0]

    if entry_count == 0:
        return {
            "version": version,
            "entry_count": 0,
            "entries": [],
            "header_valid": True,
            "notes": ["Archive contains zero entries."],
        }

    # The exact AFS table format is not assumed here. We read a minimal entry list
    # only when the archive is large enough for a standard 16-byte record layout.
    # This inspection tool is deliberately conservative: malformed archives are
    # rejected before any extraction or modification is attempted.
    entry_size = 16
    table_size = entry_count * entry_size
    table_start = AFS_HEADER_SIZE
    table_end = table_start + table_size

    if table_end > file_size:
        raise AFSInspectionError(
            "Archive entry table exceeds file boundaries: expected {} bytes, found {} bytes.".format(
                table_end, file_size
            )
        )

    raw_entries = _read_exact(path, table_start, table_size)
    if len(raw_entries) != table_size:
        raise AFSInspectionError("Could not read the full AFS entry table.")

    entries = []
    for index in range(entry_count):
        offset = table_start + index * entry_size
        chunk = raw_entries[index * entry_size:(index + 1) * entry_size]
        if len(chunk) != entry_size:
            raise AFSInspectionError("Incomplete entry record encountered at index {}.".format(index))

        data = struct.unpack("<IIII", chunk)
        entry_offset = data[0]
        entry_size_bytes = data[1]
        real_size = data[2]
        flags = data[3]

        entries.append(
            {
                "index": index,
                "offset": entry_offset,
                "size": entry_size_bytes,
                "real_size": real_size,
                "flags": flags,
                "status": "unknown",
                "reason": None,
            }
        )

    for entry in entries:
        entry_end = entry["offset"] + entry["size"]
        if entry["offset"] < AFS_HEADER_SIZE or entry["offset"] > file_size:
            entry["status"] = "invalid"
            entry["reason"] = "offset outside archive boundary"
        elif entry_end > file_size:
            entry["status"] = "invalid"
            entry["reason"] = "entry exceeds file size"
        elif entry["size"] == 0:
            entry["status"] = "empty"
            entry["reason"] = "zero-length entry"
        else:
            entry["status"] = "ok"
            entry["reason"] = None

    return {
        "version": version,
        "entry_count": entry_count,
        "entries": entries,
        "header_valid": True,
        "notes": [
            "AFS header and table were inspected without extracting archive contents.",
            "This tool reads only metadata and validates boundary conditions.",
        ],
    }


def inspect_afs(path):
    """Return AFS metadata without revealing or writing file contents."""
    if not os.path.exists(path):
        raise AFSInspectionError("AFS archive does not exist.")

    file_stat = os.stat(path, follow_symlinks=False)
    if not stat.S_ISREG(file_stat.st_mode):
        raise AFSInspectionError("The selected path is not a regular file.")

    file_size = file_stat.st_size
    if file_size < AFS_HEADER_SIZE:
        raise AFSInspectionError("File is too small to be a valid AFS archive.")

    header = _read_exact(path, 0, AFS_HEADER_SIZE)
    if len(header) != AFS_HEADER_SIZE:
        raise AFSInspectionError("Could not read the full AFS header.")
    if header[:4] != AFS_MAGIC:
        raise AFSInspectionError("AFS magic signature is invalid.")

    return _parse_optional_entries(path, file_size)
