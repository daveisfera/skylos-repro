# Skylos false-positive reproducer

Minimal fixtures shaped like **working large Django app patterns**. See [`upstream-fp-reproducers.md`](upstream-fp-reproducers.md) for gaps that remain after [#1056](https://github.com/duriantaco/skylos/issues/1056) / [#1068](https://github.com/duriantaco/skylos/pull/1068) / [#1072](https://github.com/duriantaco/skylos/pull/1072).

Upstream tracking: [#1056](https://github.com/duriantaco/skylos/issues/1056).  
Agent brief for analyzer fixes: [`AGENT_FIX_BRIEF.md`](AGENT_FIX_BRIEF.md).

**Fixture validity rule:** if a soft-key goes quiet in this repo while the matching consumer canary still FLAGs at `-c 80`, the fixture is **invalid** — harden the extract (do not claim fixed).

> Doc note: do not write `ClassName.method` forms for canaries in markdown here — skylos rescues those as `documented_public_api` and invalidates the provider fixture.

## Verified (2026-10-24) — literal extracts

| Build | How |
|-------|-----|
| Released 5.0.0 | `./run.sh 5.0.0-python3.11` or `skylos . -c 80 --format concise` |
| PR under test | install that checkout editable, then same scan |

### Tier-1 canaries that must FLAG on 5.0.0 (literal extracts)

| Fixture | Soft-keys (FLAG) | Production shape |
|---------|------------------|------------------|
| `lovable_registry/` | `create_game`, `update_game`, `delete_game_safely`, `create_practice`, `get_game_form_schema`, `get_team_schedule`, `get_team_roster`, `get_user_teams` | nested registry + factory `getattr` + `type(...)` |
| `checkout_phone/` | `_validate_phone` (`called_by` nested serializers, `references: 0`) | checkout views module; no `run_checks()` toy entry |
| `django_form_field/` | `FacilityChoiceField` (class) | string-only type map; form usage commented |
| `test_runner_settings/` | `NoDbTestRunner` | only in commented `TEST_RUNNER` on primary settings |
| `provider_iface/` | `schedule_dates`, `division_teams`, `game_detail`, `box_score`, `play_by_play` | multi-method client; factory + pipeline call sites |
| `mgmt_command_helpers/` | helpers after `handle` (when consumer still FLAGs that shape) | private helpers defined below `Command.handle` |
| `test_module/` | intentional TP `UnusedHelperTests`; TestCase classes quiet once discovery works | denser `app/tests.py` layout |
| `celery_result_backend/` | `RedisClusterBackend` on 5.0.0; must stay quiet on #1072 | `result_backend="pkg.mod:Class"` |

### Also keep (regression / other shapes)

| Fixture | Notes |
|---------|-------|
| `25_lovable_registry_factory/` | numbered twin of lovable factory extract |
| `26_checkout_phone_serializers/` | numbered twin of checkout phone extract |
| `21_django_receiver_signals/`, `receiver_signals/` | `@receiver` — FLAG if consumer signal canaries FLAG on the build under test |
| `22_celery_result_backend_string/` | Celery colon backend twin |
| `23_test_runner_secondary_settings/` | `LegacyNoDbRunner` comment-only; secondary assigns a different runner |
| `24_management_command_helpers/` | helpers-after-handle twin |
| `template_static_js/`, `04_django_url_converter.py`, `logging_infra/` | other #1056 / precision cases |

## Run

```bash
./run.sh                      # 4.35.0-python3.11
./run.sh 5.0.0-python3.11     # released 5.0.0
# PR head (example):
#   pip install -e /path/to/skylos@branch
#   skylos . -c 80 --format concise --no-grep-verify
```

Requires Docker for `./run.sh`.
