"""Provider interface — duck-typed calls on base type (web-server college_data shape).

schedule_dates is part of the live provider contract but never named at the
call site below.
"""


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
    return provider.scoreboard(day)


# Entry keeps ConcreteProvider / scoreboard live; schedule_dates stays contract-only.
RESULT = fetch_day(ConcreteProvider(), "2026-10-23")
