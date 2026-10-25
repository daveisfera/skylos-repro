# Skylos false-positive reproducer

Minimal fixtures shaped like **working large Django app patterns**. See [`upstream-fp-reproducers.md`](upstream-fp-reproducers.md) for the gaps that remain after [#1056](https://github.com/duriantaco/skylos/issues/1056) / [#1068](https://github.com/duriantaco/skylos/pull/1068).

Upstream tracking: [#1056](https://github.com/duriantaco/skylos/issues/1056), [#1068](https://github.com/duriantaco/skylos/pull/1068).  
Agent brief for analyzer fixes: [`AGENT_FIX_BRIEF.md`](AGENT_FIX_BRIEF.md).

## Verified (2026-10-24) — strengthened suite

| Build | How |
|-------|-----|
| Released 5.0.0 | `./run.sh 5.0.0-python3.11` |
| PR #1068 head | `skylos . -c 80 --format concise` from `daveisfera/skylos@fix/django-deadcode-fps-1056` (`68c00c47` when checked) |

### Still false-positive on PR #1068 (and 5.0.0 unless noted)

These are the useful “still red” cases for another upstream fix:

| Fixture | Flagged | Maps to |
|---------|---------|---------|
| `04_django_url_converter.py` | `register_converter` | local django_urls shim (precision pass may still miss) |
| `template_static_js/` | `greet` | `{% static %}` JS export |
| `celery_result_backend/` | `RedisClusterBackend` | Celery `result_backend="pkg.mod:Class"` (**new**) |
| `provider_iface/` | `Provider.schedule_dates` / `division_teams` / `game_detail` / `box_score` / `play_by_play` | multi-method duck-typed client (**strengthened**) |
| `logging_infra/` | `JSONFormatter`, `ExtraAdder` | satellite `LOGGING` — **FP on 5.0.0 only**; quiet on #1068 |
| `test_module/` | `DemoAPITests` | django `TestCase` — **FP on 5.0.0 only**; quiet on #1068 |
| `test_module/` | `UnusedHelperTests` | intentional true positive |

### Added / strengthened but quiet on #1068 (regression guards / already handled)

Keep these so fixes do not regress; they mirror large-app shapes even when already quiet:

| Fixture | Pattern |
|---------|---------|
| `21_django_receiver_signals/` | nested `AppConfig.ready()` → `pkg.feature.signals` (P1.1) |
| `22_celery_result_backend_string/` | Celery `app.conf.update(result_backend="mod:Class")` (P1.2) |
| `23_test_runner_secondary_settings/` | `TEST_RUNNER` on secondary settings module (P1.3) |
| `24_management_command_helpers/` | helpers called from `Command.handle` (P2.2) |
| `25_registry_getattr_handlers/` | nested registry + `getattr(module, name)` (P2.4) |
| `26_same_module_private_helper/` | `_validate_phone` with nested callers + routed view (P3.1) |
| `receiver_signals/`, `test_runner_settings/`, `mgmt_command_helpers/`, … | earlier named copies of the same themes |
| `django_form_field/`, `model_template/`, `processor_plugin/`, … | earlier #1056 suite |

If a large Django app still reports noise in those categories, extend the fixture with a literal snippet rather than deleting it.

## Run

```bash
./run.sh                      # 4.35.0-python3.11
./run.sh 5.0.0-python3.11     # released 5.0.0
# PR head (example):
#   pip install -e /path/to/daveisfera/skylos@fix/django-deadcode-fps-1056
#   skylos . -c 80 --format concise
```

Requires Docker for `./run.sh`.
