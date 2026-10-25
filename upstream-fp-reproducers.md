# Skylos upstream: false-positive reproducers (from a large Django app)

Hand this file to an agent working in **https://github.com/duriantaco/skylos** (and optionally https://github.com/daveisfera/skylos-repro). Goal: add **minimal, literal reproducers** + liveness fixes so these stop reporting at `-c 80`, the same way [#1056](https://github.com/duriantaco/skylos/issues/1056) / [#1068](https://github.com/duriantaco/skylos/pull/1068) did for the first Django batch.

Do **not** need the full web-server tree. Each case below is a pattern; clone the idea into a tiny fixture under `skylos-repro/` (or `test/` fixtures in skylos) and assert `skylos <fixture> -c 80` is clean except any intentional true positive.

## Already covered — do not re-open

These were the [#1056](https://github.com/duriantaco/skylos/issues/1056) eleven and are addressed (or claimed) by **5.0.0** and/or **PR #1068**. Repro suite already exists in `skylos-repro` / `test/test_django_app_repro_liveness.py`.

| Pattern | Status on web-server @ PR #1068 head `00cc96d` |
|---------|-----------------------------------------------|
| Django migrations | Quiet on 5.0.0 |
| `MIDDLEWARE` / `STORAGES` dotted paths | Quiet on 5.0.0 (`RouteMiddleware`, `MediaStorage`, …) |
| `AUTHENTICATION_BACKENDS` classes | Quiet on 5.0.0 for Django auth backends |
| `LOGGING` `"()"` factories | Quiet only with #1068 (`JSONFormatter`, `ExtraAdder`, `CeleryTaskAdder`) |
| Management `Command` **classes** | Quiet on 5.0.0 |
| `{% static %}` JS exports / `register_converter` wrappers | Covered by #1068 repros (not the main leftover noise here) |

**Scan evidence (same tree, `-c 80 --no-grep-verify`):**

| Skylos | functions | classes | imports | variables |
|--------|----------:|--------:|--------:|----------:|
| 4.35.0 | 448 | 194 | 97 | 168 |
| 5.0.0 | 427 | 29 | 96 | 102 |
| PR #1068 @ `00cc96d` | 436 | 25 | 93 | 210 |

Almost all of the big drop is **5.0.0**. #1068 is nearly net-flat on functions+classes+imports and **adds** signal-handler FPs + many variables. Fix the gaps below; also treat the signal regression as a must-fix.

---

## How to work

1. For each **Priority** case, add a self-contained fixture (one small package or file tree).
2. Run: `skylos <fixture> -c 80 --format concise` (and a pytest that embeds the same expectation).
3. Expected: **zero** unused hits for the live symbols named in the case; optional intentional dead helper OK (see `UnusedHelperTests` style in #1068).
4. Prefer evidence-based liveness (settings/Celery string paths, `@receiver`, unittest discovery, `getattr(module, name)` from a registry dict) over broad ignore lists.
5. Keep fixes precise — do not mark every private function in `management/commands/` live.

---

## Priority 1 — regressions / gaps introduced or left by #1068

### P1.1 Django `@receiver` signal handlers reported unused

**Symptom on web-server after #1068 (new vs 5.0.0):** these appear as unused functions only on the PR build:

- `api/hub/signals.py` — `assign_project_onboarding_form`
- `scoreboard_runtime/signals.py` — `_sync_layout_flags`, `sync_segment_report_flags_on_layout_save`, `sync_segment_report_flags_on_layout_delete`
- Similar: `playlists/models/playlist.py` / `team/models/recruiting.py` receivers and `bullpen/models.py` `_on_model_signal`

**Minimal shape:**

```python
# myapp/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from myapp.models import Item

@receiver(post_save, sender=Item, dispatch_uid="myapp.item_created")
def on_item_created(sender, instance, created, **kwargs):
    if created:
        instance.touch()
```

Wire `myapp` into `INSTALLED_APPS` and import `myapp.signals` from `AppConfig.ready()` (or rely on Django’s usual signals import). **Nothing else should call `on_item_created`.**

**Accept:** `on_item_created` not reported at `-c 80`.  
**Also cover:** receivers defined on the model module; `post_delete`; helpers only called from the receiver body should not drag the receiver into “unused.”

### P1.2 Celery `result_backend="pkg.mod:ClassName"` (colon path, not Django auth)

**Still flagged:** `redishelper/celery_result_backend.py` — `RedisClusterBackend`

**Wire (real):**

```python
# celery app conf
result_backend="redishelper.celery_result_backend:RedisClusterBackend"
```

This is **not** `AUTHENTICATION_BACKENDS`. Skylos must treat Celery’s `module:Class` / `module.Class` result-backend strings as live class entrypoints (same family as `#1056` auth backends, different config key).

**Minimal shape:** package `redishelper/celery_result_backend.py` with `class RedisClusterBackend`, and a `celery_app.py` that only references it via the string above. No Python import of the class.

**Accept:** class not reported unused.

### P1.3 `TEST_RUNNER` only in a non-default / commented settings module

**Still flagged:** `pitchaware/nodb_test_runner.py` — `NoDbTestRunner`

**Real pattern:** class exists; primary settings may comment it out while another settings module (or docs/CI) still names it:

```python
# settings.py
# TEST_RUNNER = "pitchaware.nodb_test_runner.NoDbTestRunner"

# settings_ci.py  (or env-selected module)
TEST_RUNNER = "pitchaware.nodb_test_runner.NoDbTestRunner"
```

**Accept:** if **any** scanned settings module assigns `TEST_RUNNER` to the dotted path, the class is live. Optional: subclasses of `DiscoverRunner` that override `setup_databases` are convention entrypoints when named from settings.

---

## Priority 2 — #1056 cases that still fail on a large Django app

### P2.1 Test-module discovery (classes + imports inside tests)

**Still loud:** keep-bucket `test-module` **93/93** still present under PR #1068.

Examples still reported:

- Classes: `cv_tagging/tests.py` — `CVTrackingRegionAPITests`, `DetectEvalSessionTests`, …
- Helpers: `cv_tagging/tests.py` — `_healthy`; `league/tests.py` — `_playbook_roster_row`
- Imports used only inside test modules: e.g. `league/tests.py` imports (`json`, `ContentFile`, …) still show as unused imports in our triage

**Minimal shape:**

```python
# app/tests.py  (or tests/test_foo.py discovered by unittest/pytest)
from django.test import TestCase

class DemoAPITests(TestCase):
    def test_ok(self):
        self.assertTrue(_helper())

def _helper():
    return True
```

No import of `DemoAPITests` from production code.

**Accept:** test class, test methods, and private helpers **only referenced from that test module** are live; imports used only by those tests are not unused.

### P2.2 Management-command **module helpers** (not the `Command` class)

**Command classes** are already quiet on 5.0.0. **61** keep items remain: private helpers inside `management/commands/*.py` that are only called from `Command.handle` / other helpers in the same file.

Example: `cv_tagging/management/commands/auto_label_detect_eval.py` — `_charted_pitches`, `_climb`, `_rehome_take`, …

**Minimal shape:**

```python
# myapp/management/commands/hello.py
from django.core.management.base import BaseCommand

def _format_name(name):
    return name.strip().title()

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(_format_name(options["name"]))
```

**Accept:** `_format_name` not unused when only called from `Command` in the same command module.  
**Do not** mark arbitrary private functions live just because the file lives under `management/commands/` if nothing in that command module calls them (true dead helpers should still flag).

### P2.3 Provider / duck-typed client methods

**Still flagged:** `college_data/provider.py` — `NcaaClient.schedule_dates`, `.scoreboard`, `.division_teams`, … and `tickets/network_hardware/providers.py` — `NotApplicableNetworkHardwareProvider.initialize_field_hardware`.

**Pattern:** call sites invoke methods on a **base type** or via dynamic dispatch; concrete subclass methods are the real implementations and never named at the call site.

Repro already sketched in skylos-repro `16_provider_interface/` — **extend** until a multi-method client like `NcaaClient` (several public methods, shared private `_graphql`) stays clean when only `BaseProviderClient` / a registry type appears in call sites.

**Accept:** public methods that override or implement the provider contract are live; unused private helpers with no callers may still flag.

### P2.4 `importlib` + `getattr` processor / registry plugins

**Still flagged:**

- `modernstat/msgame/processors/integrate_sessions.py` — `IntegrateSessions` (class loaded by name)
- `video_watcher/processors/hls_clip_url.py` — `combine_url_and_args_for_hls_clip` (string-selected callable)
- Lovable RPC: `api/lovable/factory.py` does `getattr(mutations, name)`, `getattr(queries, name)`, `getattr(form_schemas, name)` where `name` comes from a registry dict (`api/lovable/registry.py` — e.g. `"options_method": "get_game_form_schema"`). Still flagged: `get_game_form_schema`, `create_game`, `delete_game_safely`, …

**Minimal shape (registry + getattr):**

```python
# registry.py
HANDLERS = {"create": "create_item", "schema": "get_item_schema"}

# handlers.py
def create_item(request): ...
def get_item_schema(request): ...

# factory.py
from . import handlers, registry
def dispatch(kind, request):
    return getattr(handlers, registry.HANDLERS[kind])(request)
```

No direct Python reference to `create_item` / `get_item_schema` except via `getattr` + string table.

**Accept:** those functions/classes are live. Cover both `getattr(module, literal_or_const)` and `importlib.import_module` + `getattr`.

### P2.5 Custom Django form fields / `clean` on Form subclasses

**Still flagged:** `modernstat/msfacility/fields.py` — `FacilityChoiceField`  
#1068 quieted some `.clean` methods (`JoinFacility.clean`, `PitcherProspectFeedForm.clean`) but the **field class** can still show unused.

**Minimal shape:** field class used only as a form attribute (`facility = FacilityChoiceField(...)`) with overrides (`clean`, `validate`). Same family as skylos-repro `20_django_form_field/`.

**Accept:** field class + overridden methods live when attached to a Form that is itself live (view/admin/API).

### P2.6 Model methods used only from Django templates

**Still loud:** keep-bucket `model-method-template-risk` **37** remaining (e.g. `HubProjectRecord.get_current_status_display`, `next_steps_message`).

Extend skylos-repro `15_model_template_method/` with:

- `{{ obj.get_foo }}` / `{{ obj.get_foo }}` callable form
- methods that are not `get_*` display helpers (`next_steps_message`)
- auto-display helpers like `get_FOO_display` if still flagged when FOO is a real field

**Accept:** method not unused when a template in the scanned tree references it.

---

## Priority 3 — high-volume analyzer gaps (harder, still valuable)

### P3.1 Same-file / same-module use still reported (`skylos-false-positive-in-file-uses`)

**~95** keep items still on PR #1068 — symbols with in-module callers that Skylos still marks unused (often `references: 0` while `called_by` lists same-module users).

Canary from this app: `api/checkout/views.py` — `_validate_phone` (called from several serializer `validate_phone` methods in the same file; still reported).

**Minimal shape:** private helper defined at module top, called from methods later in the same module (including nested classes). No cross-module imports.

**Accept:** not reported unused. Prefer fixing reference graph / call resolution over framework heuristics.

### P3.2 LAPI / string command dispatch

**Example:** `lapi/commands.py` — `reboot` selected by command name string from camera/LAPI messages.

**Minimal shape:** dict or if/elif mapping `{"reboot": reboot_fn}` or `getattr(commands, cmd_name)` where `cmd_name` arrives as data.

### P3.3 Cross-repo / string product contracts

Lower priority for generic Skylos; document only if easy:

- `rtmp/report_key.py` — `get_report_key` shared with rtmp-server by convention
- Partner payload builders only referenced from settings-selected integrations

Skip these if they need product-specific allowlists; focus on framework-general evidence.

---

## Suggested skylos-repro layout

Mirror existing numbered fixtures:

| ID | Directory / file | Maps to |
|----|------------------|---------|
| 21 | `21_django_receiver_signals/` | P1.1 |
| 22 | `22_celery_result_backend_string/` | P1.2 |
| 23 | `23_test_runner_secondary_settings/` | P1.3 |
| 24 | `24_management_command_helpers/` | P2.2 |
| 25 | `25_registry_getattr_handlers/` | P2.4 (Lovable-style) |
| 26 | `26_same_module_private_helper/` | P3.1 |

Extend existing `14_test_module`, `15_model_template_method`, `16_provider_interface`, `19_processor_plugin`, `20_django_form_field` rather than duplicating when the gap is “fixture too small.”

---

## Acceptance checklist for the Skylos PR

- [ ] New/extended fixtures fail on **5.0.0** (or current `main` without the fix) and pass with the fix at `-c 80`
- [ ] Pytest coverage next to #1068’s `test_django_app_repro_liveness.py` style
- [ ] P1.1: no new unused hits on `@receiver` handlers vs 5.0.0 baseline on those fixtures
- [ ] P1.2: `result_backend="pkg.mod:Class"` quiets the class
- [ ] P2.1–P2.2: test discovery + command helpers covered without blanket-ignoring all privates
- [ ] Concise note in the PR: which #1056 bullets were incomplete on large apps

## Out of scope for that PR

- Making the consumer app `--gate` green (hundreds of real or ambiguous findings remain)
- Mass `# skylos: ignore` in the consumer
- Re-litigating migrations / middleware / STORAGES / LOGGING already fixed in 5.0.0 / #1068

## Provenance

- Consumer: large Django monolith (internal)
- Compare artifacts: `.tmp_unused_routes/skylos_baseline.json` (4.35.0), `skylos_5.0.0.json`, `skylos_pr1068.json`, `skylos_pr1068_compare.txt`
- Upstream issue/PR: [#1056](https://github.com/duriantaco/skylos/issues/1056), [#1068](https://github.com/duriantaco/skylos/pull/1068)
- Skylos-repro: https://github.com/daveisfera/skylos-repro
