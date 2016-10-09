from django.apps import AppConfig as BaseAppConfig


class EtConfig(BaseAppConfig):
    name = "ET"
    REMEMBER_ME_EXPIRY = 60 * 60 * 24 * 365 * 10
