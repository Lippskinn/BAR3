"""
Modulbeschreibung
"""

# start Nina
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from datetime import datetime
from Cith2.forms import SafeOffer
from django.shortcuts import render, redirect

from Cith2.models import Resource, Plz
from Cith2.register.views import check_captcha
@csrf_exempt

def getOffers(request):
    """
    Liefert die Resourcen aus der Datenbank zurück, die zu den Filtereingaben des Nutzers passen.
    """

    # Kontrolle der Input-Daten
    data = request.POST
    global currentFilters
    currentFilters = data
    empty = ''

    # Aufbereitung Datum
    if request.POST['startDate'] is not empty and request.POST['endDate'] is not empty:
        startDate = datetime.strptime(request.POST['startDate'],'%Y-%m-%d')
        endDate= datetime.strptime(request.POST['endDate'],'%Y-%m-%d')

    # Daten für Umkreisberechnung (eigentlich Rechteck)
    if request.POST['lat'] is not empty and request.POST['lat'] is not empty and request.POST['umkreis'] is not empty:
        ambit = float(request.POST['umkreis'])*0.009000747858346241
        longminus = float(request.POST['lng'])-ambit
        latminus = float(request.POST['lat'])-ambit
        longplus = float(request.POST['lng'])+ambit
        latplus = float(request.POST['lat'])+ambit

    if request.POST['keywords'] is not empty:
        if request.POST['lat'] is not empty and request.POST['lat'] is not empty and request.POST['umkreis'] is not empty:
            if request.POST['startDate'] is not empty and request.POST['endDate'] is not empty:
                # keyword, Location und Datum wurde angegeben
                # nicht verfügbarer Zeitraum
                false = Resource.objects.filter(
                    title__contains=request.POST['keywords']).exclude(
                    constraints__available=False,
                    constraints__startDate__lte=startDate,
                    constraints__endDate__gte=endDate).filter(
                    locationLong__gt=longminus).filter(
                    locationLat__gt=latminus).filter(
                    locationLong__lt=longplus).filter(
                    locationLat__lt=latplus
                )
                # Verfügbarer Zeitraum
                true = Resource.objects.filter(
                    title__contains=request.POST['keywords']).filter(
                    constraints__available=True,
                    constraints__startDate__lte=endDate,
                    constraints__endDate__gte=endDate).filter(
                    locationLong__gt=longminus).filter(
                    locationLat__gt=latminus).filter(
                    locationLong__lt=longplus).filter(
                    locationLat__lt=latplus
                )

                success = true & false

            else:
                # keyword & location angegeben
                success = Resource.objects.filter(
                    title__contains=request.POST['keywords']).filter(
                    locationLong__gt=longminus).filter(
                    locationLat__gt=latminus).filter(
                    locationLong__lt=longplus).filter(
                    locationLat__lt=latplus
                )
        else:
            if request.POST['startDate'] is not empty and request.POST['endDate'] is not empty:
                # keyword & Datum wurde angegeben
                false = Resource.objects.filter(
                    title__contains=request.POST['keywords']).exclude(
                    constraints__available=False,
                    constraints__startDate__lte=startDate,
                    constraints__endDate__gte=endDate)

                true = Resource.objects.filter(
                    title__contains=request.POST['keywords']).filter(
                    constraints__available=True,
                    constraints__startDate__lte=endDate,
                    constraints__endDate__gte=endDate)

                success = true & false
            else:
                # nur keyword
                success = Resource.objects.filter(
                    title__contains=request.POST['keywords'])
    else:
        if request.POST['lat'] is not empty and request.POST['lat'] is not empty and request.POST['umkreis'] is not empty:
            if request.POST['startDate'] is not empty and request.POST['endDate'] is not empty:
                # Location & Datum
                false = Resource.objects.exclude(
                    constraints__available=False,
                    constraints__startDate__lte=startDate,
                    constraints__endDate__gte=endDate).filter(
                    locationLong__gt=longminus).filter(
                    locationLat__gt=latminus).filter(
                    locationLong__lt=longplus).filter(
                    locationLat__lt=latplus
                )
                true = Resource.objects.filter(
                    constraints__available=True,
                    constraints__startDate__lte=endDate,
                    constraints__endDate__gte=endDate).filter(
                    locationLong__gt=longminus).filter(
                    locationLat__gt=latminus).filter(
                    locationLong__lt=longplus).filter(
                    locationLat__lt=latplus
                )

                success = true & false
            else:
                # nur Location wurde angegeben
                success = Resource.objects.filter(
                    locationLong__gt=longminus).filter(
                    locationLat__gt=latminus).filter(
                    locationLong__lt=longplus).filter(
                    locationLat__lt=latplus
                )
        else:
            if request.POST['startDate'] is not empty and request.POST['endDate'] is not empty:
                # nur Datum
                false = Resource.objects.exclude(
                    constraints__available=False,
                    constraints__startDate__lte=startDate,
                    constraints__endDate__gte=endDate
                )
                true = Resource.objects.filter(
                    constraints__available=True,
                    constraints__startDate__lte=endDate,
                    constraints__endDate__gte=endDate)

                success = true & false
            else:
                if request.POST['categories'] is not empty:
                    # nur Kategorie angegeben
                    success = Resource.objects.filter(categoryId=request.POST['categories'])
                else:
                    # gar keine Angaben
                    success = Resource.objects.all()

    # QuerySet into JSON-Object
    response = serializers.serialize("json", success)

    return JsonResponse(response, safe=False)
