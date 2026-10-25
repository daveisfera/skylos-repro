# Skylos unused findings on `dev` — review

Source: `local/skylos.sh . -c 80` baseline JSON on clean `origin/dev` (`.tmp_unused_routes/skylos_baseline.json`).

The large unused-route cleanup WIP was stashed as `unused-route-cleanup-and-skylos-cascade-wip`.

## Removed as legitimate dead code

Deleted **36** symbols (25 functions + 14 unused imports) that had no in-file uses beyond the definition, no other `.py` references, and were not settings-/middleware-/test-/Django-convention entry points.

### Functions

- `api/hub/sales_api.py:96` — `_feature_option`
- `college_data/pipeline.py:2306` — `_awre_team_is_established`
- `cv_tagging/detect_eval/cells.py:315` — `assemble_cells`
- `cv_tagging/detect_eval/lighting.py:54` — `color_balance`
- `cv_tagging/detect_eval/motion.py:59` — `count_bursts`
- `cv_tagging/detect_eval/pipeline.py:672` — `calibrated_trackman`
- `cv_tagging/detect_eval/trackman.py:35` — `offsets_by_camera`
- `game/utils/gamechanger.py:32` — `load_raw_game_stream_events`
- `hs_enrichment/utils.py:17` — `fetch_association_schools`
- `hs_enrichment/utils.py:54` — `detect_programs`
- `hs_enrichment/utils.py:87` — `extract_contacts_from_html`
- `hs_enrichment/utils.py:137` — `infer_email`
- `kvs/game_discontinuity_analysis.py:309` — `analyze_fields_from_mapping`
- `kvs/game_discontinuity_analysis.py:498` — `clear_analysis_progress`
- `kvs/game_discontinuity_analysis.py:525` — `get_analysis_status`
- `kvs/mlb_promote.py:198` — `_mlb_gcs_copy_jobs`
- `maddux/utils/helpers.py:81` — `fetch_report`
- `maddux/utils/helpers.py:202` — `upload_csv_to_openai`
- `modernstat/msgame/utils/game_timestamps.py:37` — `roll_practice_end_by_half_day`
- `scoreboard_runtime/reader_scorebug.py:152` — `clear_pending_results`
- `scoreboard_runtime/utils.py:162` — `attach_runtime_session_to_game`
- `scoreboard_runtime/utils.py:195` — `attach_runtime_session_to_training_event`
- `stats/rml_pdf.py:130` — `merge_pdf_files_sectioned`
- `tickets/unifi_api.py:79` — `_extract_mac_candidates`
- `tickets/unifi_api.py:272` — `check_unifi_device_status`

### Imports

- `api/events_v1/payloads.py` — `enable_cameras`
- `api/hub/serializers.py` — `Sum`
- `communications/api/v1/serializers.py` — `signing`
- `hs_enrichment/pipeline/ohsaa.py` — `BeautifulSoup`
- `hs_enrichment/pipeline/ohsaa.py` — `urljoin`
- `modernstat/accounting/views/management.py` — `IntegrityError`
- `modernstat/msgame/views/charting_watch.py` — `AUTH_TOKEN_PREFIX`
- `playlists/serializers.py` — `reverse`
- `stats/tasks.py` — `team_keys`
- `stats/tasks.py` — `team_keys`
- `stats/tasks.py` — `team_keys`
- `tickets/network_hardware/tplink_omada.py` — `extract_mac_candidates`
- `tickets/tasks.py` — `TicketEmailDeliveryConfigurationError`
- `tickets/tasks.py` — `TicketEmailDeliveryError`

## Incorrect / leave alone (Skylos false positives or unsafe to delete)

Skylos reported **700** additional unused functions/classes/imports that should **not** be deleted without a deeper product/framework review. Grouped by why:

### django-migration (153)

Django migration `Migration` classes — loaded by name.

