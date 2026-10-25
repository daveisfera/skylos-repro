"""Multi-method duck-typed client — college_data NcaaClient shape."""


class Provider:
    def schedule_dates(self, season: int):
        raise NotImplementedError

    def scoreboard(self, day: str):
        raise NotImplementedError

    def division_teams(self, division: str):
        raise NotImplementedError

    def game_detail(self, game_id: str):
        raise NotImplementedError

    def box_score(self, game_id: str):
        raise NotImplementedError

    def play_by_play(self, game_id: str):
        raise NotImplementedError


class NcaaClient(Provider):
    def _graphql(self, query: str) -> dict:
        return {"query": query, "data": {}}

    def schedule_dates(self, season: int):
        return self._graphql(f"schedule({season})")["data"] or [f"{season}-01-01"]

    def scoreboard(self, day: str):
        return self._graphql(f"scoreboard({day})")

    def division_teams(self, division: str):
        return self._graphql(f"teams({division})")

    def game_detail(self, game_id: str):
        return self._graphql(f"game({game_id})")

    def box_score(self, game_id: str):
        return self._graphql(f"box({game_id})")

    def play_by_play(self, game_id: str):
        return self._graphql(f"pbp({game_id})")


def fetch_day(provider: Provider, day: str):
    # Call sites only name scoreboard on the base type.
    return provider.scoreboard(day)


RESULT = fetch_day(NcaaClient(), "2026-10-23")