# end Nina

# start Nina

def addQuery(request):
    """ Speichert eine Suchanfrage in die Datenbank, wenn Nutzer eine Ressource im System nicht gefunden hat."""
    plzs = Plz.objects.all()
    empty =''
    if request.user.is_authenticated:
        if request.method == "POST":
           form = SafeOffer(request.POST, request.FILES)
           if form.is_valid():
               result = check_captcha(request)
               logger.info(result)
               if result['success']:
                   form = SafeOffer()
                   query = form.save(commit=False)
                   query.title = request.POST['title']
                   query.category = request.POST['category']
                   query.longitude = request.POST['longitude']
                   query.latitude = request.POST['latitude']
                   query.ambit = request.POST['ambit']
                   query.userId = request.user

                   if request.POST['startDate'] is not empty and request.POST['endDate'] is not empty:
                        query.endDate = request.POST['endDate']
                        query.startDate = request.POST['startDate']

                   query.save()
                   return redirect('/profil/suchanfragen/')

               else:
                    return render(request, "query-new.html", {'form': form, 'plzs': plzs, 'failedCaptchaMsg': 'Captcha ist nicht korrekt'})
           else:
               return render(request, "query-new.html", {'form': form})
        else:
            form = SafeOffer()
            return render(request, "query-new.html", {'form': form, 'plzs': plzs, 'preFill': currentFilters})
    else:
        return redirect('/login/')

logger = logging.getLogger(__name__)
# end Nina

# start Nina

@csrf_exempt
def getSimOffer(request):
    """Liefert ähnliche Ressourcen zurück. Diese Ressourcen passen nicht exakt auf die Eingaben des Users."""
    data = request.POST
    empty = ''

    # Ähnlichkeit über Kategorie
    cat = ''
    if request.POST['categories'] is not empty:
        cat = Resource.objects.filter(categoryId__exact=request.POST['categories'])
    # Ähnlichkeit über Title (alle Zeiträume und alle Orte)
    tit = ''
    if request.POST['keywords'] is not empty:
            tit = Resource.objects.filter(title__contains=request.POST['keywords'])

    success = cat if cat is not empty else tit


    # QuerySet into JSON-Object
    response = serializers.serialize("json", success)

    return JsonResponse(response, safe=False)

# end Nina