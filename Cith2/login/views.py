from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from Cith2.forms import RemindPasswordForm
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from Cith2.forms import LoginForm, RemindPasswordForm
from Cith2.models import User


def remind_password(request):
    # if this is a POST request we process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RemindPasswordForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data
            return HttpResponseRedirect('/profil')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = RemindPasswordForm()

    return render(request, 'remind.html', {'form': form})


def loginview(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            print(form.cleaned_data['password'])
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.filter(username=username).first()
            # compare the password hash
            authenticate = check_password(password, user.password)
            if authenticate:
                login(request, user)
                return redirect('/profil/merkliste')

        return render(request, 'login.html', {'form': form, 'failedLoginMsg': "Nutzername oder Passwort ist nicht korrekt"})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})