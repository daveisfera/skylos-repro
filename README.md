# Skylos false-positive reproducer

Minimal examples of patterns that [Skylos](https://github.com/duriantaco/skylos) flags at 80% confidence but are required by framework/runtime conventions. Each file is intentionally free of `# skylos: ignore` comments.

Older cases (01–04) came from [awresports/hls-server](https://github.com/awresports/hls-server). Cases 05–10 came from [awresports/web-server](https://github.com/awresports/web-server) on 2026-08-28. Cases 11–22 come from the keep-categories in [`unused-review.md`](unused-review.md) (web-server unused triage).

## Verified (2026-10-23)

| Version | Image |
|---------|-------|
| Baseline (default) | `ghcr.io/duriantaco/skylos:4.35.0-python3.11` |
| Latest compared | `ghcr.io/duriantaco/skylos:5.0.0-python3.11` |

**Fixed in 5.0.0** (flagged on 4.35.0, clean on 5.0.0): duck-typed wrapper `load_m3u8_from_s3` (02); Celery `route_task` + unused router params (08); Django error-handler / migration / auth unused params (03, 05, 12); `AppConfig` signals import (django_signals_app); empty `admin.py` `SKY-E002` (10); unused entry `build_report` / `describe` (17, 22).

**Still false-positive on 5.0.0:** template-loaded JS `greet` (07); `register_converter` wrapper (04); management `Command` (11); auth backend / middleware / storage wired only by settings strings (12, 13); test `DemoAPITests` (14); template-only model `Record` (15); unused interface method `Provider.schedule_dates` (16); logging `JSONFormatter` (18); processor `IntegrateSessions` (19); form field / form class (20).

**Did not reproduce the intended FP on 4.35.0:** in-file helpers in 17 (`device_id_check` / `_hardware_health_status` correctly live); dict-map dynamic dispatch in 21 (handlers correctly live); cross-file `get_hls_info` in 22 (import correctly live). Gunicorn config (01) already clean since 4.34.0.

Note: 5.0.0 reported `SKY-ANALYSIS-INCOMPLETE` once on `17_in_file_uses/health.py` (1 of 51 candidates abstained from dead-code reporting).

## Cases

| File | Pattern | Why it looks dead | How it is actually used |
|------|---------|-------------------|-------------------------|
| `01_gunicorn_config.py` | Module-level config globals + hook | No in-repo references | Gunicorn reads settings by attribute name and calls `worker_exit`. **Fixed in 4.34.0** — no longer flagged. |
| `02_duck_typing.py` | Duck-typed `download()` + wrapper | Wrapper has no other callers | `m3u8.load(..., http_client=...)` calls `download()`. **5.0.0** no longer flags `load_m3u8_from_s3`. |
| `03_django_error_handlers.py` | `handler400` / `403` / `404` / `500` | Assigned but never imported | Django looks these names up in the root URLconf. Handlers live in 4.34+; **params fixed in 5.0.0**. |
| `04_django_url_converter.py` | `regex` on a converter class | Only `to_python` / `to_url` look called | `register_converter` reads `regex` reflectively. **Still flags** the local `register_converter` wrapper on 5.0.0. |
| `05_django_migration/migrations/0001_initial.py` | `RunPython` callback signature | `apps` / `schema_editor` unused | Django always calls `forwards(apps, schema_editor)`. **Params fixed in 5.0.0**. |
| `07_template_static_js/` | JS `export` loaded from a Django template | No ES import of `greet` | `{% static 'widget.js' %}` loads the file in the browser. **Still FP on 5.0.0**. |
| `08_celery_router.py` | Celery router + unused callback args | Function and `args` / `kwargs` / `task` / `kw` unused | Celery calls `route_task(...)` via the dotted-path string. **Fixed in 5.0.0**. |
| `self_import_pkg/` | Package imports its own `celery` submodule | One-node import cycle | `celery worker -A self_import_pkg` needs the side-effect import. |
| `django_signals_app/` | `AppConfig.ready()` imports `signals` | Import looks unused | Django only connects `@receiver` handlers if `ready()` imports the module. **Fixed in 5.0.0**. |
| `10_empty_admin/admin.py` | Comment-only `admin.py` | `SKY-E002` empty file | Django still loads `<app>/admin.py` when the app is installed. **Fixed in 5.0.0**. |
| `11_management_command/` | `management/commands/` entry | `Command` never imported | `manage.py <name>` loads the module by path. **Still FP on 5.0.0**. |
| `12_auth_backend/` | `AUTHENTICATION_BACKENDS` string | Backend class never imported | Django loads the dotted path from settings. **Still FP on 5.0.0**. |
| `13_settings_middleware_storage/` | `MIDDLEWARE` / storage strings | Classes never imported | Django loads dotted paths from settings. **Still FP on 5.0.0**. |
| `14_test_module/` | TestCase subclass | Class never imported | Test runners discover `tests.py` / `Test*` classes. **Still FP on 5.0.0**. |
| `15_model_template_method/` | Model method in template | No Python call sites | `{{ record.get_display_name }}` in a Django template. **Still FP on 5.0.0**. |
| `16_provider_interface/` | Interface / override methods | Override not named at call site | Duck-typed `provider.scoreboard(...)` on base type; `schedule_dates` is part of the provider contract. **Still FP on 5.0.0**. |
| `17_in_file_uses/` | Helpers used many times in-file | (web-server reported FPs) | On 4.35.0 helpers were correctly live; only orphan entry `build_report` flagged (gone in 5.0.0). |
| `18_logging_infra/` | `LOGGING` formatter path | Formatter never imported | Django logging config loads `()` dotted path. **Still FP on 5.0.0**. |
| `19_processor_plugin/` | Processor loaded by name | Class never imported | `importlib.import_module` + `getattr` by string. **Still FP on 5.0.0**. |
| `20_django_form_field/` | Custom `Field` on a Form | Field class / `clean` look unused | Declared as `facility = FacilityChoiceField(...)`. **Still FP on 5.0.0**. |
| `21_dynamic_dispatch/` | Name→callable command map | Handlers only reached by string key | `COMMANDS["reboot"](...)` — **did not FP on 4.35.0** (map values count as uses). |
| `22_cross_file_miss/` | Helper used from another file | (web-server “missed elsewhere”) | `from hls_helpers import get_hls_info` — **did not FP on 4.35.0**; only unused entry `describe` flagged (gone in 5.0.0). |

Not reproduced (do not add): Django `class Migration` (known since 4.34.0), Django view `request` / `*args` / `**kwargs` when the view is in `urlpatterns`.

## Run

```bash
./run.sh                      # 4.35.0-python3.11 (default)
./run.sh 5.0.0-python3.11     # latest compared here
```

Requires Docker. Optional first argument is the GHCR tag suffix after `ghcr.io/duriantaco/skylos:`.

## Expected fix

Skylos should treat these convention-based entry points as live without per-symbol suppressions:

1. **Config modules** — already fixed for gunicorn globals in 4.34.0
2. **Duck-typed protocols** — methods invoked on values passed to external libraries (**improved in 5.0.0**)
3. **Django URLconf handlers** — `handler400` / `403` / `404` / `500`, including their `request` / `exception` parameters (**params fixed in 5.0.0**)
4. **Django path converters** — `regex` (and related protocol members) on classes passed to `register_converter` (wrapper still flagged)
5. **Django migrations** — `RunPython` / `RunSQL` callbacks always receive `apps` and `schema_editor` (**fixed in 5.0.0**)
6. **Template-loaded JS** — `{% static %}` / `<script src>` is a use (**still open**)
7. **Celery routers** — dotted-path `task_routes` callables, including unused required parameters (**fixed in 5.0.0**)
8. **Package side-effect imports** — `from pkg import celery` is not a circular dependency
9. **`AppConfig.ready()` signal imports** — `import <app>.signals` is load-bearing (**fixed in 5.0.0**)
10. **Django `admin.py` stubs** — an empty admin module is a conventional keep (**fixed in 5.0.0**)
11. **Management commands** — `management/commands/*.py` `Command` classes (**still open**)
12. **Settings-wired classes** — `AUTHENTICATION_BACKENDS`, `MIDDLEWARE`, storage, `LOGGING` dotted paths (**still open**)
13. **Test modules** — discovered `TestCase` subclasses (**still open**)
14. **Template model methods** — `{{ obj.method }}` (**still open**)
15. **Provider / interface methods** — duck-typed protocol members (**still open**)
16. **Processor plugins** — `importlib` + `getattr` by configured name (**still open**)
17. **Django form fields** — custom `Field` subclasses used as form attributes (**still open**)