- `api/migrations/0001_schema_20260916.py:12` — `class` `Migration`
- `api/migrations/0002_schema_20260916.py:9` — `class` `Migration`
- `api/migrations/0003_register_periodic_tasks.py:55` — `class` `Migration`
- `api/migrations/0004_seed_hub_form_templates.py:146` — `class` `Migration`
- `api/migrations/0005_checkout_delivery.py:36` — `class` `Migration`
- `api/migrations/0006_checkout_workflow.py:10` — `class` `Migration`
- `api/migrations/0007_checkout_workflow_backfill.py:28` — `class` `Migration`
- `api/migrations/0008_auto_20260925_1406.py:33` — `class` `Migration`
- `api/migrations/0009_crm_sales_backfill.py:208` — `class` `Migration`
- `api/migrations/0010_auto_20260929_1136.py:9` — `class` `Migration`
- `api/migrations/0011_air2_catalog_pricing.py:23` — `class` `Migration`
- `api/migrations/0012_enable_sales_crm_v2_reads.py:20` — `class` `Migration`
- `api/migrations/0013_approved_sales_stage.py:35` — `class` `Migration`
- `api/migrations/0014_checkout_programs.py:37` — `class` `Migration`
- `api/migrations/0015_document_organization_program.py:32` — `class` `Migration`
- `api/migrations/0016_program_workspace.py:8` — `class` `Migration`
- `api/migrations/0017_resume_unconfigured_invoices.py:19` — `class` `Migration`
- `bullpen/migrations/0001_schema_20260916.py:10` — `class` `Migration`
- `bullpen/migrations/0002_schema_20260916.py:8` — `class` `Migration`
- `bullpen/migrations/0003_schema_20260916.py:7` — `class` `Migration`
- `college_data/migrations/0001_initial.py:8` — `class` `Migration`
- `college_data/migrations/0002_ncaa_provider.py:17` — `class` `Migration`
- `college_data/migrations/0003_auto_20261007_1407.py:6` — `class` `Migration`
- `college_data/migrations/0004_alter_collegeimportrun_scope.py:6` — `class` `Migration`
- `college_data/migrations/0005_remove_collegegame_division.py:6` — `class` `Migration`
- `college_data/migrations/0006_collegeteam_catalog_program.py:7` — `class` `Migration`
- `college_data/migrations/0007_alter_collegeimportrun_scope.py:6` — `class` `Migration`
- `college_data/migrations/0008_alter_collegeimportrun_scope.py:6` — `class` `Migration`
- `college_data/migrations/0009_college_association_providers.py:29` — `class` `Migration`
- `communications/migrations/0001_schema_20260916.py:10` — `class` `Migration`
- `communications/migrations/0002_schema_20260916.py:8` — `class` `Migration`
- `communications/migrations/0003_register_periodic_tasks.py:83` — `class` `Migration`
- `communications/migrations/0004_gate_installation_on_quote_acceptance.py:38` — `class` `Migration`
- `communications/migrations/0005_seed_installation_process_campaign.py:233` — `class` `Migration`
- `communications/migrations/0006_auto_20260925_1406.py:8` — `class` `Migration`
- `communications/migrations/0007_installation_email_copy.py:50` — `class` `Migration`
- `cv_tagging/migrations/0001_schema_20260916.py:7` — `class` `Migration`
- `cv_tagging/migrations/0002_schema_20260916.py:8` — `class` `Migration`
- `cv_tagging/migrations/0003_seed_event_types.py:272` — `class` `Migration`
- `event_center/migrations/0001_schema_20260916.py:9` — `class` `Migration`
- … and 113 more (see `.tmp_unused_routes/baseline_classify_keep.json`)

### class-method-skylos-gap-or-interface (107)

Methods on classes (including client/provider interfaces) — often called dynamically or via subclass.

- `college_data/provider.py:174` — `function` `schedule_dates` (on NcaaClient)
- `college_data/provider.py:192` — `function` `scoreboard` (on NcaaClient)
- `college_data/provider.py:208` — `function` `division_teams` (on NcaaClient)
- `college_data/provider.py:283` — `function` `game_detail` (on NcaaClient)
- `college_data/provider.py:294` — `function` `box_score` (on NcaaClient)
- `college_data/provider.py:302` — `function` `play_by_play` (on NcaaClient)
- `college_data/provider.py:350` — `function` `schedule_dates` (on NjcaaClient)
- `college_data/provider.py:383` — `function` `scoreboard` (on NjcaaClient)
- `college_data/provider.py:396` — `function` `division_teams` (on NjcaaClient)
- `college_data/provider.py:444` — `function` `game_detail` (on NjcaaClient)
- `college_data/provider.py:478` — `function` `box_score` (on NjcaaClient)
- `college_data/provider.py:482` — `function` `play_by_play` (on NjcaaClient)
- `college_data/provider.py:804` — `function` `schedule_dates` (on NaiaClient)
- `college_data/provider.py:810` — `function` `scoreboard` (on NaiaClient)
- `college_data/provider.py:819` — `function` `division_teams` (on NaiaClient)
- `college_data/provider.py:836` — `function` `game_detail` (on NaiaClient)
- `college_data/provider.py:839` — `function` `box_score` (on NaiaClient)
- `college_data/provider.py:842` — `function` `play_by_play` (on NaiaClient)
- `communications/services/gmail_inbound.py:96` — `function` `GmailThreadSyncSummary.to_dict`
- `facility/forms.py:93` — `function` `JoinFacility.clean`
- `game/engine/training_mode.py:220` — `function` `TrainingModeKeeper.reset_situation`
- `game/engine/training_mode.py:244` — `function` `TrainingModeKeeper.adjust_lineup_opponent`
- `game/engine/training_mode.py:285` — `function` `TrainingModeKeeper.change_pitcher_team`
- `game/engine/training_mode.py:330` — `function` `TrainingModeKeeper.pitcher_handedness`
- `game/engine/training_mode.py:360` — `function` `TrainingModeKeeper.change_atbat_hitter`
- `game/serializers/partners.py:425` — `function` `PitchDataShareSerializer.get_timestamp`
- `game/serializers/partners.py:431` — `function` `PitchDataShareSerializer.get_session_type`
- `game/serializers/partners.py:434` — `function` `PitchDataShareSerializer.get_tracking_type`
- `game/serializers/partners.py:437` — `function` `PitchDataShareSerializer.get_session_id`
- `game/serializers/partners.py:440` — `function` `PitchDataShareSerializer.get_pitcher_external_id`
- `game/serializers/partners.py:448` — `function` `PitchDataShareSerializer.get_hitter_external_id`
- `game/utils/base.py:265` — `function` `CSVImporter.initialize_training_sessions_for_training`
- `game/utils/base.py:988` — `function` `CSVImporter.master_pitch_type_classifier`
- `game/utils/base.py:1027` — `function` `CSVImporter.generate_sha`
- `game/utils/base.py:1033` — `function` `CSVImporter.what_am_i`
- `game/utils/base.py:1068` — `function` `CSVImporter.get_importer`
- `game/utils/dartfish.py:44` — `function` `DartFishImporter.get_pitcher`
- `game/utils/dartfish.py:73` — `function` `DartFishImporter.get_hitter`
- `game/utils/gamechanger.py:173` — `function` `GameChangerClient.get_raw_game_stream_events_for_event`
- `game/utils/gc_state.py:280` — `function` `_Replayer._positions_for`
- … and 67 more (see `.tmp_unused_routes/baseline_classify_keep.json`)

