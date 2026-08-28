# Side-effect import so `celery worker -A self_import_pkg` loads the app.
# Skylos reports this as a one-node cycle: self_import_pkg → self_import_pkg.
from self_import_pkg import celery
