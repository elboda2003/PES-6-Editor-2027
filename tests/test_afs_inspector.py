"""Tests for safe AFS archive metadata inspection."""

import os
import struct
import tempfile
import unittest

from pes6_editor.core.afs_inspector import AFSInspectionError, detect_afs, inspect_afs


class AFSInspectorTests(unittest.TestCase):
    def _make_afs(self, folder, name, entry_count, offsets, sizes, real_sizes):
        file_path = os.path.join(folder, name)
        header = b"AFS\x00" + struct.pack("<I", 1) + struct.pack("<I", entry_count)
        table = b""
        for entry_index in range(entry_count):
            table += struct.pack("<IIII", offsets[entry_index], sizes[entry_index], real_sizes[entry_index], 0)
        with open(file_path, "wb") as archive:
            archive.write(header + table)
        return file_path

    def test_detects_afs_signature(self):
        with tempfile.TemporaryDirectory() as folder:
            file_path = os.path.join(folder, "archive.afs")
            with open(file_path, "wb") as archive:
                archive.write(b"AFS\x00\x01\x00\x00\x00\x02\x00\x00\x00")
            self.assertTrue(detect_afs(file_path))

    def test_rejects_invalid_signature(self):
        with tempfile.TemporaryDirectory() as folder:
            file_path = os.path.join(folder, "not_afs.bin")
            with open(file_path, "wb") as archive:
                archive.write(b"NOPE")
            self.assertFalse(detect_afs(file_path))

    def test_valid_archive_reports_entry_count_and_metadata(self):
        with tempfile.TemporaryDirectory() as folder:
            offsets = [12 + 16, 64]
            sizes = [52, 10]
            real_sizes = [52, 10]
            file_path = self._make_afs(folder, "valid.afs", 2, offsets, sizes, real_sizes)
            result = inspect_afs(file_path)

        self.assertTrue(result["header_valid"])
        self.assertEqual(result["entry_count"], 2)
        self.assertEqual(result["entries"][0]["index"], 0)
        self.assertEqual(result["entries"][0]["status"], "ok")
        self.assertEqual(result["entries"][1]["status"], "ok")

    def test_malformed_archive_reports_invalid_boundary(self):
        with tempfile.TemporaryDirectory() as folder:
            file_path = self._make_afs(folder, "broken.afs", 1, [999999], [1000], [1000])
            result = inspect_afs(file_path)

        self.assertEqual(result["entries"][0]["status"], "invalid")
        self.assertIn("offset", result["entries"][0]["reason"])

    def test_truncated_entry_table_raises_error(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "truncated.afs")
            header = b"AFS\x00" + struct.pack("<I", 1) + struct.pack("<I", 1)
            with open(path, "wb") as archive:
                archive.write(header)

            with self.assertRaises(AFSInspectionError):
                inspect_afs(path)


if __name__ == "__main__":
    unittest.main()
