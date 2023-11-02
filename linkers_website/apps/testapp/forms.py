from django import forms
from django.forms import ModelForm #add data to database, and they are models
from .models import YourModel

class LinkerForm(ModelForm):
    class Meta:
        model=YourModel
        fields = '__all__'
        labels={
            'aasequence':'',
            'length':'',
            'Origin':'',
        }

        widgets={
            'aasequence':forms.TextInput(attrs={'class':'form-control','placeholder':'Amino Acids Sequence'}),
            'length':forms.NumberInput(attrs={'class':'form-control','placeholder':'Length'}),
            'Origin':forms.TextInput(attrs={'class':'form-control','placeholder':'Description'}),
        }

    