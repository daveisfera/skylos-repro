"""Custom runners — NoDbTestRunner is only named in a comment on primary settings.

Secondary settings assign a different runner (NoMigrateDiscoverRunner), matching
consumer pitchaware/settings.py + settings_tests_discover.py.
"""


class DiscoverRunner:
    def setup_databases(self, **kwargs):
        raise NotImplementedError


class NoDbTestRunner(DiscoverRunner):
    """Should FLAG — only referenced in a commented TEST_RUNNER line."""

    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass


class NoMigrateDiscoverRunner(DiscoverRunner):
    """Assigned from settings_ci — should stay quiet once string entrypoints work."""

    def setup_databases(self, **kwargs):
        return None
