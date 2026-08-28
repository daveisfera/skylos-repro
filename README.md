# Skylos false-positive reproducer

Minimal examples of patterns that [Skylos](https://github.com/duriantaco/skylos) **v4.35.0** flags at 80% confidence but are required by framework/runtime conventions. Each file is intentionally free of `# skylos: ignore` comments.

Older cases (01–04) came from [awresports/hls-server](https://github.com/awresports/hls-server). Newer cases (05+) came from [awresports/web-server](https://github.com/awresports/web-server) on 2026-08-28.

Verified with `ghcr.io/duriantaco/skylos:4.35.0-python3.11`. All cases below still reproduce except gunicorn config (already fixed in 4.34.0).

## Cases

| File | Pattern | Why it looks dead | How it is actually used |
|------|---------|-------------------|-------------------------|
| `01_gunicorn_config.py` | Module-level config globals + hook | No in-repo references | Gunicorn reads settings by attribute name and calls `worker_exit`. **Fixed in 4.34.0** — no longer flagged. |
| `02_duck_typing.py` | Duck-typed `download()` + wrapper | Wrapper has no other callers | `m3u8.load(..., http_client=...)` calls `download()`. The class is rescued by grep-verify; `load_m3u8_from_s3` is still flagged. |
| `03_django_error_handlers.py` | `handler400` / `403` / `404` / `500` | Assigned but never imported | Django looks these names up in the root URLconf. The handlers themselves are live in 4.34.0; **`request` / `exception` params are still flagged**. |
| `04_django_url_converter.py` | `regex` on a converter class | Only `to_python` / `to_url` look called | `register_converter` reads `regex` reflectively. The class is rescued by grep-verify; the local `register_converter` wrapper is still flagged. |
| `05_django_migration/migrations/0001_initial.py` | `RunPython` callback signature | `apps` / `schema_editor` unused | Django always calls `forwards(apps, schema_editor)`. The `Migration` class itself is no longer flagged. |
| `07_template_static_js/` | JS `export` loaded from a Django template | No ES import of `greet` | `{% static 'widget.js' %}` loads the file in the browser. |
| `08_celery_router.py` | Celery router + unused callback args | Function and `args` / `kwargs` / `task` / `kw` unused | Celery calls `route_task(name, args, kwargs, options, task=..., **kw)` via the dotted-path string. 4.34.0 rescued the function via grep-verify; **4.35.0 flags the function and the unused params**. |
| `self_import_pkg/` | Package imports its own `celery` submodule | One-node import cycle | `celery worker -A self_import_pkg` needs the side-effect import. Skylos reports `SKY-CIRC` `self_import_pkg → self_import_pkg`. |
| `django_signals_app/` | `AppConfig.ready()` imports `signals` | Import looks unused | Django only connects `@receiver` handlers if `ready()` imports the module. |
| `10_empty_admin/admin.py` | Comment-only `admin.py` | `SKY-E002` empty file | Django still loads `<app>/admin.py` when the app is installed. |

Not reproduced (do not add): Django `class Migration` (known since 4.34.0), Django view `request` / `*args` / `**kwargs` when the view is in `urlpatterns`.

## Run

```bash
./run.sh
```

Requires Docker.

## Expected fix

Skylos should treat these convention-based entry points as live without per-symbol suppressions:

1. **Config modules** — already fixed for gunicorn globals in 4.34.0
2. **Duck-typed protocols** — methods invoked on values passed to external libraries
3. **Django URLconf handlers** — `handler400` / `403` / `404` / `500`, including their `request` / `exception` parameters
4. **Django path converters** — `regex` (and related protocol members) on classes passed to `register_converter`
5. **Django migrations** — `RunPython` / `RunSQL` callbacks always receive `apps` and `schema_editor`
6. **Template-loaded JS** — `{% static %}` / `<script src>` is a use
7. **Celery routers** — dotted-path `task_routes` callables, including unused required parameters
8. **Package side-effect imports** — `from pkg import celery` is not a circular dependency
9. **`AppConfig.ready()` signal imports** — `import <app>.signals` is load-bearing
10. **Django `admin.py` stubs** — an empty admin module is a conventional keep
