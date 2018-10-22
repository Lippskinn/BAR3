# start Nina
from django.conf import settings
from django.db.backends.signals import connection_created
from django.db.models import F
from django.dispatch import receiver
import math
from django.core.mail import send_mail

from Cith2.models import Resource
from Cith2.models import Query
from django.db.models.signals import post_save

# Because sqllite doesn't support math functions
#@receiver(connection_created)
#def extend_sqlite(connection=None, **kwargs):
    #if connection.vendor == "sqlite":
        #cf = connection.connection.create_function
        #cf('acos', 1, math.acos)
        #cf('cos', 1, math.cos)
        #cf('radians', 1, math.radians)
        #cf('sin', 1, math.sin)

# Everytime when a Resource instance finalize the execution of its save method, the get_Query function will be executed
# Senden einer E-mail, wenn eine neue Ressource angelegt oder verändert wird, die auf eine gespeicherte Suchanfrage passt
@receiver(post_save, sender=Resource)
def get_Query(sender, instance: Resource, created, **kwargs):

    if instance.constraints.exists():

        success = Query.objects.filter(
            title__contains=instance.title).filter(
            startDate__gte=instance.constraints.get().startDate).filter(
            endDate__lte=instance.constraints.get().endDate).filter(
            longitude__gt=(instance.locationLong - F('ambit'))).filter(
            latitude__gt=(instance.locationLat - F('ambit'))).filter(
            longitude__lt=(instance.locationLong + F('ambit'))).filter(
            latitude__lt=(instance.locationLat + F('ambit')))
    else:
        success = Query.objects.filter(
            title__contains=instance.title).filter(
            longitude__gt=(instance.locationLong - F('ambit'))).filter(
            latitude__gt=(instance.locationLat - F('ambit'))).filter(
            longitude__lt=(instance.locationLong + F('ambit'))).filter(
            latitude__lt=(instance.locationLat + F('ambit')))

    #print(success)

    for entry in success:
        print(success)
        mail = entry.userId.email

        send_mail(
            'Interessante Ressource',
            'Im Ressourcenpool Bamberg wurde soeben eine möglicherweise für Sie interessante Ressource angelegt.',
            settings.EMAIL_HOST_USER,
            [mail],
            fail_silently=False,
        )

# end Nina