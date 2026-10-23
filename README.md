# Skylos false-positive reproducer

Minimal examples of patterns that [Skylos](https://github.com/duriantaco/skylos) may flag at 80% confidence but are required by framework/runtime conventions. Each file is intentionally free of `# skylos: ignore` comments.

Older cases (01–05, 08, 10, signals, self-import) came from awresports apps. Later cases came from web-server unused triage ([`unused-review.md`](unused-review.md)), then were **hardened** to match Skylos’s own Django/importlib fixture shapes (valid package names, real `django.*` / `unittest` imports, recognizable settings with `INSTALLED_APPS` + markers).

Upstream tracking: [duriantaco/skylos#1056](https://github.com/duriantaco/skylos/issues/1056).

## Verified (2026-10-23, after repro cleanup)

| Version | Image |
|---------|-------|
| Baseline (default) | `ghcr.io/duriantaco/skylos:4.35.0-python3.11` |
| Latest compared | `ghcr.io/duriantaco/skylos:5.0.0-python3.11` |

### Still false-positive on 5.0.0 (real gaps)

| Case | Path | What’s flagged |
|------|------|----------------|
| 04 | `04_django_url_converter.py` | `register_converter` wrapper |
| 07 | `template_static_js/` | JS `greet` only loaded via `{% static %}` |
| 12 | `auth_backend/` | `TokenAuthBackend.authenticate` / `get_user` (class itself is live via settings) |
| 14 | `test_module/` | `DemoAPITests(unittest.TestCase)` |

### Cleared after repro cleanup (were invalid/stub repros, not analyzer gaps on 5.0.0)

Management `Command` (`mgmt_command/`), settings-wired middleware/storage (`settings_wired/`), `LOGGING` formatter (`logging_infra/`), importlib plugin class (`processor_plugin/`), Django form field (`django_form_field/`), template-only model (`model_template/`), provider interface (`provider_iface/`).

Intentional true positives still reported: `mgmt_command` → `unused_export_job`; `auth_backend` → `StaleAuthBackend`; `processor_plugin` → `unused_plugin_hook`; `test_module` → `UnusedHelperTests`.

### Fixed in 5.0.0 vs 4.35.0 (legacy cases)

Duck-typed wrapper (02); Celery router + params (08); error-handler / migration unused params (03, 05); signals import; empty `admin.py` (10). Gunicorn config (01) already clean since 4.34.0.

### Never reproduced as FP (correctly live)

In-file helpers (`in_file_uses/` with module-level `RESULT`); dict-map dynamic dispatch (`dynamic_dispatch/`); cross-file `get_hls_info` (`cross_file_miss/`).

## Cases

| Label | Path | Pattern | Notes |
|-------|------|---------|-------|
| 01 | `01_gunicorn_config.py` | Gunicorn config globals | Fixed in 4.34.0 |
| 02 | `02_duck_typing.py` | Duck-typed external client | Fixed in 5.0.0 |
| 03 | `03_django_error_handlers.py` | URLconf error handlers | Params fixed in 5.0.0 |
| 04 | `04_django_url_converter.py` | `register_converter` | **Still FP on 5.0.0** |
| 05 | `05_django_migration/` | `RunPython` callback params | Fixed in 5.0.0 |
| 07 | `template_static_js/` | `{% static %}` → JS export | **Still FP on 5.0.0** |
| 08 | `08_celery_router.py` | Celery `task_routes` | Fixed in 5.0.0 |
| — | `self_import_pkg/` | Package side-effect import | Circular-import noise |
| — | `django_signals_app/` | `AppConfig.ready()` signals | Fixed in 5.0.0 |
| 10 | `10_empty_admin/` | Empty `admin.py` | Fixed in 5.0.0 |
| 11 | `mgmt_command/` | `management/commands` + `BaseCommand` | Cleared on 5.0.0 after cleanup |
| 12 | `auth_backend/` | `AUTHENTICATION_BACKENDS` | **Methods still FP**; class live on 5.0.0 |
| 13 | `settings_wired/` | `MIDDLEWARE` / `STORAGES` | Cleared on 5.0.0 after cleanup |
| 14 | `test_module/` | `unittest.TestCase` | **Still FP on 5.0.0** |
| 15 | `model_template/` | Template-only model method | Cleared on 5.0.0 after cleanup |
| 16 | `provider_iface/` | Provider interface methods | Cleared on 5.0.0 after cleanup |
| 17 | `in_file_uses/` | Heavy in-file helper uses | Non-repro (correctly live) |
| 18 | `logging_infra/` | `LOGGING` `"()"` formatter | Cleared on 5.0.0 after cleanup |
| 19 | `processor_plugin/` | `importlib.import_module` plugin | Cleared on 5.0.0 after cleanup |
| 20 | `django_form_field/` | Custom `forms.Field` on `Form` | Cleared on 5.0.0 after cleanup |
| 21 | `dynamic_dispatch/` | Name→callable map | Non-repro (correctly live) |
| 22 | `cross_file_miss/` | Cross-file import use | Non-repro (correctly live) |

## Run

```bash
./run.sh                      # 4.35.0-python3.11 (default)
./run.sh 5.0.0-python3.11     # latest compared here
```

Requires Docker. Optional first argument is the GHCR tag after `ghcr.io/duriantaco/skylos:`.
