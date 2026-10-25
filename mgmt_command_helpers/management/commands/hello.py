"""Literal mgmt helper shape: private helpers defined AFTER handle, called only from handle.

Mirrors consumer auto_label_detect_eval.py where _charted_pitches sits below Command.handle.
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Greet / eval-style command"

    def add_arguments(self, parser):
        parser.add_argument("--name", default="world")
        parser.add_argument("--game-ids", nargs="*", type=int, default=[])

    def handle(self, *args, **options):
        # Helpers are defined later in this module (same as consumer canary).
        self.stdout.write(_format_name(options["name"]))
        pitches = _charted_pitches(set(options["game_ids"]))
        self.stdout.write(_format_pitch_summary(pitches))


def _format_name(name: str) -> str:
    return name.strip().title()


def _charted_pitches(game_ids) -> dict:
    """Private helper after handle — consumer canary shape."""
    out = {}
    for gid in game_ids or []:
        out[gid] = [{"pitch": 1}]
    return out


def _format_pitch_summary(pitches_by_game: dict) -> str:
    total = sum(len(v) for v in pitches_by_game.values())
    return f"pitches={total}"


def _dead_helper():
    # Intentional true positive — nothing in this module calls it.
    return "stale"
