import urllib, json
from urllib.request import urlopen, Request
from django.shortcuts import render, redirect, get_object_or_404
from Cith2.forms import NewResourceForm, IntervalModelForm
from Cith2.models import Resource, Plz, IntervalConstraint, Watchlist
from django.core import serializers
#start Alina
from django.http import HttpResponseRedirect
#end Alina

def single(request, id):
    # TODO: SINGLE ITEM - Fill context with following data:
    #     - all info on the offer with the given id: name, description,
    #       time constraints (positive and negative), longitude and lattitude,
    #       are contacts available only for logged in users or for everyone? Answer Alina: For logged in users only.
    #     - contacts of the offerer: name, phone number, email, etc.

    myObject = Resource.objects.get(id=id)
    raw = IntervalConstraint.objects.filter(resourceId=id)
    intervals = serializers.serialize("json", raw)
    is_watched = Watchlist.objects.filter(resourceId=id, userId=request.user.id).first()
    other_offers = Resource.objects.filter(userId=myObject.userId).exclude(id=id)
    context = {'obj': myObject, 'intervals': intervals, 'is_watched': is_watched, 'other_offers': other_offers}
    return render(request, 'single.html', context)

# start Nina (edit)

def newOffer(request):
    """Erzeugung und Speicherung einer neuen Ressource"""
    if request.user.is_authenticated:
        if request.method == "POST":
           form = NewResourceForm(request.POST, request.FILES)
           if form.is_valid():
                # Begin reCAPTCHA validation '''
                recaptcha_response = request.POST.get('g-recaptcha-response')
                url = 'https://www.google.com/recaptcha/api/siteverify'
                values = {
                   'secret': '6LfBBF0UAAAAAHKCTHrIESTLwDhnro1q8bDzFmlq',
                   'response': recaptcha_response
                }
                data = urllib.parse.urlencode(values).encode("utf-8")
                req = Request(url, data)
                response = urlopen(req)
                rawResponse = response.read()
                result = json.loads(rawResponse.decode("utf-8"))

                if result['success']:
                    initial_form = form
                    # commit=False means the form doesn't save at this time.
                    # commit defaults to True which means it normally saves.
                    model_instance = initial_form.save(commit=False)
                    model_instance.userId = request.user
                    model_instance.imagePath = request.FILES['imagePath']
                    model_instance.save()

                    if len(form.cleaned_data['startDate']) > 0 and len(form.cleaned_data['endDate']) > 0:
                        interval = IntervalModelForm()
                        emptyInterval = interval.save(commit=False)
                        emptyInterval.resourceId = model_instance
                        emptyInterval.startDate = form.cleaned_data['startDate']
                        emptyInterval.endDate = form.cleaned_data['endDate']
                        emptyInterval.available = True
                        emptyInterval.save()

                    model_instance.save()

                    return redirect('/angebot/%d/'%model_instance.id)
                else:
                    return render(request, "single-new.html", {'form': form, 'failedCaptchaMsg': 'Captcha ist nicht korrekt'})
        else:
            form = NewResourceForm()
            plzs = Plz.objects.all()
            return render(request, "single-new.html", {'form': form, 'plzs': plzs, 'mode': 'Neues Angebot erstellen'})
    else:
        return redirect('/login/')
# end Nina

#start Nina
# Bearbeitung IntervalConstraint oder Ressource mit mehreren IntervalConstraints funktioniert leider nicht 
def editOffer(request, ObjId):
    """Bearbeitet bestehende Ressource"""
    if request.user == Resource.objects.get(id=ObjId).userId:
        if request.method == "POST":
            instance = get_object_or_404(Resource, id=ObjId)
            form = NewResourceForm(request.POST or None, instance=instance)
            if form.is_valid():
                # Begin reCAPTCHA validation '''
                recaptcha_response = request.POST.get('g-recaptcha-response')
                url = 'https://www.google.com/recaptcha/api/siteverify'
                values = {
                    'secret': '6LfBBF0UAAAAAHKCTHrIESTLwDhnro1q8bDzFmlq',
                    'response': recaptcha_response
                }
                data = urllib.parse.urlencode(values).encode("utf-8")
                req = Request(url, data)
                response = urlopen(req)
                rawResponse = response.read()
                result = json.loads(rawResponse.decode("utf-8"))

                if result['success']:
                    form.save()

                    if len(form.cleaned_data['startDate']) > 0 and len(form.cleaned_data['endDate']) > 0:
                        interval = IntervalModelForm()
                        emptyInterval = interval.save(commit=False)
                        emptyInterval.resourceId = instance
                        emptyInterval.startDate = request.POST['startDate']
                        emptyInterval.endDate = request['endDate']
                        emptyInterval.available = True
                        emptyInterval.save()

                    instance.save()
                    if instance.type == "ZU VERSCHENKEN":
                        instance.deposit = None
                        instance.costs = None
                        instance.save()

                    return redirect('/angebot/%d/' % instance.id)
                else:
                    return render(request, "single-new.html",{'form': form, 'failedCaptchaMsg': 'Captcha ist nicht korrekt'})
            return render(request, 'single_new.html', {'form': form})
        else:
            prevdata = Resource.objects.get(id=ObjId)
            form = NewResourceForm(instance=prevdata)
            plzs = Plz.objects.all()
            return render(request, "single-new.html", {'form': form, 'plzs': plzs, 'mode': 'Angebot bearbeiten', 'res': prevdata})
    else:
        return redirect('/profil/angebote/')
#end Nina

#start Alina

def deleteOffer(request, resource_id):
    """deletes an Offer"""
    res = Resource.objects.get(id=resource_id)
    user = request.user
    if res.userId == user:
        delete_res = Resource.objects.get(id=res.id)
        delete_res.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
#end Alina

# start Nina

def addConstraint(request, resource_id, startDate, endDate ):
    """Constraint zu bestimmter Ressource wird angelegt (v.a. wenn Ressource in einem Zeitraum als verliehen markiert wird)."""
    res = Resource.objects.get(id=resource_id)
    user = request.user
    if res.userId == user:
        interval = IntervalModelForm()
        emptyInterval = interval.save(commit=False)
        emptyInterval.resourceId = res
        emptyInterval.startDate = startDate
        emptyInterval.endDate = endDate
        emptyInterval.available = False
        emptyInterval.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def deleteConstraint(request, constraint_id):
    """Löscht einen Zeitraum"""
    intv = IntervalConstraint.objects.get(id=constraint_id)
    user = request.user
    res = Resource.objects.get(id=intv.resourceId.id)
    if res.userId == user:
        delete_intv = IntervalConstraint.objects.get(id=intv.id)
        delete_intv.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
# end Nina