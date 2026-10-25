"""Secondary settings that assign TEST_RUNNER (accept criterion from upstream brief).

Primary settings.py only has the assignment commented out.
"""

INSTALLED_APPS = ["test_runner_settings"]
SECRET_KEY = "x"
ROOT_URLCONF = "test_runner_settings.urls"

TEST_RUNNER = "test_runner_settings.nodb_test_runner.NoDbTestRunner"
