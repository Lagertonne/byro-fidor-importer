from django.apps import AppConfig
from django.utils.translation import ugettext_lazy


class PluginApp(AppConfig):
    name = 'byro_fidor_importer'
    verbose_name = 'Fidor importer for byro'

    class ByroPluginMeta:
        name = ugettext_lazy('Fidor importer for byro')
        author = 'lagertonne'
        description = ugettext_lazy('Short description')
        visible = True
        version = '0.0.1'

    def ready(self):
        from . import signals  # NOQA


default_app_config = 'byro_fidor_importer.PluginApp'
