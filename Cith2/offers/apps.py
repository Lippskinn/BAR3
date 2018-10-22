# start Nina

from django.apps import AppConfig


class OffersConfig(AppConfig):
    name = 'Cith2.offers'

    def ready(self):
        import Cith2.offers.signals

# end Nina