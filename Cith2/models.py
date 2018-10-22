# start Meike
from django.contrib.auth.models import User
from django.db import models
# start Alina
from django.db.models.expressions import RawSQL
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail


class Plz(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=100)
    def __str__(self):
        return str(self.number)

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    address = models.CharField(max_length=50, blank=True)
    plz = models.ForeignKey(Plz, on_delete=models.CASCADE, blank=True, null=True)
    isOrganisation = models.BooleanField(default=False)
    organisationName = models.CharField(max_length=150, blank=True)
    imagePath = models.ImageField(upload_to='static/images/avatars', default='static/images/avatars/avatar-1.jpg')
    def __str__(self):
        return str(self.user)
    #define signals that automatically create/update Account when we create/update User instances
    @receiver(post_save, sender=User)
    def create_user_account(sender, instance, created, **kwargs):
        if created:
            Account.objects.create(user=instance)
        instance.account.save()
#end Alina



class Category(models.Model):
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default="fa fa-gift")

    def __str__(self):
        return self.title
# start Nina
#class ResourceManager(models.Manager):
    #def within_distance(self, lat, long, ambit):
        #gcd = """
                      #6371 * acos(
                       #cos(radians(%s)) * cos(radians(locationLat))
                       #* cos(radians(locationLong) - radians(%s)) +
                       #sin(radians(%s)) * sin(radians(locationLat))
                      #)
                      #"""
        #return self.get_queryset().annotate(distance=RawSQL(gcd, (lat,long, lat))).filter(distance__lt=ambit)

# end Nina
class Resource(models.Model):
    title = models.CharField(max_length=50)
    locationLat = models.FloatField()
    locationLong = models.FloatField()
    description = models.CharField(max_length=400)
    categoryId = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, default=0)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    costs = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    imagePath = models.ImageField(upload_to='static/images/offers')
    deposit = models.CharField(max_length=30, blank=True, null=True)
    #objects = ResourceManager()


    TYPE_CHOICES = (
        ('ZU VERSCHENKEN', 'Zu Verschenken'),
        ('ZU VERLEIHEN', 'Zu Verleihen'),
        ('ZUR MIETE', 'Zur Miete'),
    )
    type = models.CharField(choices=TYPE_CHOICES,
                        default='ZU VERSCHENKEN',
                        max_length=30)

    def __str__(self):
        return self.title


class Watchlist(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    resourceId = models.ForeignKey(Resource, on_delete=models.CASCADE)


class IntervalConstraint(models.Model):
    resourceId = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name="constraints")
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    available = models.BooleanField(default=1)


class Query(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()

    CATEGORY_CHOICES = (
     ('WISSEN & DIENSTLEISTUNGEN', 'Wissen & Dienstleistungen'),
     ('BÜCHER, MUSIK & FILM', 'Bücher, Musik & Film'),
     ('SPIEL, SPORT & FREIZEIT', 'Spiel, Sport & Freizeit'),
     ('HAUSHALTSINVENTAR', 'Haushaltsinventar'),
     ('TRANSPORTMITTEL', 'Transportmittel'),
     ('BÜROARTIKEL', 'Büroartikel'),
     ('ELEKTRONIK & TECHNIK', 'Elektronik & Technik'),
     ('VERANSTALTUNGSEQUIPMENT', 'Veranstaltungsequipment'),
     ('RÄUMLICHKEITEN', 'Räumlichkeiten'),
     ('WERKZEUGE', 'Werkzeuge'),
     )
    category = models.CharField(choices=CATEGORY_CHOICES,
                        max_length=50)
    startDate = models.DateTimeField(blank=True, null=True)
    endDate = models.DateTimeField(blank=True, null=True)

    AMBIT_CHOICES = (
        #start Nina
        (0.04500373929, '5 km'),
        (0.09000747858, '10 km'),
        (0.1800149572, '20 km'),
        (0.2700224358, '30 km'),
        #end Nina
    )
    ambit = models.FloatField(choices=AMBIT_CHOICES,
                             default=5,
                             )
    def __str__(self):
        return self.title

# end Meike