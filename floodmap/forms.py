from django import forms
from django.forms import ModelForm
from .models import AddMarker


class AddMarkerForm(ModelForm):
    class Meta:
        model = AddMarker
        exclude = ['lat', 'lon']

    def __init__(self, *args, **kwargs):
        super(AddMarkerForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['placeholder'] = field_name.replace("_", " ")
