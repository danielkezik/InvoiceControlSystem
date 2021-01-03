from django.apps import AppConfig


class InvoicesSystemConfig(AppConfig):
    name = 'invoices_system'

    def ready(self):
        import invoices_system.signals
