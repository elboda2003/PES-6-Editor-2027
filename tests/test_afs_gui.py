"""Non-interactive tests for the AFS inspector GUI launcher."""

import tempfile
import unittest
from unittest import mock

from pes6_editor.gui import afs_inspector


class AFSInspectorLauncherTests(unittest.TestCase):
    def test_valid_afs_opens_separate_read_only_inspector_window(self):
        with tempfile.NamedTemporaryFile(suffix=".afs") as archive:
            window = mock.Mock()
            panel = mock.Mock()
            with mock.patch.object(afs_inspector.tk, "Toplevel", return_value=window) as toplevel:
                with mock.patch.object(afs_inspector, "detect_afs", return_value=True):
                    with mock.patch.object(afs_inspector, "AFSInspectorPanel", return_value=panel):
                        result = afs_inspector.open_afs_inspector(archive.name, mock.Mock())

        self.assertIs(result, window)
        toplevel.assert_called_once()
        panel.inspect_path.assert_called_once_with(archive.name)
        panel.pack.assert_called_once()

    def test_invalid_signature_is_rejected_without_opening_window(self):
        with tempfile.NamedTemporaryFile(suffix=".afs") as archive:
            with mock.patch.object(afs_inspector, "detect_afs", return_value=False):
                with mock.patch.object(afs_inspector.tk, "Toplevel") as toplevel:
                    with mock.patch.object(afs_inspector.messagebox, "showerror") as showerror:
                        result = afs_inspector.open_afs_inspector(archive.name, mock.Mock())

        self.assertIsNone(result)
        toplevel.assert_not_called()
        showerror.assert_called_once()


if __name__ == "__main__":
    unittest.main()