### test-module (93)

Test modules / TestCase classes.

- `cv_tagging/tests.py:7` — `import` `ValidationError`
- `cv_tagging/tests.py:9` — `import` `SimpleTestCase`
- `cv_tagging/tests.py:24` — `import` `CVScoreboardState`
- `cv_tagging/tests.py:25` — `import` `CVTaggingEvent`
- `cv_tagging/tests.py:32` — `import` `FIELD_READY_COMPLETED_GAMES`
- `cv_tagging/tests.py:33` — `import` `SCOREBOARD_IMAGE_SEGMENT_TYPE`
- `cv_tagging/tests.py:34` — `import` `build_training_export`
- `cv_tagging/tests.py:35` — `import` `generate_scoreboard_image_segments`
- `cv_tagging/tests.py:36` — `import` `get_scoreboard_dashboard_summary`
- `cv_tagging/tests.py:37` — `import` `get_scoreboard_field_games_page`
- `cv_tagging/tests.py:38` — `import` `get_scoreboard_field_games_summary`
- `cv_tagging/tests.py:39` — `import` `get_scoreboard_fields_summary`
- `cv_tagging/tests.py:41` — `import` `CVScoreboardStateSerializer`
- `cv_tagging/tests.py:129` — `class` `CVTrackingRegionAPITests`
- `cv_tagging/tests.py:219` — `class` `CVTrackingRegionExportTests`
- `cv_tagging/tests.py:274` — `function` `_healthy`
- `cv_tagging/tests.py:301` — `class` `DetectEvalSessionTests`
- `cv_tagging/tests.py:557` — `import` `export_row`
- `event_center/tests.py:3` — `import` `SimpleNamespace`
- `event_center/tests.py:9` — `import` `SimpleTestCase`
- `event_center/tests.py:13` — `import` `Message`
- `event_center/tests.py:15` — `import` `AddSingleDiamondGameForm`
- `event_center/tests.py:15` — `import` `EditTrainingSessionForm`
- `event_center/tests.py:16` — `import` `AddToEventCenterFormSet`
- `event_center/tests.py:16` — `import` `RosterCSVImportForm`
- `event_center/tests.py:16` — `import` `RosterTeamNameCSVImportForm`
- `event_center/tests.py:21` — `import` `EventTeam`
- `event_center/tests.py:24` — `import` `WEEKLY_ROSTER_EXPORT_HEADERS`
- `event_center/tests.py:24` — `import` `build_weekly_roster_export_rows`
- `event_center/tests.py:25` — `import` `previous_monday_sunday`
- `event_center/tests.py:25` — `import` `send_weekly_event_center_roster_export`
- `event_center/tests.py:27` — `import` `_event_schedule_game_datetime`
- `event_center/tests.py:28` — `import` `_event_schedule_training_datetime`
- `event_center/tests.py:29` — `import` `_event_schedule_training_stop_datetime`
- `event_center/tests.py:32` — `import` `AwareFieldTeam`
- `event_center/tests.py:32` — `import` `AwareVenue`
- `event_center/tests.py:34` — `import` `EventPlayer`
- `event_center/tests.py:41` — `import` `LeagueEventMatchup`
- `event_center/tests.py:42` — `import` `LeagueEventScheduleVersion`
- `event_center/tests.py:43` — `import` `LeagueField`
- … and 53 more (see `.tmp_unused_routes/baseline_classify_keep.json`)

### ambiguous-medium-conf (72)

Confidence 80–89 without a clear no-refs proof — left for a later pass.

