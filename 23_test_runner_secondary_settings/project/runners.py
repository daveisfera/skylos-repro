from django.test.runner import DiscoverRunner


class NoMigrateDiscoverRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        return None


class LegacyNoDbRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        pass
