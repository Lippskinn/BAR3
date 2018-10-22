from Cith2.forms import UserForm, UserProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
import urllib, json
from urllib.request import urlopen, Request
from Cith2.models import Plz


def register(request):
    # if this is a POST request we need to process the form data
    return render(request, 'pick_registration_type.html')


def start_registration(request, organisation):
    uf = UserForm()
    upf = UserProfileForm()
    plzs = Plz.objects.all()
    return render(request, 'register.html',
                  {'userform': uf, 'accountform': upf, 'plzs': plzs, 'organisation': organisation})

#start Meike
def process_registration(request, organisation):
    if request.method == "POST":
        captcha = check_captcha(request)
        if captcha['success']:

            newUser = create_user(request, organisation)
            if newUser == None:
                userForm = UserForm(request.POST)
                userProfileForm = UserProfileForm(request.POST)
                plzs = Plz.objects.all()
                return render(request, 'register.html',
                              {'userform': userForm, 'accountform': userProfileForm, 'plzs': plzs,
                               'organisation': organisation, 'mode': 'Registrieren'})
            else:
                login(request, newUser)
                return redirect('/login/')
#end Meike

        else:
            uf = UserForm()
            upf = UserProfileForm()
            plzs = Plz.objects.all()
            return render(request, 'register.html',
                          {'userform': uf, 'accountform': upf, 'plzs': plzs, 'organisation': organisation,
                           'failedCaptchaMsg': 'Captcha ist nicht korrekt'})


def check_captcha(request):
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
    return result

#start Meike
def create_user(request, organisation):
    userForm = UserForm(request.POST)
    userProfileForm = UserProfileForm(request.POST)
    if not userForm.is_valid() or not userProfileForm.is_valid():
        return None

    newUser = userForm.save(commit=False)
    password = make_password(request.POST['password'])
    newUser.password = password
    newUser.save()
    newUserProfile = userProfileForm.save(commit=False)
    newUserProfile.user = newUser
    newUserProfile.isOrganisation = organisation
    newUserProfile.save()
    return newUser
#end Meike