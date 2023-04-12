from django import forms
from django.forms import ModelForm
from web.models import Driver,Circuit
from datetime import datetime
from django.db.models import Q

class DriverCircuitYear(forms.Form):
    driver = forms.ModelChoiceField(required=True,label="Pick a driver", queryset=Driver.objects.all().filter(~Q(code='nan')).order_by("name"))
    circuit = forms.ModelChoiceField(required=True,label="Pick a circuit", queryset=Circuit.objects.all().order_by("name"))
    year = forms.ChoiceField(choices=( (x,x) for x in range(datetime.now().year,1949,-1)),required=True,label="Pick a year")



class CompareSpeed(forms.Form):
    driver_1 = forms.ModelChoiceField(required=True,label="Pick a driver", queryset=Driver.objects.all().filter(~Q(code='nan')).order_by("name"))
    driver_2 = forms.ModelChoiceField(required=True,label="Pick a driver", queryset=Driver.objects.all().filter(~Q(code='nan')).order_by("name"))
    circuit = forms.ModelChoiceField(required=True,label="Pick a circuit", queryset=Circuit.objects.all().order_by("name"))
    year = forms.ChoiceField(choices=( (x,x) for x in range(datetime.now().year,1949,-1)),required=True,label="Pick a year")

