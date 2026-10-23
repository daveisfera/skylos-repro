"""Test module — unittest discovers TestCase subclasses by convention."""

import unittest


def _expected_label() -> str:
    return "ready"


class DemoAPITests(unittest.TestCase):
    def test_label(self):
        self.assertEqual(_expected_label(), "ready")


class UnusedHelperTests:
    """Not a TestCase — may still be unused noise; keep out of discovery contract."""

    def check(self):
        return False
