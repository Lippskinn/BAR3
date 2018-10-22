from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from Cith2.forms import SafeOffer
from Cith2.models import Plz, Category, Resource


def index(request):
    categories = Category.objects.all()
    offers = Resource.objects.all()
    plzs = Plz.objects.all()
    return render(request, 'index.html', {'plzs': plzs, 'categories': categories, 'offers': offers})


def newQuery(request):
    plzs = Plz.objects.all()
    form = SafeOffer()
    return render(request, 'query-new.html', {'form':form, 'plzs': plzs})


