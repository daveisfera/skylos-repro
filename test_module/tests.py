"""django.test.TestCase discovery — helpers + imports used only in tests."""

import json

from django.test import TestCase


def _expected_label() -> str:
    return "ready"


def _helper() -> bool:
    return True


class DemoAPITests(TestCase):
    def test_label(self):
        payload = json.dumps({"label": _expected_label()})
        self.assertIn("ready", payload)
        self.assertTrue(_helper())


class UnusedHelperTests:
    """Not a TestCase — intentional true positive."""

    def check(self):
        return False
