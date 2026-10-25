"""Mutation handlers — only reached via factory getattr(mutations, name)."""


def create_game(request, serializer):
    return {"id": 1}


def update_game(instance, request):
    return instance


def delete_game_safely(instance, request):
    return {"deleted": True}


def create_practice(request, serializer):
    return {"id": 2}
