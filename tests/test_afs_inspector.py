"""Tests for conservative, read-only AFS signature inspection."""

import os
import tempfile
import unittest

from pes6_editor.core.afs_inspector import (
    AFSInspectionError,
    detect_afs,
    inspect_afs,
)


class AFSInspectorTests(unittest.TestCase):
    def _write(self, directory, name, data):
        path = os.path.join(directory, name)
        with open(path, "wb") as stream:
            stream.write(data)
        return path

    def test_detects_afs_magic_signature(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self._write(directory, "archive.afs", b"AFS\x00extra")
            self.assertTrue(detect_afs(path))

    def test_rejects_invalid_signature(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self._write(directory, "not_afs.bin", b"NOPE")
            self.assertFalse(detect_afs(path))
            with self.assertRaises(AFSInspectionError):
                inspect_afs(path)

    def test_rejects_truncated_signature(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self._write(directory, "truncated.afs", b"AF")
            self.assertFalse(detect_afs(path))
            with self.assertRaises(AFSInspectionError):
                inspect_afs(path)

    def test_recognized_signature_does_not_claim_unverified_layout(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self._write(
                directory,
                "archive.afs",
                b"AFS\x00" + b"\x00" * 64,
            )
            result = inspect_afs(path)

        self.assertTrue(result["header_valid"])
        self.assertFalse(result["format_supported"])
        self.assertIsNone(result["entry_count"])
        self.assertEqual(result["entries"], [])
        self.assertTrue(any("unverified" in note for note in result["notes"]))

    def test_rejects_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(AFSInspectionError):
                inspect_afs(directory)


if __name__ == "__main__":
    unittest.main()
