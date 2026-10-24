"""Main settings module — pulls LOGGING in from settings_logging (web-server shape)."""

INSTALLED_APPS = ["logging_infra"]
SECRET_KEY = "x"
ROOT_URLCONF = "logging_infra.urls"

# These imports place the settings in this module's namespace for Django.
from logging_infra.settings_logging import LOGGING  # noqa: F401
