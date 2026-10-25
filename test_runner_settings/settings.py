"""Primary settings — TEST_RUNNER only commented (pitchaware/settings.py)."""

INSTALLED_APPS = ["test_runner_settings"]
SECRET_KEY = "x"
ROOT_URLCONF = "test_runner_settings.urls"

# TEST_RUNNER = "test_runner_settings.nodb_test_runner.NoDbTestRunner"
