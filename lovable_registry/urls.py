from .factory import create_viewset_class
from .registry import REGISTERED_MODELS

urlpatterns = []
for item in REGISTERED_MODELS:
    model, config = item[0], item[1]
    viewset = create_viewset_class(model, config)
    globals()[viewset.__name__] = viewset
    urlpatterns.append((model.__name__.lower(), viewset))
