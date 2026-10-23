"""Provider interface methods — called via duck typing on the base type."""


class Provider:
    def schedule_dates(self, season: int):
        raise NotImplementedError

    def scoreboard(self, day: str):
        raise NotImplementedError


class ConcreteProvider(Provider):
    def schedule_dates(self, season: int):
        return [f"{season}-01-01"]

    def scoreboard(self, day: str):
        return {"day": day, "games": []}


def fetch_day(provider: Provider, day: str):
    # Call sites only see the base type; schedule_dates is contract-only here.
    return provider.scoreboard(day)


def run():
    return fetch_day(ConcreteProvider(), "2026-10-23")


RESULT = run()
