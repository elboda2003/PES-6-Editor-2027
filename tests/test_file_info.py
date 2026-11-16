"""Tests for bounded, read-only file metadata and preview helpers."""

import os
import tempfile
import unittest
from datetime import datetime

from pes6_editor.core.file_info import (
    format_size,
    get_extension,
    get_file_details,
)
from pes6_editor.core.file_preview import (
    PREVIEW_LIMIT,
    detect_format,
    format_hex_preview,
    inspect_file,
)


class FileInfoTests(unittest.TestCase):
    def test_extension_for_file(self):
        self.assertEqual(get_extension("EDIT.bin"), ".bin")

    def test_extension_for_name_without_extension(self):
        self.assertEqual(get_extension("README"), "(none)")

    def test_format_size_in_bytes(self):
        self.assertEqual(format_size(12), "12 bytes")

    def test_format_size_in_kilobytes(self):
        self.assertEqual(format_size(2048), "2.0 KB (2048 bytes)")

    def test_file_details_include_name_extension_path_size_and_modified_time(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            file_path = os.path.join(temporary_directory, "EDIT.bin")
            with open(file_path, "wb") as test_file:
                test_file.write(b"test data")

            expected_time = 1609459200
            os.utime(file_path, (expected_time, expected_time))
            details = get_file_details(file_path)

        self.assertEqual(details["name"], "EDIT.bin")
        self.assertEqual(details["extension"], ".bin")
        self.assertEqual(details["size"], "9 bytes")
        self.assertEqual(details["path"], os.path.abspath(file_path))
        self.assertEqual(
            details["modified"],
            datetime.fromtimestamp(expected_time).strftime("%Y-%m-%d %H:%M:%S"),
        )


class FilePreviewTests(unittest.TestCase):
    def _make_file(self, folder, name, data):
        path = os.path.join(folder, name)
        with open(path, "wb") as output:
            output.write(data)
        return path

    def test_detects_common_pes_extensions_without_parsing_or_execution(self):
        expected = {
            "game.afs": "AFS archive",
            "game.bin": "Binary data file",
            "game.dat": "Data file",
            "game.img": "Image/disk data file",
            "game.exe": "Windows executable",
        }
        for filename, description in expected.items():
            with self.subTest(filename=filename):
                self.assertIn(description, detect_format(filename, b"sample text"))

    def test_hex_preview_shows_offsets_and_hex_bytes(self):
        rendered = format_hex_preview(b"\x00\x41\xff")
        self.assertIn("00000000", rendered)
        self.assertIn("00 41 FF", rendered)
        self.assertIn(".A.", rendered)

    def test_text_preview_only_for_safely_recognized_unknown_text(self):
        with tempfile.TemporaryDirectory() as folder:
            text_path = self._make_file(folder, "notes.txt", b"hello\nPES 6")
            binary_path = self._make_file(folder, "resource.bin", b"hello\nPES 6")
            mixed_path = self._make_file(folder, "unknown.datx", b"\x00\xff\x01")

            text_result = inspect_file(text_path)
            binary_result = inspect_file(binary_path)
            mixed_result = inspect_file(mixed_path)

        self.assertIn("Text file", text_result["format"])
        self.assertEqual(text_result["text"], "hello\nPES 6")
        self.assertIsNone(binary_result["text"])
        self.assertIsNone(mixed_result["text"])

    def test_large_file_reads_only_first_256_bytes(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self._make_file(folder, "large.unknown", b"A" * (1024 * 1024))
            result = inspect_file(path)

        self.assertEqual(result["size_bytes"], 1024 * 1024)
        self.assertEqual(result["bytes_read"], PREVIEW_LIMIT)
        self.assertEqual(len(result["hex"].splitlines()), 16)

    def test_empty_file_has_empty_hex_preview(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self._make_file(folder, "empty.bin", b"")
            result = inspect_file(path)
        self.assertEqual(result["hex"], "(empty file)")
        self.assertIsNone(result["text"])


if __name__ == "__main__":
    unittest.main()
