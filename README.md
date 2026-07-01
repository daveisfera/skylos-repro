# Skylos false-positive reproducer

Minimal examples of dead-code patterns that [Skylos](https://github.com/duriantaco/skylos) v4.5.0 flags at 80% confidence but are required by framework/runtime conventions. Each file is intentionally free of `# skylos: ignore` comments.

Derived from [awresports/hls-server](https://github.com/awresports/hls-server), which suppresses these today.

## Cases

| File | Pattern | Why it looks dead | How it is actually used |
|------|---------|-------------------|-------------------------|
| `01_gunicorn_config.py` | Module-level config globals + hook function | No in-repo references | Gunicorn imports the module and reads settings by attribute name (`bind`, `workers`, …) and calls `worker_exit` by name |
| `02_duck_typing.py` | Method on a duck-typed client class | No static call site in this module | External `m3u8.load(..., http_client=...)` calls `download()` on whatever object is passed |
| `03_django_error_handlers.py` | `handler400` / `handler403` / `handler404` / `handler500` | Assigned but never imported elsewhere | Django's URL resolver loads the root URLconf and looks up these names for error dispatch |
| `04_django_url_converter.py` | `regex` class attribute on a converter class | Only `to_python` / `to_url` are called directly | `register_converter` reads `regex` (and methods) from the converter class reflectively |

## Run

```bash
./run.sh
```

Requires Docker. Uses the same Skylos image/version as awresports-hls CI (`v4.5.0`, 80% confidence, dead-code analysis).

## Expected fix

Skylos should treat these convention-based entry points as live without requiring per-symbol suppressions:

1. **Config modules** — module globals and named hooks loaded via `getattr` / import-and-introspect (gunicorn, uwsgi, pytest plugins, etc.)
2. **Duck-typed protocols** — methods invoked on values passed to external libraries or `typing.Protocol` implementors
3. **Django URLconf handlers** — `handler400`, `handler403`, `handler404`, `handler500` in the root URLconf module
4. **Django path converters** — `regex` (and related protocol members) on classes passed to `register_converter`