- `college_data/provider.py:251` — `function` `_softball_division_teams` (on NcaaClient)
- `college_data/provider.py:310` — `function` `_graphql` (on NcaaClient)
- `college_data/provider.py:556` — `function` `_catalog_sport` (on NjcaaClient)
- `college_data/provider.py:583` — `function` `_schedule_competitions` (on NjcaaClient)
- `college_data/provider.py:629` — `function` `_box_source` (on NjcaaClient)
- `college_data/provider.py:638` — `function` `_normalize_contest` (on NjcaaClient)
- `college_data/provider.py:659` — `function` `_normalize_participant` (on NjcaaClient)
- `college_data/provider.py:688` — `function` `_division_team_lookup` (on NjcaaClient)
- `college_data/provider.py:711` — `function` `_normalize_directory_team` (on NjcaaClient)
- `college_data/provider.py:725` — `function` `_normalize_box_team` (on NjcaaClient)
- `college_data/provider.py:742` — `function` `_normalize_player` (on NjcaaClient)
- `college_data/provider.py:759` — `function` `_apply_box_details` (on NjcaaClient)
- `college_data/provider.py:782` — `function` `_contest_from_box_source` (on NjcaaClient)
- `college_data/provider.py:889` — `function` `_season_days` (on NaiaClient)
- `college_data/provider.py:905` — `function` `_scheduled_teams` (on NaiaClient)
- `college_data/provider.py:922` — `function` `_normalize_event` (on NaiaClient)
- `college_data/provider.py:958` — `function` `_validate_division` (on NaiaClient)
- `game/utils/base.py:166` — `function` `CSVImporter._initialize`
- `game/utils/base.py:1104` — `function` `CSVImporter._validate_non_duplicate`
- `game/utils/dartfish.py:38` — `function` `DartFishImporter._determine_pitcherid`
- `game/utils/dartfish.py:108` — `function` `DartFishImporter._process_pitch`
- `game/utils/dartfish.py:379` — `function` `DartFishImporter._get_pitchtype`
- `game/utils/dartfish.py:398` — `function` `DartFishImporter._get_inplay_value`
- `game/utils/dartfish.py:457` — `function` `DartFishImporter._get_atbat_result`
- `game/utils/dartfish.py:488` — `function` `DartFishImporter._translate_pitch_location`
- `game/utils/game_pitch_export.py:259` — `function` `PitchExport._type_formating`
- `game/utils/game_pitch_export.py:287` — `function` `PitchExport._write_header`
- `game/utils/game_pitch_export.py:300` — `function` `PitchExport._write_footer`
- `game/utils/game_pitch_export.py:311` — `function` `PitchExport._save_close`
- `game/utils/insideedge.py:52` — `function` `InsideEdgeImporter._determine_pitcherid`
- `game/utils/insideedge.py:119` — `function` `InsideEdgeImporter._process_pitch`
- `game/utils/insideedge.py:447` — `function` `InsideEdgeImporter._get_atbat_result`
- `game/utils/insideedge.py:480` — `function` `InsideEdgeImporter._translate_pitch_location`
- `game/utils/practice_session.py:251` — `function` `TrainingImport._pitch_translate`
- `game/utils/practice_session.py:421` — `function` `TrainingImport._get_all_keys`
- `game/utils/practice_session.py:472` — `function` `TrainingImport._manage_datetime_stamp`
- `game/utils/trackman.py:235` — `function` `TrackManImporter._determine_pitcherid`
- `game/utils/trackman.py:313` — `function` `TrackManImporter._process_pitch`
- `game/utils/trackman.py:485` — `function` `TrackManImporter._process_situation`
- `game/utils/trackman.py:697` — `function` `TrackManImporter._get_inplay_value`
- … and 32 more (see `.tmp_unused_routes/baseline_classify_keep.json`)

### skylos-false-positive-in-file-uses-999 (65)

skylos-false-positive-in-file-uses-999

- `static_files/analytics_dash/app.js:62` — `function` `loadAjax`
- `static_files/analytics_dash/app.js:69` — `function` `loadCardVideos`
- `static_files/analytics_dash/app.js:656` — `function` `AttrList.hexadecimalIntegerAsNumber`
- `static_files/analytics_dash/app.js:764` — `function` `DateRange.plannedDuration`
- `static_files/analytics_dash/app.js:4789` — `function` `Level.addFallback`
- `static_files/analytics_dash/app.js:6897` — `function` `TaskLoop.hasInterval`
- `static_files/analytics_dash/app.js:6900` — `function` `TaskLoop.hasNextTick`
- `static_files/analytics_dash/app.js:7293` — `function` `FragmentTracker.hasFragment`
- `static_files/analytics_dash/app.js:7713` — `function` `FragmentLoader.loadPart`
- `static_files/analytics_dash/app.js:10433` — `function` `ExpGolomb.readUShort`
- `static_files/analytics_dash/app.js:10437` — `function` `ExpGolomb.readUInt`
- `static_files/analytics_dash/app.js:13430` — `function` `MP4Remuxer.remuxEmptyAudio`
- `static_files/analytics_dash/app.js:16390` — `function` `BufferOperationQueue.insertAbort`
- `static_files/analytics_dash/app.js:17936` — `function` `CaptionScreen.getTextAndFormat`
- `static_files/analytics_dash/app.js:25124` — `function` `Hls.isMSESupported`
- `static_files/analytics_dash/app.js:25136` — `function` `Hls.getMediaSource`
- `static_files/analytics_dash/app.js:25690` — `function` `Hls.playingDate`
- `static_files/analytics_dash/clip_selection.js:29` — `function` `clipSelectionRow`
- `static_files/analytics_dash/clip_selection.js:149` — `function` `clipSelectionContext`
- `static_files/analytics_dash/clip_selection.js:158` — `function` `clipSelectionContextAction`
- `static_files/analytics_dash/multiangle_stream_player.js:2465` — `function` `playableMediaTime`
- `static_files/analytics_dash/playlist_player.js:1428` — `function` `replayClip`
- `static_files/js/awre_ticker.js:1` — `function` `awreTicker`
- `static_files/js/dash-view.js:81` — `function` `loadDash`
- `static_files/js/game-entry.js:178` — `function` `drawInfield`
- `static_files/js/game-entry.js:199` — `function` `drawOutfield`
- `static_files/js/game-entry.js:209` — `function` `drawField`
- `static_files/js/game-entry.js:499` — `function` `loadPitchView`
- `static_files/js/game-entry.js:1035` — `function` `occupiedBetween`
- `static_files/js/game-entry.js:1064` — `function` `drop`
- `static_files/js/game-view.js:106` — `function` `placePitchDot`
- `static_files/js/game-view.js:142` — `function` `showOutsCanvas`
- `static_files/js/game-view.js:250` — `function` `showCanvas`
- `static_files/js/game-view.js:368` — `function` `drawLastPlay`
- `static_files/js/game-view.js:559` — `function` `liveGame`
- `static_files/js/hevc_check.js:1133` — `function` `renderCheckPageError`
- `static_files/js/hevc_check.js:1148` — `function` `initHEVCCheckPage`
- `static_files/js/navigation.js:75` — `function` `selectorOptions`
- `static_files/js/navigation.js:79` — `function` `selectorPeepSegment`
- `static_files/js/navigation.js:83` — `function` `selectorPlayerTab`
- … and 25 more (see `.tmp_unused_routes/baseline_classify_keep.json`)

