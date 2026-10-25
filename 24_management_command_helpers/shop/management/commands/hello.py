"""Literal mgmt helper shape: private helpers defined AFTER handle."""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(_format_name(options.get("name", "")))
        pitches = _charted_pitches(set(options.get("game_ids") or []))
        self.stdout.write(_format_pitch_summary(pitches))


def _format_name(name):
    return name.strip().title()


def _charted_pitches(game_ids):
    return {gid: [{"pitch": 1}] for gid in game_ids}


def _format_pitch_summary(pitches_by_game):
    return f"pitches={sum(len(v) for v in pitches_by_game.values())}"


def _unused_export_job():
    return "dead"
