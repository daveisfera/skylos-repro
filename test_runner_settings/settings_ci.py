"""Secondary settings assign a DIFFERENT runner — not NoDbTestRunner.

Assigning NoDbTestRunner here would incorrectly quiet the canary.
"""

INSTALLED_APPS = ["test_runner_settings"]
SECRET_KEY = "x"
ROOT_URLCONF = "test_runner_settings.urls"

TEST_RUNNER = "test_runner_settings.nodb_test_runner.NoMigrateDiscoverRunner"