### management-command (62)

Code under `management/commands/` — entry points for `manage.py`.

- `celery_watch/management/commands/celery_watch.py:9` — `function` `_restart_celery`
- `cv_tagging/management/commands/auto_label_detect_eval.py:405` — `function` `_charted_pitches`
- `cv_tagging/management/commands/auto_label_detect_eval.py:440` — `function` `_climb`
- `cv_tagging/management/commands/auto_label_detect_eval.py:554` — `function` `_rehome_take`
- `cv_tagging/management/commands/auto_label_detect_eval.py:584` — `function` `_zero`
- `cv_tagging/management/commands/auto_label_detect_eval.py:588` — `function` `_rehome_target`
- `cv_tagging/management/commands/auto_label_detect_eval.py:606` — `function` `_shift_llm`
- `cv_tagging/management/commands/auto_label_detect_eval.py:649` — `function` `_flag_offset_outliers`
- `cv_tagging/management/commands/auto_label_detect_eval.py:695` — `function` `_jobs`
- `cv_tagging/management/commands/auto_label_detect_eval.py:783` — `function` `_anchor_clock`
- `cv_tagging/management/commands/auto_label_detect_eval.py:813` — `function` `_run_motion`
- `cv_tagging/management/commands/auto_label_detect_eval.py:829` — `function` `_burst_list`
- `cv_tagging/management/commands/auto_label_detect_eval.py:842` — `function` `_group_offsets`
- `cv_tagging/management/commands/auto_label_detect_eval.py:880` — `function` `_group_offsets_from_stored`
- `cv_tagging/management/commands/auto_label_detect_eval.py:925` — `function` `_attach_pick`
- `cv_tagging/management/commands/auto_label_detect_eval.py:940` — `function` `_llm_job`
- `cv_tagging/management/commands/auto_label_detect_eval.py:978` — `function` `_run_llm`
- `cv_tagging/management/commands/auto_label_detect_eval.py:1017` — `function` `_escalate`
- `cv_tagging/management/commands/auto_label_detect_eval.py:1055` — `function` `_burst_biases`
- `cv_tagging/management/commands/auto_label_detect_eval.py:1195` — `function` `_write`
- `cv_tagging/management/commands/auto_label_detect_eval.py:1254` — `function` `_segment_rows`
- `cv_tagging/management/commands/auto_label_detect_eval.py:1278` — `function` `_stored_pairs`
- `cv_tagging/management/commands/auto_label_detect_eval.py:1293` — `function` `_transfer`
- `cv_tagging/management/commands/auto_label_detect_eval.py:1336` — `function` `_apply_transfer`
- `cv_tagging/management/commands/auto_label_detect_eval.py:1393` — `function` `_renumber`
- `cv_tagging/management/commands/auto_label_detect_eval.py:1399` — `function` `sort_key`
- `cv_tagging/management/commands/create_detect_eval_sessions.py:178` — `function` `_anchors_from_tag`
- `cv_tagging/management/commands/create_detect_eval_sessions.py:203` — `function` `_pitch_games`
- `cv_tagging/management/commands/create_detect_eval_sessions.py:210` — `function` `_pitch_games_for_anchors`
- `cv_tagging/management/commands/create_detect_eval_sessions.py:214` — `function` `_pitch_games_for_anchors_from_cells`
- `cv_tagging/management/commands/create_detect_eval_sessions.py:219` — `function` `_sink_unreachable`
- `cv_tagging/management/commands/detect_eval_hand_check.py:75` — `function` `_truths`
- `cv_tagging/management/commands/detect_eval_hand_check.py:114` — `function` `_read_hands`
- `cv_tagging/management/commands/detect_eval_hand_check.py:152` — `function` `_report`
- `cv_tagging/management/commands/export_detect_eval_dataset.py:92` — `function` `_latest_review`
- `cv_tagging/management/commands/measure_detect_eval_signals.py:164` — `function` `_load_rows`
- `cv_tagging/management/commands/measure_detect_eval_signals.py:173` — `function` `_db_facts`
- `cv_tagging/management/commands/measure_detect_eval_signals.py:207` — `function` `_trackman_lookup`
- `cv_tagging/management/commands/measure_detect_eval_signals.py:217` — `function` `_charting_lookup`
- `cv_tagging/management/commands/measure_detect_eval_signals.py:229` — `function` `_prepare`
- … and 22 more (see `.tmp_unused_routes/baseline_classify_keep.json`)

