"""Call sites use factory client; do not name concrete NcaaClient methods here."""

from provider_iface.provider import get_provider_client


class _Provider:
    slug = "ncaa"


class _ImportRun:
    sport = "baseball"
    division = 1
    season = 2026


def import_month(client, season: int, month: int):
    schedule_dates, _ = client.schedule_dates("baseball", 1, season)
    dates = list(schedule_dates) or [f"{season}-{month:02d}-01"]
    return client.scoreboard("baseball", 1, season, dates[0])


def run():
    client = get_provider_client(_Provider(), _ImportRun())
    return import_month(client, 2026, 10)
