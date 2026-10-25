"""Literal extract of consumer api/lovable/factory.py getattr pattern."""

import form_schemas
import mutations
import queries


class GenericViewSet:
    pass


class Response:
    def __init__(self, data=None, status=200, headers=None):
        self.data = data
        self.status = status


def create_viewset_class(model_class, config=None):
    if config is None:
        config = {}

    model_name_plural = model_class._meta.verbose_name_plural
    related_models_config = config.get("related_models", {})
    queryset_method_name = config.get("queryset_method")
    allowed_methods = config.get(
        "allowed_methods",
        ["list", "create", "retrieve", "update", "partial_update", "destroy"],
    )
    custom_destroy_method = config.get("destroy_method")
    custom_create_method = config.get("create_method")
    custom_update_method = config.get("update_method")
    options_method_name = config.get("options_method")

    def get_queryset(self):
        if hasattr(self, "_queryset_method_name") and self._queryset_method_name:
            if hasattr(queries, self._queryset_method_name):
                query_func = getattr(queries, self._queryset_method_name)
                return query_func(self.request)
        return []

    class_dict = {
        "__doc__": f"API Endpoint to manage {model_name_plural}.",
        "_queryset_method_name": queryset_method_name,
        "get_queryset": get_queryset,
    }

    if custom_create_method and "create" in allowed_methods:

        def create(self, request, *args, **kwargs):
            if hasattr(mutations, custom_create_method):
                mutation_func = getattr(mutations, custom_create_method)
                result = mutation_func(request, None)
                if isinstance(result, Response):
                    return result
                return Response(result, status=201)
            return Response(status=201)

        class_dict["create"] = create

    if custom_update_method and (
        "update" in allowed_methods or "partial_update" in allowed_methods
    ):

        def update(self, request, *args, **kwargs):
            instance = object()
            if hasattr(mutations, custom_update_method):
                mutation_func = getattr(mutations, custom_update_method)
                result = mutation_func(instance, request)
                if isinstance(result, Response):
                    return result
                return Response(result)
            return Response()

        class_dict["update"] = update

    if custom_destroy_method and "destroy" in allowed_methods:

        def destroy(self, request, *args, **kwargs):
            instance = object()
            if hasattr(mutations, custom_destroy_method):
                mutation_func = getattr(mutations, custom_destroy_method)
                return mutation_func(instance, request)
            return Response(status=204)

        class_dict["destroy"] = destroy

    if options_method_name:

        def options(self, request, *args, **kwargs):
            if hasattr(form_schemas, options_method_name):
                schema_func = getattr(form_schemas, options_method_name)
                return Response(schema_func(request))
            return Response({})

        class_dict["options"] = options

    for relation_name, relation_config in related_models_config.items():
        related_qs_name = relation_config.get("queryset_method")
        related_create_name = relation_config.get("create_method")
        related_options_name = relation_config.get("options_method")

        def related_action(
            self,
            request,
            *args,
            _qs=related_qs_name,
            _create=related_create_name,
            **kwargs,
        ):
            if request.method == "GET" and _qs and hasattr(queries, _qs):
                return Response(getattr(queries, _qs)(request))
            if request.method == "POST" and _create and hasattr(mutations, _create):
                return Response(getattr(mutations, _create)(request, None), status=201)
            return Response([])

        class_dict[relation_name] = related_action

        if related_options_name:

            def related_options(self, request, *args, _opt=related_options_name, **kwargs):
                if hasattr(form_schemas, _opt):
                    return Response(getattr(form_schemas, _opt)(request))
                return Response({})

            class_dict[f"{relation_name}_options"] = related_options

    name = f"{model_class.__name__}LovableViewSet"
    return type(name, (GenericViewSet,), class_dict)
