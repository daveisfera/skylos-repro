# Skylos false-positive reproducer

Minimal examples shaped like **working [awresports/web-server](https://github.com/awresports/web-server) patterns** (not “textbook only” Django). Each file is free of `# skylos: ignore` comments.

Package names are valid Python identifiers (digit-leading modules break Skylos dotted-path resolution — production never used those). Inheritance, settings layout, and loaders follow the real app.

Upstream: [duriantaco/skylos#1056](https://github.com/duriantaco/skylos/issues/1056). Source triage: [`unused-review.md`](unused-review.md).

## Verified (2026-10-24) — web-server-shaped repros on 5.0.0

Image: `ghcr.io/duriantaco/skylos:5.0.0-python3.11` (`./run.sh 5.0.0-python3.11`).

### Still false-positive on 5.0.0

| Path | What’s flagged | Web-server analogue |
|------|----------------|---------------------|
| `04_django_url_converter.py` | `register_converter` wrapper | reflective `register_converter` |
| `template_static_js/` | `greet` export | `{% static %}` / script src only |
| `auth_backend/` | `MobileTokenBackend.authenticate` / `get_user` | duck-typed backend in `AUTHENTICATION_BACKENDS` (class is live; methods are not) |
| `logging_infra/` | `JSONFormatter`, `ExtraAdder` | `LOGGING` `"()"` paths in satellite `settings_logging.py` imported into settings |
| `settings_wired/storage.py` | `MediaStorage.save` | `STORAGES` / storage backend methods |
| `test_module/` | `DemoAPITests(unittest.TestCase)` | discovered test classes |

### Realistic shapes that go quiet on 5.0.0 (fixed or covered for this layout)

| Path | Pattern |
|------|---------|
| `mgmt_command/` | Helper passed to `autoreload.run_with_reloader` (celery_watch) — `_restart_worker` not flagged |
| `settings_wired/middleware.py` | Plain `RouteMiddleware` + `_matched_route` in `MIDDLEWARE` — class/helper not flagged |
| `processor_plugin/` | `importlib` + name registry without module-level `RESULT` — `IntegrateSessions` not flagged |
| `django_form_field/` | `ModelChoiceField.label_from_instance` — not flagged |
| `model_template/` | Template-only model methods — not flagged |
| `provider_iface/` | Contract method `schedule_dates` unused at call site — not flagged when provider instance is live |

### Older cases fixed between 4.35.0 and 5.0.0

Duck-typed wrapper (02), Celery router (08), error-handler/migration params (03, 05), signals import, empty `admin.py` (10). Gunicorn (01) fixed since 4.34.0.

## Cases (criterion: mirrors web-server)

| Label | Path | Real shape |
|-------|------|------------|
| 04 | `04_django_url_converter.py` | Local `register_converter` wrapper |
| 07 | `template_static_js/` | `{% static 'widget.js' %}` loads ES `export` |
| 11 | `mgmt_command/` | `autoreload.run_with_reloader(_restart_worker, …)` |
| 12 | `auth_backend/` | Duck-typed `MobileTokenBackend` (no auth base) |
| 13 | `settings_wired/` | Plain middleware + `STORAGES` backend |
| 14 | `test_module/` | `unittest.TestCase` in `tests.py` |
| 15 | `model_template/` | `{{ record.get_display_name }}` only |
| 16 | `provider_iface/` | Duck-typed provider; `schedule_dates` never called |
| 18 | `logging_infra/` | `from …settings_logging import LOGGING` + `"()"` paths |
| 19 | `processor_plugin/` | Name → module path registry + `import_module` / `getattr` |
| 20 | `django_form_field/` | `forms.ModelChoiceField.label_from_instance` |

Plus legacy 01–05, 08, 10, `django_signals_app/`, `self_import_pkg/`, `in_file_uses/`, `dynamic_dispatch/`, `cross_file_miss/`.

## Run

```bash
./run.sh                      # 4.35.0-python3.11 (default)
./run.sh 5.0.0-python3.11     # latest compared here
```

Requires Docker.