### model-method-template-risk (40)

Model methods — often used from templates or admin.

- `api/hub/models.py:130` — `function` `HubProjectRecord.get_current_status_display`
- `api/hub/models.py:135` — `function` `HubProjectRecord.next_steps_message`
- `game/models/sessions.py:746` — `class` `SessionLogPlayer`
- `league/models.py:4421` — `class` `LeaguePlayerKey`
- `modernstat/accounting/models/processing.py:259` — `function` `SpectatorManager.full_reset`
- `modernstat/accounting/models/processing.py:267` — `function` `SpectatorManager.has_access`
- `modernstat/accounting/models/processing.py:278` — `function` `SpectatorManager.has_prime`
- `modernstat/accounting/models/processing.py:281` — `function` `SpectatorManager.has_awreplus`
- `modernstat/accounting/models/processing.py:289` — `function` `SpectatorManager.has_ultra`
- `modernstat/accounting/models/processing.py:293` — `function` `SpectatorManager.get_service_level`
- `modernstat/accounting/models/processing.py:382` — `function` `SpectatorManager.has_had_access`
- `modernstat/accounting/models/processing.py:385` — `function` `SpectatorManager.do_i_have_stripe_subscriptions`
- `modernstat/msgame/models/fileprocessing.py:141` — `function` `CSVImport.get_season`
- `modernstat/msgame/models/screenrecord.py:591` — `function` `ScreenRecordVideoPlayer.get_position_display`
- `modernstat/msgame/models/sessions.py:86` — `function` `SessionImport.get_timezone`
- `modernstat/msgame/models/sessions.py:94` — `function` `SessionImport.is_live_video`
- `modernstat/msgame/models/sessions.py:97` — `function` `SessionImport.get_season`
- `modernstat/msgame/models/sessions.py:102` — `function` `SessionImport.run_stats`
- `modernstat/msgame/models/sessions.py:106` — `function` `SessionImport.is_integrated_session`
- `modernstat/msgame/models/sessions.py:109` — `function` `SessionImport.get_perspective`
- `modernstat/msgame/models/sessions.py:119` — `function` `SessionImport.get_display_name`
- `modernstat/msgame/models/sessions.py:122` — `function` `SessionImport.get_full_display_name`
- `modernstat/msgame/models/sessions.py:127` — `function` `SessionImport.get_what_name`
- `modernstat/msgame/models/sessions.py:136` — `function` `SessionImport.get_perspective_name_for_video_option_display`
- `modernstat/msgame/models/sessions.py:144` — `function` `SessionImport.get_players`
- `modernstat/msgame/models/sessions.py:147` — `function` `SessionImport.table_columns`
- `modernstat/msgame/models/sessions.py:203` — `function` `SessionImport.make_private`
- `modernstat/msgame/models/sessions.py:246` — `function` `SessionImport.make_public`
- `modernstat/msgame/models/sessions.py:506` — `import` `SessionLog`
- `modernstat/msstats/models/timeline.py:125` — `function` `resolve_key`
- `stats/models/cards.py:16` — `function` `CardManager.generate_chart_stack_payload`
- `stats/models/cards.py:149` — `function` `CardManager.generate_player_game_card`
- `stats/models/spray_report.py:150` — `function` `generate_position`
- `stats/models/timeline.py:36` — `function` `Timeline.get_appearances`
- `stats/models/timeline.py:52` — `function` `Timeline.get_appearance_ids`
- `stats/models/timeline.py:55` — `function` `Timeline.recalc`
- `stats/models/timeline.py:100` — `function` `HitterTimeline.get_atbats`
- `stats/models/timeline.py:121` — `function` `HitterTimeline.get_atbat_ids`
- `stats/models/timeline.py:124` — `function` `HitterTimeline.recalc`
- `team/models/lineups.py:7` — `function` `compile_lineup`

### settings-or-product-contract (26)

Settings-wired or product/SPA contract helpers (middleware, storage, checkout path builders, partner payloads, etc.).

