"""Tests for read-only file metadata helpers."""

import unittest

from pes6_editor.core.file_info import format_size, get_extension


class FileInfoTests(unittest.TestCase):
    def test_extension_for_file(self):
        self.assertEqual(get_extension("EDIT.bin"), ".bin")

    def test_extension_for_name_without_extension(self):
        self.assertEqual(get_extension("README"), "(none)")

    def test_format_size_in_bytes(self):
        self.assertEqual(format_size(12), "12 bytes")

    def test_format_size_in_kilobytes(self):
        self.assertEqual(format_size(2048), "2.0 KB (2048 bytes)")


if __name__ == "__main__":
    unittest.main()
