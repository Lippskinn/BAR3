import urllib, json
from urllib.request import Request, urlopen
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from Cith2.forms import UserProfileForm, UserForm, SafeOffer
from django.core import serializers
# start Nina
from django.contrib.auth.hashers import make_password
# end Nina

#start Alina
from django.contrib.auth.models import User
from Cith2.models import Account, Resource, Watchlist, IntervalConstraint, Query, Plz
from django.contrib.auth.decorators import login_required

# Adds item to watchlist.
@login_required(login_url='/login/')
def watch(request, resource_id):
    """
    The function watch() puts a selected resource into the currently logged in the watchlist model. I.e. the resource's id and the user's id will be written in the watchlist model.
    """
    # writes the logged in user's ID and the resourceId into class Watchlist
    res = Resource.objects.get(pk=resource_id)
    user = request.user
    Watchlist.objects.create(userId = user, resourceId =res)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

# Removes item from watchlist.
@login_required(login_url='/login/')
def unwatch(request, resource_id):
    """
    # writes the logged in user's ID and the resourceId into watchlist model
    """
    res = Resource.objects.get(pk=resource_id)
    user = request.user
    delete_obj = Watchlist.objects.get(userId = user, resourceId =res)
    delete_obj.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def profile(request, section):
    """defines variables to be used in templates/cith2/profile.html """
    username = User.username
    first_name =User.first_name
    last_name = User.last_name
    email = User.email
    address = Account.address
    userAccount = Account.objects.get(user=request.user)
    #in my_watchlist live those resources that the logged in user saved for later
    my_watchlist = Watchlist.objects.filter(userId=request.user.id).prefetch_related('resourceId')
    #in my_resources live the resources which the logged in user published herself/himself
    my_resources = Resource.objects.filter(userId=request.user.id).prefetch_related('constraints')
    #in my_queries live the queries which the user saved in case a matching resource is added later
    my_queries = Query.objects.filter(userId=request.user)

    context = {'active_section': section, 'account': userAccount, 'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email, 'address': address, 'my_watchlist': my_watchlist, 'my_res': my_resources, 'my_queries':my_queries}

    return render(request, 'profile.html', context)
#end Alina

def editAvailability(request, res_id):
    """Bearbeiten der Verfügbarkeit einer Resource"""
    userAccount = Account.objects.get(user=request.user)
    res = Resource.objects.filter(id=res_id).first()
    my_watchlist = Watchlist.objects.filter(userId=request.user.id).prefetch_related('resourceId')
    my_resources = Resource.objects.filter(userId=request.user.id).prefetch_related('constraints')
    raw = IntervalConstraint.objects.filter(resourceId=res_id)
    intervals = serializers.serialize("json", raw)
    context = {'my_watchlist': my_watchlist, 'res': res, 'account': userAccount, 'my_res': my_resources, 'active_section': 'angebote', "intervals": intervals}
    return render(request, 'profile.html', context)

# start Nina

@login_required(login_url='/login/')
def editProfile(request):
    """Bearbeitung eines bestehenden Profils"""
    userId = request.user.id
    if request.method == "POST":
        instance = get_object_or_404(User, id=userId)
        account = get_object_or_404(Account, user_id=userId)
        accountform = UserProfileForm(request.POST or None, instance=account)
        userform = UserForm(request.POST or None, instance=instance)
        if accountform.is_valid() and userform.is_valid():
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
                userform.save()
                accountform.address = request.POST['address']
                accountform.save()
                account.imagePath = "static/images/avatars/" + request.POST['imagePath']
                account.save()
                instance.account = account
                instance.password = make_password(request.POST['password'])
                instance.save()
                return redirect('/login/')
            else:
                return render(request, "register.html", {'accountform': accountform, 'userform': userform, 'failedCaptchaMsg': 'Captcha ist nicht korrekt'})
        return render(request, 'register.html', {'accountform': accountform, 'userform': userform})
    else:
        prevdataUser = request.user
        prevdataAcc = request.user.account
        plzs = Plz.objects.all()
        organisation = request.user.account.isOrganisation
        uf = UserForm(instance=prevdataUser)
        upf = UserProfileForm(instance=prevdataAcc)
        return render(request, 'register.html',  {'mode': 'Profil bearbeiten', 'userform': uf, 'accountform': upf, 'plzs': plzs, 'organisation': organisation})
# end Nina

#start Alina
def deleteProfile(request):
    """
    deletes a profile
    """
    user = request.user
    user.delete()
    return redirect('/registrieren/')


def deleteQuery(request, query_id):
    """
    deletes a saved query

    """
    user = request.user
    query = Query.objects.get(pk=query_id)
    if query.userId == user:
        delete_query = Query.objects.get(id = query.id)
        delete_query.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
#end Alina

# start Nina

def editQuery(request, queryId):
    """Bearbeitung einer bestehenden Suchanfrage """
    if request.user == Query.objects.get(id=queryId).userId:
        if request.method == "POST":
            instance = get_object_or_404(Query, id=queryId)
            form = SafeOffer(request.POST or None, instance=instance)
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
                    instance.save()

                    return redirect('/profil/suchanfragen/')
                else:
                    return render(request, "query-new.html", {'form': form, 'failedCaptchaMsg': 'Captcha ist nicht korrekt'})
            return render(request, 'query-new.html', {'form': form})
        else:
            prevdata = Query.objects.get(id=queryId)
            form = SafeOffer(instance=prevdata)
            plzs = Plz.objects.all()
            return render(request, "query-new.html", {'form': form, 'plzs': plzs, 'mode': 'Suchanfrage bearbeiten', 'res': prevdata})
    else:
        return redirect('/profil/suchanfragen/')
# end Nina