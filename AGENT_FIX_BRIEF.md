# Skylos dead-code false positives — fix brief (post-#1068 gaps)

Hand this to an agent with the **skylos** source. Goal: stop reporting the symbols below at `-c 80` using evidence-based liveness (not broad ignores).

| Item | Detail |
|------|--------|
| Upstream | [#1056](https://github.com/duriantaco/skylos/issues/1056), [#1068](https://github.com/duriantaco/skylos/pull/1068) |
| Repros | https://github.com/daveisfera/skylos-repro |
| Consumer evidence | [`upstream-fp-reproducers.md`](upstream-fp-reproducers.md) (large Django app still noisy after #1068) |
| Verify | `skylos <skylos-repro> -c 80 --format concise` |

**Note:** #1068 quieted the first small Django batch for some builds, then a precision follow-up (`preserve Django liveness precision`) brought back stricter behavior for converters / static JS. Re-run the suite against the PR HEAD you are fixing.

---

## Still red on PR #1068 head (fix these next)

### 1. Celery `result_backend="pkg.mod:ClassName"` (colon path)

**Repro:** `celery_result_backend/`

- `backend.py` — `class RedisClusterBackend`
- `celery_app.py` — `result_backend="celery_result_backend.backend:RedisClusterBackend"` only

**Flagged:** `RedisClusterBackend`

**Why live:** Celery loads result backends from `module:Class` / `module.Class` strings. Not `AUTHENTICATION_BACKENDS`.

**Accept:** class not unused. Cover colon and dotted forms on `result_backend` / `celery_result_backend` conf keys.

---

### 2. Multi-method duck-typed provider / client

**Repro:** `provider_iface/provider.py`

`NcaaClient` implements many public methods; call sites only use `provider.scoreboard(...)` on the `Provider` base type.

**Flagged:** `Provider.schedule_dates`, `.division_teams`, `.game_detail`, `.box_score`, `.play_by_play` (and similarly concrete overrides if reported)

**Accept:** public contract methods on the provider hierarchy are live when the type is used as a duck-typed client; private `_graphql` with in-class callers stays live; truly unused privates may still flag.

---

### 3. Local `register_converter` wrapper / django_urls shim

**Repro:** `04_django_url_converter.py` + `django_urls.py`

**Flagged:** `register_converter`

**Accept:** project wrappers that forward to `django.urls.register_converter` (including local `django_urls` shims) count as registration entrypoints; converter class protocol stays live.

---

### 4. `{% static %}` → JS export

**Repro:** `template_static_js/`

**Flagged:** `greet`

**Accept:** exports / top-level functions in a JS file referenced via `{% static %}` / `<script src>` are browser entrypoints.

---

### 5. Satellite `LOGGING` `"()"` (5.0.0; should stay quiet on #1068)

**Repro:** `logging_infra/` — `from …settings_logging import LOGGING` with `"()"` factories.

**Flagged on 5.0.0:** `JSONFormatter`, `ExtraAdder`  
**Expect on #1068:** quiet (regression if they return).

---

### 6. `django.test.TestCase` discovery (5.0.0; quiet on #1068)

**Repro:** `test_module/tests.py` — `DemoAPITests(TestCase)` + helpers/imports used only in tests.

**Flagged on 5.0.0:** `DemoAPITests`  
**Intentional TP:** `UnusedHelperTests` (keep reporting)

---

## Regression fixtures (should stay green)

Do not delete; fail the PR if these start reporting as unused again:

| Fixture | Live symbols |
|---------|----------------|
| `receiver_signals/` | `on_item_created`, `on_item_deleted` |
| `test_runner_settings/` | `NoDbTestRunner` when `settings_ci.TEST_RUNNER` points at it |
| `mgmt_command_helpers/` | `_format_name` called from `Command.handle`; `_dead_helper` may flag |
| `mgmt_command/` | `_restart_worker` via `autoreload.run_with_reloader` |
| `registry_getattr/` | `create_item`, `get_item_schema` via nested registry + `getattr` |
| `same_module_helper/` | `_validate_phone` with same-file callers |
| `django_form_field/` | `FacilityChoiceField` on a Form used from a urlpatterns view |
| `model_template/` | `get_display_name`, `next_steps_message`, `get_current_status_display` in templates |
| `auth_backend/`, `settings_wired/`, `processor_plugin/`, … | earlier #1056 shapes |

---

## Suggested skylos areas

- Celery string entrypoints / `result_backend` — near existing `task_routes` handling in `framework_liveness.py`
- Provider / interface methods — duck-typing / external protocol evidence
- Converters — `django_converter_liveness.py` (shim / uncalled wrapper precision)
- Static JS — `browser_refs.py` + TS/JS export liveness
- Settings satellite imports — `django_framework_liveness.py`

## Workflow

1. Confirm red list with `skylos-repro` at `-c 80`.
2. Add skylos pytest fixtures mirroring these packages (see `test_django_app_repro_liveness.py` style from #1068).
3. Smallest evidence-based fix; re-run full skylos-repro tree.
4. Note on the PR which web-server keep-buckets from `upstream-fp-reproducers.md` are addressed.

## Failure signature (PR #1068 @ `68c00c47`, strengthened suite)

```
04_django_url_converter.py:…  unused function: register_converter
provider_iface/provider.py:…  unused function: Provider.schedule_dates
provider_iface/provider.py:…  unused function: Provider.division_teams
provider_iface/provider.py:…  unused function: Provider.game_detail
provider_iface/provider.py:…  unused function: Provider.box_score
provider_iface/provider.py:…  unused function: Provider.play_by_play
template_static_js/static/widget.js:…  unused function: greet
celery_result_backend/backend.py:…  unused class: RedisClusterBackend
test_module/tests.py:…  unused class: UnusedHelperTests
```
