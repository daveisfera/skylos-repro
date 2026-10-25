# Skylos agent brief: fix real large-app FPs (not toy fixtures)

You are working in **https://github.com/duriantaco/skylos** (fork OK).  
Consumer that still fails: **https://github.com/awresports/web-server** (sibling clone `~/projects/awresports/web-server`).

Prior PRs ([#1059](https://github.com/duriantaco/skylos/pull/1059), [#1068](https://github.com/duriantaco/skylos/pull/1068), [#1072](https://github.com/duriantaco/skylos/pull/1072)) repeatedly:

1. Wrote a **flattened** `tmp_path` fixture.
2. Made `pytest` green on that fixture.
3. Claimed the production FP was fixed.

Then a scan of **web-server at `-c 80`** still flagged the same symbols (or totals went **up**). That loop is the bug in the workflow, not just in the analyzer.

**Your job is done only when the canaries below are quiet on a real web-server scan (or on a literal extract that still fails on current `main` / 5.0.0 the same way).** Pytest on toys is necessary but not sufficient.

---

## Hard acceptance (all required)

### A. Consumer canary scan

Clone or use existing `awresports/web-server` on a clean `dev` (or the tree the human names). Run:

```bash
# From web-server; pin may be 5.0.0 — override by installing YOUR branch into the image:
docker run --rm --entrypoint sh \
  -v "$PWD":/usr/src/app:z,cached \
  -v /path/to/your/skylos/checkout:/skylos-src:ro \
  -w /usr/src/app \
  ghcr.io/duriantaco/skylos:5.0.0-python3.11 \
  -c 'cp -a /skylos-src /tmp/skylos && pip install -q /tmp/skylos && \
      skylos . -c 80 --no-grep-verify --force \
        --exclude .agents --exclude .claude --exclude workers/_dont_import \
        --format json-ci -o /tmp/out.json && skylos --version'
```

Compare soft-keys `(file, name)` against the same scan on **released `5.0.0`** (do not only compare to `main` — `main` already adds noise).

**Pass only if every Must-quiet canary is absent** from `unused_functions` / `unused_classes` / `unused_imports` in `/tmp/out.json`.

### B. No-regression canaries

These must stay **absent** if they were absent on `main` before your change, and must not become newly present vs 5.0.0 for signal handlers:

| Symbol | File (web-server) | Rule |
|--------|-------------------|------|
| `JSONFormatter` | `pa_logging/json_formatter.py` | Must not re-appear if you touch Celery/registry liveness |
| `ExtraAdder` | `pa_logging/extra.py` | same |
| `CeleryTaskAdder` | `pa_logging/celery_task_adder.py` | same |
| `CustomRedisCluster` | `redishelper/custom_cluster.py` | same |
| `assign_project_onboarding_form` | `api/hub/signals.py` | Must be quiet (was quiet on 5.0.0; `main`/#1072 regress) |
| `on_recruit_post_saved` | `team/models/recruiting.py` | same family (`@receiver`) |

[#1072](https://github.com/duriantaco/skylos/pull/1072) **failed this**: it quieted `RedisClusterBackend` but re-flagged the LOGGING classes.

### C. Fixtures must be literal extracts

Do **not** rewrite the pattern into a flatter shape that your heuristic already handles.  
If production uses nested registries + factory-generated view methods, the fixture must too.  
A fixture that passes while the canary on web-server still flags is **invalid** — delete or harden it until both agree.

### D. PR description must include numbers

```
web-server -c 80 --no-grep-verify:
  5.0.0:  functions=… classes=… imports=…  f+c+i=…
  this PR: functions=… classes=… imports=…  f+c+i=…
Canaries: list each Must-quiet with ok/FLAG on 5.0.0 and on this PR.
```

If `f+c+i` does not drop (or canaries stay FLAG), **do not claim** “large-app gaps closed.”

---

## Must-quiet canaries (web-server)

Status when last measured (cleanup tree): **5.0.0** vs **`main`** vs **#1072 `fea4b41`**.

### Tier 1 — claimed fixed before, still FLAG on #1072 (fix these for real)

| Symbol | File | Notes |
|--------|------|--------|
| `_validate_phone` | `api/checkout/views.py` | Skylos lists `called_by` four serializers in the **same file** but `references: 0` and still reports. Fix the **reference/call graph**, not a one-off entrypoint heuristic that only matches the toy layout. |
| `_get_api_key_from_request` | `api/permissions.py` | Same class of same-module false dead. |
| `get_game_form_schema` | `api/lovable/form_schemas.py` | Registry + `getattr` — see Lovable shape below |
| `create_game` | `api/lovable/mutations.py` | same |
| `update_game` | `api/lovable/mutations.py` | same |
| `delete_game_safely` | `api/lovable/mutations.py` | same |
| `create_practice` | `api/lovable/mutations.py` | same |
| `get_user_teams` | `api/lovable/queries.py` | same |
| `get_team_roster` | `api/lovable/queries.py` | same |
| `get_team_schedule` | `api/lovable/queries.py` | same |
| `get_team_practices` | `api/lovable/queries.py` | same |
| `IntegrateSessions` | `modernstat/msgame/processors/integrate_sessions.py` | importlib/getattr plugin |
| `FacilityChoiceField` | `modernstat/msfacility/fields.py` | form field class still unused |
| `NoDbTestRunner` | `pitchaware/nodb_test_runner.py` | `TEST_RUNNER` often only in secondary/commented settings |
| `CVTrackingRegionAPITests` | `cv_tagging/tests.py` | unittest/Django discovery still failing on this app |
| `DetectEvalSessionTests` | `cv_tagging/tests.py` | same |
| `LeagueHomeTestCase` | `league/tests.py` | same |
| `schedule_dates` (on NcaaClient) | `college_data/provider.py` | duck-typed provider methods |
| `initialize_field_hardware` (on NotApplicableNetworkHardwareProvider) | `tickets/network_hardware/providers.py` | provider interface |

### Tier 1b — quiet on #1072 only (keep quiet; add regression test)

| Symbol | File |
|--------|------|
| `RedisClusterBackend` | `redishelper/celery_result_backend.py` |

Wire: `result_backend="redishelper.celery_result_backend:RedisClusterBackend"` in `pitchaware/celery.py` (`app.conf.update` / Celery constructor). Colon and dotted forms.

### Tier 2 — volume buckets (do not claim done until these move)

Approximate keep leftovers that still dominate totals (not all must hit zero in one PR, but a “large-app” PR should move at least one bucket by **tens**, with canaries as proof):

| Bucket | ~still present | What “fixed” means |
|--------|---------------:|--------------------|
| `test-module` | 93 | TestCase classes + imports/helpers only used from tests |
| `skylos-false-positive-in-file-uses` | ~94 | Same-module callers; `_validate_phone` is the canary |
| `class-method-skylos-gap-or-interface` | ~91 | Provider/client methods |
| `management-command` | 62 | Helpers only called from `Command.handle` in same module (`Command` class itself already quiet on 5.0) |
| `model-method-template-risk` | ~37 | Model methods only referenced from templates |

---

## Production shapes to copy (do not flatten)

### 1. Lovable registry + factory `getattr` (why #1072’s fixture was invalid)

**Registry** ([`api/lovable/registry.py`](api/lovable/registry.py)) — nested under resource keys:

```python
"games": {
    "queryset_method": "get_team_schedule",
    "create_method": "create_game",
    "update_method": "update_game",
    "options_method": "get_game_form_schema",
    ...
}
```

**Factory** ([`api/lovable/factory.py`](api/lovable/factory.py)) — names stored on the generated class, `getattr` inside nested methods:

```python
class_dict = {
    "_queryset_method_name": queryset_method_name,
    ...
}

def get_queryset(self):
    if hasattr(self, "_queryset_method_name") and self._queryset_method_name:
        if hasattr(queries, self._queryset_method_name):
            query_func = getattr(queries, self._queryset_method_name)
            return query_func(self.request)

# similarly:
mutation_func = getattr(mutations, custom_create_method)
schema_func = getattr(form_schemas, options_method_name)
```

A flat `HANDLERS[kind].get("create_method")` in the same file as `dispatch()` is **not** equivalent. Extract or mirror this factory pattern until `create_game` / `get_game_form_schema` go quiet on web-server.

### 2. Same-module helper with `called_by` but `references: 0`

[`api/checkout/views.py`](api/checkout/views.py) — `_validate_phone` is called from nested `Serializer.validate_phone` methods in the same module. Evidence on 5.0.0/#1072 still shows `called_by: [...]` and `references: 0` / `no_refs`.  

**Fix the analyzer’s reference counting for same-module / nested-class calls.** Do not only mark the helper live because a view is routed.

### 3. Celery `result_backend` string

Already partially handled in #1072 — keep `RedisClusterBackend` quiet and ensure LOGGING `"()"` factories stay quiet (regression).

### 4. Django `@receiver`

[`api/hub/signals.py`](api/hub/signals.py):

```python
@receiver(post_save, sender=HubProjectRecord, dispatch_uid="...")
def assign_project_onboarding_form(sender, instance, created, **kwargs):
    ...
```

Must be live. Currently a **regression vs 5.0.0** on `main` / #1072.

### 5. TestCase discovery

Classes like `CVTrackingRegionAPITests` in `cv_tagging/tests.py` still FLAG after #1059’s `unittest_liveness`. Copy **this app’s** test module layout (Django `TestCase` in `app/tests.py`), do not only use stdlib `unittest` in a tiny file.

### 6. Management command helpers

Private functions in `*/management/commands/*.py` called only from `Command.handle` — still FLAG. `Command` class is already fine on 5.0.0.

---

## Suggested work order

1. **Regressions first:** `@receiver` quiet again vs 5.0.0; LOGGING classes stay quiet when Celery backend liveness changes.
2. **Reference graph:** `_validate_phone` / `_get_api_key_from_request` — prove with web-server canary.
3. **Lovable-faithful registry:** all nine mutation/query/schema canaries quiet on web-server.
4. **TestCase + command helpers + provider methods** — bucket movement with named canaries.
5. Re-run full web-server scan; put numbers in the PR body.

---

## Forbidden claims

- “Fixed large-app FPs” when only `tmp_path` pytest is green.
- “Closes #1056 leftovers” when Tier-1 canaries still FLAG on web-server.
- Net `f+c+i` increase vs 5.0.0 without calling out regressions and listing which canaries flipped to FLAG.

---

## Out of scope

- Editing `awresports/web-server` product code or adding `# skylos: ignore` to silence canaries.
- Making the entire web-server `--gate` green in one PR (hundreds of remaining findings).
- Re-opening migrations / middleware / `STORAGES` already quiet on 5.0.0 — unless your PR regresses them.

---

## Provenance

- Consumer scans: `.tmp_unused_routes/skylos_5.0.0_cleanup.json`, `skylos_main.json`, `skylos_pr1072.json`
- Related upstream: [#1056](https://github.com/duriantaco/skylos/issues/1056), [#1059](https://github.com/duriantaco/skylos/pull/1059), [#1068](https://github.com/duriantaco/skylos/pull/1068), [#1072](https://github.com/duriantaco/skylos/pull/1072)
- Repro corpus (optional base, must be hardened to match shapes above): https://github.com/daveisfera/skylos-repro
