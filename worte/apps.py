from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_stufen(*args, **kwargs):
    from worte.models import Stufe
    Stufe.objects.get_or_create(stufe='A')
    Stufe.objects.get_or_create(stufe='B')


class WorteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'worte'

    def ready(self):
        post_migrate.connect(create_stufen, sender=self)
