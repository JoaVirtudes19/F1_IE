from django import forms
from django.forms import ModelForm
from web.models import Driver,Circuit
from datetime import datetime
from django.db.models import Q

class DriverCircuitYear(forms.Form):
    driver = forms.ModelChoiceField(required=True,label="Seleccione un piloto", queryset=Driver.objects.all().filter(~Q(code='nan')).order_by("name"))
    circuit = forms.ModelChoiceField(required=True,label="Seleccione un circuito", queryset=Circuit.objects.all().order_by("name"))
    year = forms.ChoiceField(choices=( (x,x) for x in range(datetime.now().year,1949,-1)),required=True,label="Seleccione un año")
