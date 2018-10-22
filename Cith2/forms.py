from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from Cith2.models import Resource, Category, IntervalConstraint, Account, Query, Plz


class LoginForm(forms.Form):
    username = forms.CharField(label='Nutzername', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'username', 'placeholder': 'Ihr Nutzername'}))
    password = forms.CharField(label='Passwort', max_length=30, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'example-password-input', 'placeholder': 'Ihr Passwort'}))


class RegisterForm(forms.Form):
    mail = forms.CharField(label='E-Mail Adresse', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'username', 'placeholder': 'Ihre E-Mail Adresse'}))
    password = forms.CharField(label='Passwort', max_length=30, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'example-password-input', 'placeholder': 'Ihr Passwort'}))


class RemindPasswordForm(forms.Form):
    mail = forms.CharField(label='E-Mail Adresse', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'username', 'placeholder': 'Ihre E-Mail Adresse'}))


class IntervalModelForm(ModelForm):
    class Meta:
        model = IntervalConstraint
        fields = ['resourceId', 'startDate', 'endDate', 'available']


class ResourceModelForm(ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'locationLat', 'locationLong', 'imagePath', 'categoryId', 'costs', 'type', 'deposit']


class AccountModelForm(ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'locationLat', 'locationLong', 'imagePath', 'categoryId', 'costs', 'type', 'deposit']


class NewResourceForm(ResourceModelForm):

    startDate = forms.CharField(max_length=33, required=False)
    endDate = forms.CharField(required=False)

    class Meta(ResourceModelForm.Meta):

        newFields = ['startDate', 'endDate']
        fields = ResourceModelForm.Meta.fields + newFields

        def __init__(self, *args, **kwargs):
            super(ResourceModelForm, self).__init__(*args, **kwargs)
            self.fields['categoryId'].empty_label = None
            # following line needed to refresh widget copy of choice list
            self.fields['categoryId'].widget.choices = self.fields['categoryId'].choices


        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',  'placeholder': 'Was möchten Sie anbieten?'}),
            'description': forms.Textarea(attrs={'class': 'form-control',  'id': 'exampleTextarea',
                                    'rows': '6', 'aria-describedby': 'descHelp'}),
            'locationLat': forms.HiddenInput(attrs={'id': 'latInput'}),
            'locationLong': forms.HiddenInput(attrs={'id': 'longInput'}),
            'imagePath': forms.ClearableFileInput(attrs={'class': "form-control-file", 'id': "exampleInputFile", 'accept': "image/*",
                                  'aria-describedby': "fileHelp"}),
            'type': forms.RadioSelect(attrs={'class': 'noMarkers'}),
            'costs': forms.TextInput(attrs={'class': 'form-control'}),
            'deposit': forms.TextInput(attrs={'class': 'form-control'}),
            'startDate': forms.HiddenInput(attrs={'id': 'startDateInput'}),
            'endDate': forms.HiddenInput(attrs={'id': 'endDateInput'}),
            'categoryId': forms.Select(attrs={'class': 'col-6'})
        }


class SafeOffer(ModelForm):
    class Meta:
        model = Query
        fields= ['category','title','latitude','longitude', 'ambit','startDate', 'endDate']

        def __init__(self, *args, **kwargs):
            super(ModelForm, self).__init__(*args, **kwargs)
            self.fields['category'].empty_label = None
            # following line needed to refresh widget copy of choice list
            self.fields['category'].widget.choices = self.fields['category'].choices

        widgets = {
            'category': forms.Select(attrs={'class': 'col-6'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.HiddenInput(attrs={'id': 'latInput'}),
            'longitude': forms.HiddenInput(attrs={'id': 'longInput'}),
            'ambit': forms.Select(attrs={'class': 'form-control'}),
            'startDate': forms.HiddenInput(attrs={'id': 'startDateInput'}),
            'endDate': forms.HiddenInput(attrs={'id': 'endDateInput'}),
        }


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control is_valid'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),

        }


class UserProfileForm(ModelForm):
    plz = forms.ModelChoiceField(queryset=Plz.objects.all())
    plz.widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = Account
        exclude = ['user']
        widgets = {
            'organisationName': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'imagePath': forms.ClearableFileInput(attrs={'class': "form-control-file", 'accept': "image/*"}),
        }