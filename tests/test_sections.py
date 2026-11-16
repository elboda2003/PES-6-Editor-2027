"""Non-GUI tests for application section availability."""

import unittest

from pes6_editor.core.sections import SECTION_BY_ID


class SectionStatusTests(unittest.TestCase):
    def test_requested_sections_are_registered(self):
        expected = {
            "dashboard",
            "file_browser",
            "afs_inspector",
            "players",
            "teams",
            "transfers",
            "competitions",
            "stadiums",
            "graphics",
            "settings",
        }
        self.assertEqual(set(SECTION_BY_ID), expected)

    def test_unimplemented_editors_are_disabled(self):
        for section_id in (
            "players",
            "teams",
            "transfers",
            "competitions",
            "stadiums",
            "graphics",
        ):
            with self.subTest(section=section_id):
                section = SECTION_BY_ID[section_id]
                self.assertFalse(section["enabled"])
                self.assertIn("Not implemented", section["status"])
                self.assertIn("unavailable", section["status"])

    def test_real_tools_are_enabled(self):
        for section_id in (
            "dashboard",
            "file_browser",
            "afs_inspector",
            "settings",
        ):
            with self.subTest(section=section_id):
                self.assertTrue(SECTION_BY_ID[section_id]["enabled"])


if __name__ == "__main__":
    unittest.main()
