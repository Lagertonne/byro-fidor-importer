from django.apps import AppConfig
from django.utils.translation import ugettext_lazy


class PluginApp(AppConfig):
    name = 'byro_fidor_importer'
    verbose_name = 'Fidor importer for byro'

    class ByroPluginMeta:
        name = ugettext_lazy('Fidor importer for byro')
        author = 'lagertonne'
        description = ugettext_lazy('This importer can handle the csv files exported by fidor')
        visible = True
        version = '0.2'

    def ready(self):
        from . import signals  # NOQA


default_app_config = 'byro_fidor_importer.PluginApp'