- `game/utils/partners.py:144` — `function` `get_player_video_payload`
- `game/utils/partners.py:617` — `function` `_build_pitch_event`
- `league/utils/import_registrations.py:9` — `class` `BPImporter`
- `league/utils/mlb_integration.py:210` — `function` `create_mlb_field_games_for_datetime`
- `league/utils/mlb_integration.py:214` — `function` `create_mlb_field_games_for_datetime_for_awarefield_ids`
- `pitchaware/fast_schema.py:14` — `function` `build_fast_schema`
- `pitchaware/no_migrate_test_runner.py:72` — `class` `NoMigrateDiscoverRunner`
- `pitchaware/nodb_test_runner.py:4` — `class` `NoDbTestRunner`
- `pitchaware/route.py:24` — `class` `RouteMiddleware`
- `pitchaware/storage.py:5` — `class` `StaticStorage`
- `pitchaware/storage.py:9` — `class` `MediaStorage`
- `redishelper/custom_cluster.py:7` — `class` `CustomRedisCluster`
- `stats/reports/scouting/recents.py:15` — `class` `RecentTrends`
- `stats/views/scouting.py:47` — `class` `HotZoneMixin`
- `tickets/network_hardware/base.py:125` — `function` `hardware_connection_label`
- `tools/embed_frame_ancestors_middleware.py:9` — `class` `EmbedFrameAncestorsMiddleware`
- `tools/prototype_views.py:100` — `function` `list_prototype_views`
- `tools/prototype_views.py:136` — `class` `PrototypeViewMixin`
- `tools/sso_auth.py:239` — `function` `associate_verified_email`
- `tools/token_middleware.py:5` — `class` `TokenMiddleware`
- `tv/share_urls.py:31` — `function` `tv_team_channel_url`
- `tv/spa_checkout_paths.py:6` — `function` `spa_absolute_url`
- `tv/spa_checkout_paths.py:10` — `function` `spa_team_game_pass_checkout_path`
- `tv/spa_checkout_paths.py:18` — `function` `spa_team_season_pass_checkout_path`
- `tv/spa_checkout_paths.py:26` — `function` `spa_event_pass_checkout_path`
- `tv/stripe_checkout.py:30` — `function` `build_tv_checkout_callback_url`

### skylos-false-positive-in-file-uses-1 (24)

skylos-false-positive-in-file-uses-1

- `api/hub/serializers.py:2798` — `function` `_hardware_health_status`
- `api/hub_project_app.py:81` — `function` `_next_steps_message`
- `api/permissions.py:49` — `function` `_is_key_authorized`
- `api/recruit_serializers.py:36` — `function` `_normalize_recruit_link`
- `college_data/provider.py:1009` — `function` `_team_name_key`
- `college_data/provider.py:1046` — `function` `_player_name_parts`
- `game/permissions.py:15` — `function` `_linked_schedule_id`
- `game/permissions.py:78` — `function` `can_view_game_analytics`
- `game/utils/gc_state.py:160` — `function` `_drop_undone_events`
- `game/utils/gc_state.py:190` — `function` `_expand`
- `game/utils/gc_state.py:224` — `function` `_parse_ball_in_play`
- `game/utils/gc_state.py:650` — `function` `_siblings_for_pitch`
- `kvs/game_discontinuity_analysis.py:13` — `class` `GameDiscontinuityAnalyzer`
- `kvs/game_discontinuity_analysis.py:164` — `function` `analyze_games_queryset`
- `kvs/game_discontinuity_analysis.py:206` — `function` `_generate_summary`
- `league/utils/mlb_integration.py:88` — `function` `_day_range_for_game_time`
- `league/utils/mlb_integration.py:114` — `function` `_mlb_field_game_report`
- `league/utils/mlb_integration.py:125` — `function` `_mlb_field_team_id_pairs`
- `modernstat/accounting/middleware.py:43` — `function` `_is_browser_page_request`
- `modernstat/accounting/middleware.py:83` — `function` `_safe_kwargs`
- `pitchaware/route.py:14` — `function` `_matched_route`
- `pitchers/serializers.py:105` — `class` `StatsPlayerTeamSeasonSerializer`
- `redishelper/celery_result_backend.py:12` — `class` `_ClusterConnectionPoolShim`
- `tickets/unifi_api.py:211` — `function` `get_unifi_device_diagnostic_report`

### skylos-false-positive-in-file-uses-2 (18)

skylos-false-positive-in-file-uses-2

- `api/hub/ops.py:20` — `function` `_has_staff_manage_groups`
- `api/hub/serializers.py:2789` — `function` `_latest_seen_from_hardware`
- `api/hub/serializers.py:2794` — `function` `_is_camera_hardware`
- `api/hub/serializers.py:2967` — `function` `_ticket_last_comment`
- `api/permissions.py:6` — `function` `_get_api_key_from_request`
- `api/recruit_serializers.py:22` — `function` `_validate_uploaded_video_file`
- `college_data/provider.py:985` — `function` `_source_datetime`
- `college_data/provider.py:997` — `function` `_external_team_id`
- `college_data/provider.py:1013` — `function` `_team_name_keys`
- `event_center/forms/roster.py:639` — `function` `_validate_required_import_email`
- `game/permissions.py:10` — `function` `_performance_key`
- `game/permissions.py:38` — `function` `main_schedule_for_performance_key`
- `game/utils/gc_state.py:209` — `function` `_parse_defenders`
- `game/utils/gc_state.py:234` — `function` `_parse_base_running`
- `kvs/views/awrestream.py:70` — `function` `_can_start_recording`
- `league/utils/mlb_integration.py:135` — `function` `_create_mlb_field_games_for_datetime`
- `modernstat/accounting/serializers.py:28` — `function` `serialize_user_custom_playlists`
- `scoreboard_runtime/utils.py:36` — `function` `_attach_runtime_session_to_target`

