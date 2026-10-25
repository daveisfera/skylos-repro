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

Keep these so fixes do not regress; they mirror web-server shapes even when already quiet:

| Fixture | Pattern |
|---------|---------|
| `receiver_signals/` | `@receiver` + `AppConfig.ready()` (P1.1) |
| `test_runner_settings/` | `TEST_RUNNER` on secondary settings (P1.3) |
| `mgmt_command_helpers/` | helpers called from `Command.handle` (P2.2) |
| `mgmt_command/` | `autoreload.run_with_reloader` callback |
| `registry_getattr/` | nested registry + `getattr(handlers, spec["method"])` (P2.4) |
| `same_module_helper/` | `_validate_phone` with same-file callers (P3.1) |
| `django_form_field/` | `FacilityChoiceField` on a Form used from a view |
| `model_template/` | template-only model methods |
| `processor_plugin/`, `settings_wired/`, `auth_backend/`, … | earlier #1056 suite |

If web-server still reports noise in those categories, the production shape is larger (huge command modules, dynamic names without const propagation, etc.) — extend the fixture with a literal snippet from the app rather than deleting it.

## Run

```bash
./run.sh                      # 4.35.0-python3.11
./run.sh 5.0.0-python3.11     # released 5.0.0
# PR head (example):
#   pip install -e /path/to/daveisfera/skylos@fix/django-deadcode-fps-1056
#   skylos . -c 80 --format concise
```

Requires Docker for `./run.sh`.
