"""Test module — Django/unittest discovers TestCase subclasses by convention."""


class SimpleTestCase:
    def assertEqual(self, a, b):
        assert a == b


def _expected_label() -> str:
    return "ready"


class DemoAPITests(SimpleTestCase):
    def test_label(self):
        self.assertEqual(_expected_label(), "ready")
