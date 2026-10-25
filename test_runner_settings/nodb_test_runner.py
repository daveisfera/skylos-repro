"""Custom test runner — named from a secondary settings module only."""


class DiscoverRunner:
    def setup_databases(self, **kwargs):
        raise NotImplementedError


class NoDbTestRunner(DiscoverRunner):
    """Skip DB setup — used when TEST_RUNNER points here from settings_ci."""

    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass
