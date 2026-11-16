"""Tests for read-only file metadata helpers."""

import os
import tempfile
import unittest
from datetime import datetime

from pes6_editor.core.file_info import (
    format_size,
    get_extension,
    get_file_details,
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


if __name__ == "__main__":
    unittest.main()