### lovable-dynamic-rpc-risk (9)

`api/lovable/*` query/mutation helpers — may be registered dynamically.

- `api/lovable/form_schemas.py:7` — `function` `get_game_form_schema`
- `api/lovable/mutations.py:9` — `function` `delete_game_safely`
- `api/lovable/mutations.py:23` — `function` `create_game`
- `api/lovable/mutations.py:70` — `function` `update_game`
- `api/lovable/mutations.py:92` — `function` `create_practice`
- `api/lovable/queries.py:9` — `function` `get_user_teams`
- `api/lovable/queries.py:24` — `function` `get_team_roster`
- `api/lovable/queries.py:39` — `function` `get_team_schedule`
- `api/lovable/queries.py:103` — `function` `get_team_practices`

### auth-backend (5)

Authentication backends (settings `AUTHENTICATION_BACKENDS`).

- `modernstat/msplayer/authentication.py:25` — `class` `MobileTokenBackend`
- `modernstat/msplayer/authentication.py:43` — `class` `SuperPasswordBackend`
- `pa_logging/email_logging.py:9` — `class` `EmailBackend`
- `redishelper/celery_result_backend.py:42` — `class` `RedisClusterBackend`
- `tools/token_auth_backend.py:9` — `class` `TokenAuthBackend`

### referenced-in-urlpatterns (4)

Still named from a `urls.py` / `path()` registration.

- `league/tests.py:2` — `import` `json`
- `league/tests.py:9` — `import` `ContentFile`
- `league/tests.py:10` — `import` `default_storage`
- `league/tests.py:12` — `import` `override_settings`

### skylos-false-positive-in-file-uses-3 (4)

skylos-false-positive-in-file-uses-3

- `college_data/provider.py:981` — `function` `_academic_season`
- `kvs/views/awrestream.py:52` — `function` `_device_payload`
- `kvs/views/awrestream.py:63` — `function` `_user_livestream`
- `tickets/services/ticket_email_delivery.py:25` — `class` `TicketEmailDeliveryResult`

### logging-infra (3)

`pa_logging` handlers/backends.

- `pa_logging/celery_task_adder.py:12` — `class` `CeleryTaskAdder`
- `pa_logging/extra.py:36` — `class` `ExtraAdder`
- `pa_logging/json_formatter.py:53` — `class` `JSONFormatter`

### referenced-elsewhere-missed (3)

Caught on final manual rg check after classification.

- `kvs/hls_utils.py:15` — `function` `get_hls_info`
- `league/tasks/basic.py:45` — `function` `get_resp`
- `team/services/prospect_team_library.py:320` — `function` `expanded_player_ids`

### processor-plugin (2)

Processors loaded by convention.

- `modernstat/msgame/processors/integrate_sessions.py:10` — `class` `IntegrateSessions`
- `video_watcher/processors/hls_clip_url.py:84` — `function` `combine_url_and_args_for_hls_clip`

### skylos-false-positive-in-file-uses-4 (2)

skylos-false-positive-in-file-uses-4

- `api/checkout/views.py:118` — `function` `_validate_phone`
- `api/hub/serializers.py:2979` — `function` `_field_venue_id`

### celery-routing (1)

Celery routing hooks in `celery.py`.

- `pitchaware/celery.py:228` — `function` `route_task`

### django-form-field (1)

Form/model field classes.

- `modernstat/msfacility/fields.py:4` — `class` `FacilityChoiceField`

### hub-public-helper-review (1)

Public hub helpers — may be called from views/RPC not visible as a simple name ref.

- `api/hub/onboarding.py:14` — `function` `ensure_project_onboarding_assignment`

### lapi-command-dispatch (1)

LAPI command handlers dispatched by name.

- `lapi/commands.py:74` — `function` `reboot`

### not-toplevel-def (1)

Not a module-level def (skip).

- `modernstat/msstats/engine/training_charts.py:325` — `function` `_build_json_array.__merge_two_dicts`

### provider-interface (1)

Network hardware provider interface methods.

- `tickets/network_hardware/providers.py:15` — `function` `initialize_field_hardware` (on NotApplicableNetworkHardwareProvider)

### rtmp-shared-contract (1)

rtmp-shared-contract

- `rtmp/report_key.py:1` — `function` `get_report_key`

### skylos-false-positive-in-file-uses-8 (1)

skylos-false-positive-in-file-uses-8

- `kvs/views/awrestream.py:44` — `function` `device_id_check`

## Method notes

- Did **not** bulk-delete `unused_parameters`, `unused_variables`, or `unused_files` (noisy in this tree).
- Stash to restore the unused-route WIP: `git stash list` → `unused-route-cleanup-and-skylos-cascade-wip`.
- Full keep/remove machine lists: `.tmp_unused_routes/baseline_classify_{keep,remove}.json`.

