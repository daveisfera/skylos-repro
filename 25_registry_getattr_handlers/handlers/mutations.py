def create_game(request, **kwargs):
    return {"id": 1}


def delete_game_safely(request, **kwargs):
    return {"ok": True}


def unused_mutation():
    return None
