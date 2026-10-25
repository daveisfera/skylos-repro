"""App-package tests.py Django TestCase layout — denser, closer to consumer app/tests.py.

Multiple TestCase classes + imports used only inside tests. Keep one intentional
non-TestCase true positive.
"""

import json
import tempfile
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import SimpleTestCase, TestCase
from django.utils import timezone
from rest_framework.test import APIClient


def _expected_label() -> str:
    return "ready"


def _helper() -> bool:
    return True


def _build_payload(label: str) -> dict:
    return {"label": label, "ts": timezone.now().isoformat()}


class TrackingRegionTestBase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.label = _expected_label()

    def test_label_roundtrip(self):
        payload = json.dumps(_build_payload(self.label))
        self.assertIn("ready", payload)
        self.assertTrue(_helper())


class ScoreboardDashboardTests(TestCase):
    def test_temp_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "out.json"
            path.write_text(json.dumps({"ok": True}))
            self.assertTrue(path.exists())

    def test_dates(self):
        start = date.today()
        end = start + timedelta(days=7)
        self.assertGreater(end, start)


class CommandSmokeTests(SimpleTestCase):
    def test_call_command_import_present(self):
        # call_command is imported for TestCase-style command tests in consumer apps.
        self.assertTrue(callable(call_command))


class ValidationPathTests(TestCase):
    def test_validation_error_type(self):
        with self.assertRaises(ValidationError):
            raise ValidationError("bad")


class UnusedHelperTests:
    """Not a TestCase — intentional true positive."""

    def check(self):
        return False
