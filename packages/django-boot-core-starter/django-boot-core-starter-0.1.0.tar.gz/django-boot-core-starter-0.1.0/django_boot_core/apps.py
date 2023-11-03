from django.apps import AppConfig
from rhazes.context import ApplicationContext
from django.conf import settings
import logging
import time

logger = logging.getLogger(__name__)


class DjangoBootCoreConfig(AppConfig):
    name = "django_boot_core"

    def ready(self):
        to_scan = ["django_boot_core.services"]
        if hasattr(settings, "DI_PACKAGES") and type(settings.DI_PACKAGES) == list:
            to_scan += settings.DI_PACKAGES
        t1 = time.time()
        ApplicationContext.initialize(to_scan)
        duration = time.time() - t1
        unit = "seconds"
        if duration < 1:
            duration = duration * 1000
            unit = "milliseconds"
        duration = "%.2f" % round(duration, 2)
        logger.info(f"Application context initialized in {duration} {unit}")
