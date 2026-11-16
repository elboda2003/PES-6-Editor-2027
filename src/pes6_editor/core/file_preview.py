"""Bounded, read-only file format and preview inspection."""

import os
import stat

from pes6_editor.core.file_info import format_size

PREVIEW_LIMIT = 256

KNOWN_FORMATS = {
    ".afs": "AFS archive (recognized by extension; contents not parsed)",
    ".bin": "Binary data file (recognized by extension; contents not parsed)",
    ".dat": "Data file (recognized by extension; contents not parsed)",
    ".img": "Image/disk data file (recognized by extension; contents not parsed)",
    ".exe": "Windows executable (identified only; never executed)",
}


def detect_format(filename, sample):
    """Describe a file using its extension and, for unknown formats, a text check."""
    extension = os.path.splitext(filename)[1].lower()
    if extension in KNOWN_FORMATS:
        return KNOWN_FORMATS[extension]

    text_info = _decode_text_sample(sample)
    if text_info is not None:
        return "Text file ({} detected)".format(text_info[0])
    return "Unknown or binary file"


def format_hex_preview(data):
    """Return a conventional offset/hex/ASCII view of the supplied sample."""
    if not data:
        return "(empty file)"

    lines = []
    for offset in range(0, len(data), 16):
        chunk = data[offset:offset + 16]
        hex_part = " ".join("{:02X}".format(byte) for byte in chunk)
        hex_part = hex_part.ljust(16 * 3 - 1)
        ascii_part = "".join(chr(byte) if 32 <= byte <= 126 else "." for byte in chunk)
        lines.append("{:08X}  {}  |{}|".format(offset, hex_part, ascii_part))
    return "\n".join(lines)


def _decode_text_sample(data):
    """Decode only a small sample if it passes conservative plain-text checks."""
    if not data:
        return None

    encodings = []
    if data.startswith(b"\xef\xbb\xbf"):
        encodings.append(("UTF-8", "utf-8-sig"))
    elif data.startswith(b"\xff\xfe"):
        encodings.append(("UTF-16 LE", "utf-16"))
    elif data.startswith(b"\xfe\xff"):
        encodings.append(("UTF-16 BE", "utf-16"))
    else:
        encodings.append(("UTF-8", "utf-8"))

    for label, encoding in encodings:
        try:
            text = data.decode(encoding, errors="strict")
        except UnicodeDecodeError:
            continue
        if not text:
            continue
        allowed = sum(
            1 for character in text
            if character.isprintable() or character in "\r\n\t"
        )
        if "\x00" in text or allowed / float(len(text)) < 0.85:
            continue
        return label, text
    return None


def inspect_file(path):
    """Read at most PREVIEW_LIMIT bytes and return preview metadata.

    The selected path must currently be a regular file. It is opened in binary
    read-only mode; the contents are never executed or written. File size comes
    from filesystem metadata, so large files are not loaded into memory.
    """
    full_path = os.path.abspath(path)
    file_stat = os.stat(full_path, follow_symlinks=False)
    if not stat.S_ISREG(file_stat.st_mode):
        raise ValueError("The selected path is not a regular file.")

    with open(full_path, "rb") as source:
        opened_stat = os.fstat(source.fileno())
        if not stat.S_ISREG(opened_stat.st_mode):
            raise ValueError("The selected path is not a regular file.")
        sample = source.read(PREVIEW_LIMIT)

    extension = os.path.splitext(full_path)[1].lower()
    text_info = None
    if extension not in KNOWN_FORMATS:
        text_info = _decode_text_sample(sample)

    return {
        "format": detect_format(os.path.basename(full_path), sample),
        "size": format_size(file_stat.st_size),
        "size_bytes": file_stat.st_size,
        "hex": format_hex_preview(sample),
        "text": text_info[1] if text_info is not None else None,
        "bytes_read": len(sample),
    }
