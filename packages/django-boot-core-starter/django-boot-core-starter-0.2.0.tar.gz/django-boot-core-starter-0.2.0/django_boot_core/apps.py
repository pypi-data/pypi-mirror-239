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
        if hasattr(settings, "DJANGO_BOOT"):
            DI_PACKAGES = settings.DJANGO_BOOT.get("DI_PACKAGES", [])
            to_scan += DI_PACKAGES

            if settings.DJANGO_BOOT.get("DI_SCAN_STARTERS", False):
                for app in settings.INSTALLED_APPS:
                    if app.endswith("_starter"):
                        to_scan.append(app)

        t1 = time.time()
        ApplicationContext.initialize(to_scan)
        duration = time.time() - t1
        unit = "seconds"
        if duration < 1:
            duration = duration * 1000
            unit = "milliseconds"
        duration = "%.2f" % round(duration, 2)
        logger.info(f"Application context initialized in {duration} {unit}")
