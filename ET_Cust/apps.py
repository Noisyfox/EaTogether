from django.apps import AppConfig


class EtCustConfig(AppConfig):
    name = 'ET_Cust'

    def ready(self):
        import ET_Cust.signals
