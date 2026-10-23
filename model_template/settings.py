"""Settings so TEMPLATES DIRS are in play for template member scanning."""

from pathlib import Path

INSTALLED_APPS = ["model_template"]
SECRET_KEY = "x"
ROOT_URLCONF = "model_template.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(Path(__file__).resolve().parent / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": []},
    }
]
