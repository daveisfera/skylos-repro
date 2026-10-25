"""Nested REGISTERED_MODELS-style config — string method names only."""

# Minimal stand-in for a Django model class (factory only needs __name__ / _meta).
class Game:
    class _meta:
        verbose_name_plural = "games"


class PlayerTeamSeason:
    class _meta:
        verbose_name_plural = "roster"


REGISTERED_MODELS = [
    (
        Game,
        {
            "allowed_methods": ["list", "create", "retrieve", "update", "destroy"],
            "queryset_method": "get_team_schedule",
            "create_method": "create_game",
            "update_method": "update_game",
            "destroy_method": "delete_game_safely",
            "options_method": "get_game_form_schema",
            "related_models": {
                "roster": {
                    "model": PlayerTeamSeason,
                    "queryset_method": "get_team_roster",
                    "create_method": "create_practice",
                    "options_method": "get_game_form_schema",
                },
            },
        },
    ),
    (
        PlayerTeamSeason,
        {
            "allowed_methods": ["list"],
            "queryset_method": "get_user_teams",
        },
    ),
]
