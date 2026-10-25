from handlers import form_schemas, mutations
from rpc import registry


def dispatch(kind, request):
    relation = registry.HANDLERS[kind]
    create_name = relation.get("create_method")
    options_name = relation.get("options_method")
    destroy_name = relation.get("destroy_method")
    if create_name:
        getattr(mutations, create_name)(request)
    if options_name and hasattr(form_schemas, options_name):
        getattr(form_schemas, options_name)(request)
    if destroy_name:
        getattr(mutations, destroy_name)(request)


dispatch("games", object())
