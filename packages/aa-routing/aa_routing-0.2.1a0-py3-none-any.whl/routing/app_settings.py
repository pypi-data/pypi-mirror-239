from django.apps import apps


def corptools_active() -> bool:
    return apps.is_installed("corptools")


def drifters_active() -> bool:
    return apps.is_installed("drifters")
