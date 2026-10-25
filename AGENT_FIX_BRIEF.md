# Skylos dead-code false positives — fix brief (literal extracts)

Hand this to an agent with the **skylos** source. Goal: stop reporting the soft-keys below at `-c 80` using evidence-based liveness (not broad ignores).

| Item | Detail |
|------|--------|
| Upstream | [#1056](https://github.com/duriantaco/skylos/issues/1056), [#1068](https://github.com/duriantaco/skylos/pull/1068), [#1072](https://github.com/duriantaco/skylos/pull/1072) |
| Repros | https://github.com/daveisfera/skylos-repro |
| Consumer evidence | [`upstream-fp-reproducers.md`](upstream-fp-reproducers.md) |
| Verify | `skylos <skylos-repro> -c 80 --format concise --no-grep-verify` |

**Validity:** a fixture that goes quiet while the consumer canary still FLAGs is **invalid**. Do not claim fixed.

> Avoid `ClassName.method` spellings in this repo's markdown — skylos treats those as `documented_public_api` and can quiet provider canaries.

---

## Tier-1 red on 5.0.0 (literal extracts)

### 1. Lovable factory `getattr` + `type(...)`

**Repro:** `lovable_registry/` (twin: `25_lovable_registry_factory/`)

- `registry.py` — nested config with string method names
- `factory.py` — builds `class_dict`, nested methods do `getattr(mutations|queries|form_schemas, name)`, ends with `type(name, bases, class_dict)`
- `mutations.py` / `queries.py` / `form_schemas.py` — canary handlers
- `urls.py` — registers generated viewsets

**Soft-keys:** `create_game`, `update_game`, `delete_game_safely`, `create_practice`, `get_game_form_schema`, `get_team_schedule`, `get_team_roster`, `get_user_teams`

**Accept:** those handlers are live (factory getattr targets), not unused.

---

### 2. Checkout nested serializer helper

**Repro:** `checkout_phone/` (twin: `26_checkout_phone_serializers/`)

Module-level `_validate_phone` only called from nested `Serializer.validate_phone` methods. No module-level `run_checks()` toy entry.

**Soft-key:** `_validate_phone` (often `called_by` set, `references: 0`)

**Accept:** helper live via serializer validators on a routed view module.

---

### 3. Celery `result_backend="pkg.mod:ClassName"`

**Repro:** `celery_result_backend/`

**Soft-key:** `RedisClusterBackend` (FLAGS on 5.0.0; must stay quiet on #1072)

**Accept:** class live from colon/dotted Celery backend strings.

---

### 4. Multi-method duck-typed client

**Repro:** `provider_iface/`

Concrete client implements many public methods; `pipeline.py` uses the factory client without naming those methods on the concrete type.

**Soft-keys:** `schedule_dates`, `division_teams`, `game_detail`, `box_score`, `play_by_play`

**Accept:** public contract methods live when the client type is used; private `_graphql` with in-class callers stays live.

---

### 5. Custom form field class (string type map only)

**Repro:** `django_form_field/`

**Soft-key:** `FacilityChoiceField` (class)

**Accept:** class live when named in a string type registry / real form usage (even if assignment is dynamic or historically commented).

---

### 6. `TEST_RUNNER` comment-only primary settings

**Repro:** `test_runner_settings/`

Primary settings only comment-names `NoDbTestRunner`. Secondary settings assign a **different** runner.

**Soft-key:** `NoDbTestRunner` (should FLAG until comment/secondary string entrypoints are modeled correctly — or quiet only when a live assignment exists)

---

### 7. Management command helpers below `handle`

**Repro:** `mgmt_command_helpers/` (twin: `24_management_command_helpers/`)

Private helpers defined **after** `Command.handle`, called only from `handle`.

**Accept:** helpers live with the command; intentional `_dead_helper` may still flag.

---

### 8. Django `TestCase` app `tests.py`

**Repro:** `test_module/tests.py`

Denser TestCase layout; imports/helpers used only in tests.

**Intentional TP:** `UnusedHelperTests` (keep reporting)

---

### 9. Other still-red / precision

| Fixture | Soft-keys |
|---------|-----------|
| `04_django_url_converter.py` | `register_converter` |
| `template_static_js/` | `greet` |
| `logging_infra/` | `JSONFormatter`, `ExtraAdder` (5.0.0; quiet on #1068+) |
| `receiver_signals/` | `@receiver` handlers — FLAG iff consumer signal canaries FLAG on the build under test |

---

## Workflow

1. Confirm red soft-keys with `skylos-repro` at `-c 80`.
2. Confirm the same soft-keys FLAG on a local consumer checkout.
3. Smallest evidence-based skylos fix; re-run both trees.
4. Never claim fixed when the consumer canary still FLAGs.
