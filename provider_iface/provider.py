"""Multi-method duck-typed client — college_data NcaaClient shape.

Factory returns the concrete client; call sites in pipeline.py only use the base
type. Soft-keys: schedule_dates, division_teams, game_detail, box_score,
play_by_play (do not write Class.method forms in repo docs — that quiets them).
"""

SPORT_CODES = {"baseball": "MBA", "softball": "WSB"}
SCHEDULE_HASH = "abc"


class ProviderError(Exception):
    pass


class BaseProviderClient:
    failure_limit = 3

    def _check_enabled(self):
        return True

    def _wait_for_rate_limit(self):
        return None

    def _graphql(self, endpoint, request_key, query_hash, params):
        return {"data": {}}, "{}"

    def _record_failure(self, message):
        return message


class NcaaClient(BaseProviderClient):
    def __init__(self, provider=None, import_run=None):
        self.provider = provider
        self.import_run = import_run
        self.session = None
        self.last_request_at = 0

    def schedule_dates(self, sport: str, division: int, season: int):
        payload, raw = self._graphql(
            endpoint="schedule",
            request_key=f"{sport}:{division}:{season}",
            query_hash=SCHEDULE_HASH,
            params={
                "variables": {
                    "sportCode": SPORT_CODES[sport],
                    "division": division,
                    "seasonYear": season,
                }
            },
        )
        games = payload.get("data", {}).get("schedules", {}).get("games", [])
        return games, raw

    def scoreboard(self, sport: str, division: int, season: int, contest_date: str):
        return self._graphql(
            endpoint="scoreboard",
            request_key=f"{sport}:{division}:{season}:{contest_date}",
            query_hash=SCHEDULE_HASH,
            params={"variables": {"contestDate": contest_date}},
        )

    def division_teams(self, sport: str, division: int, season: int):
        self._check_enabled()
        self._wait_for_rate_limit()
        return {1: "Team A"}

    def game_detail(self, game_id: str):
        return self._graphql(
            endpoint="game",
            request_key=game_id,
            query_hash=SCHEDULE_HASH,
            params={},
        )

    def box_score(self, game_id: str):
        return self._graphql(
            endpoint="box",
            request_key=game_id,
            query_hash=SCHEDULE_HASH,
            params={},
        )

    def play_by_play(self, game_id: str):
        return self._graphql(
            endpoint="pbp",
            request_key=game_id,
            query_hash=SCHEDULE_HASH,
            params={},
        )


class NotApplicableNetworkHardwareProvider:
    def probe(self):
        return {"ok": True}

    def sync_inventory(self):
        return []

    def apply_config(self, payload: dict):
        return payload

    def initialize_field_hardware(self):
        return True


def get_provider_client(provider, import_run):
    if getattr(provider, "slug", "ncaa") == "ncaa":
        return NcaaClient(provider, import_run)
    raise ProviderError("unsupported")
