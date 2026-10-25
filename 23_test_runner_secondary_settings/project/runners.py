from django.test.runner import DiscoverRunner


class NoMigrateDiscoverRunner(DiscoverRunner):
    """Assigned from settings_tests_discover — should stay quiet once string entrypoints work."""

    def setup_databases(self, **kwargs):
        return None


class LegacyNoDbRunner(DiscoverRunner):
    """Only named in a commented TEST_RUNNER on primary settings — should FLAG."""

    def setup_databases(self, **kwargs):
        pass
