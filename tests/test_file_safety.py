"""Tests for copy-only, non-destructive file safety helpers."""

import os
import tempfile
import unittest

from pes6_editor.core.file_safety import (
    create_backup,
    create_working_copy,
    restore_to_new_file,
)


class FileSafetyTests(unittest.TestCase):
    def test_backup_and_working_copy_leave_source_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            source = os.path.join(directory, "EDIT.bin")
            with open(source, "wb") as stream:
                stream.write(b"original game data")

            backup = create_backup(source, os.path.join(directory, "backups"))
            working = create_working_copy(source, os.path.join(directory, "work"))

            for copy_path in (backup, working):
                with open(copy_path, "rb") as stream:
                    self.assertEqual(stream.read(), b"original game data")

            with open(source, "rb") as stream:
                self.assertEqual(stream.read(), b"original game data")

    def test_restore_creates_a_separate_copy(self):
        with tempfile.TemporaryDirectory() as directory:
            backup = os.path.join(directory, "backup.bin")
            with open(backup, "wb") as stream:
                stream.write(b"backup data")

            restored = restore_to_new_file(
                backup,
                os.path.join(directory, "restored"),
            )

            self.assertNotEqual(os.path.abspath(backup), restored)
            with open(restored, "rb") as stream:
                self.assertEqual(stream.read(), b"backup data")
            with open(backup, "rb") as stream:
                self.assertEqual(stream.read(), b"backup data")

    def test_rejects_directory_as_source(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                create_backup(directory, os.path.join(directory, "backups"))

    def test_creates_distinct_paths_for_repeated_backups(self):
        with tempfile.TemporaryDirectory() as directory:
            source = os.path.join(directory, "source.bin")
            with open(source, "wb") as stream:
                stream.write(b"source")

            first = create_backup(source, directory)
            second = create_backup(source, directory)

            self.assertNotEqual(first, second)
            self.assertTrue(os.path.isfile(first))
            self.assertTrue(os.path.isfile(second))


if __name__ == "__main__":
    unittest.main()
