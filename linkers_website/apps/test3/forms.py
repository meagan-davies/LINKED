from django import forms
from django.forms import ModelForm #add data to database, and they are models
from .models import Linker,flexibility

class LinkerForm(ModelForm):
    class Meta:
        model=Linker
        fields = ['aasequence','length','pdb_id','Source','Reference']
        labels={
            'aasequence':'Sequence',
            'length':'Length',
            'pdb_id':'PDB ID (if applicable)',
            'Source':'Description',
            'Reference':'Reference Website',
        }

        widgets={
            'aasequence':forms.TextInput(attrs={'class':'form-control','placeholder':'Amino Acids Sequence'}),
            'length':forms.NumberInput(attrs={'class':'form-control','placeholder':'Length'}),
            'pdb_id':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter NA if not applicable'}),
            'Source':forms.Textarea(attrs={'class':'form-control','placeholder':'Please provide a detailed description on the source of the linker'}),
            'Reference':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter NA if not applicable'}),
        }


class FlexForm(ModelForm):
    class Meta:
        model=flexibility
        fields=['type']

        labels={
            'type':'Flexibility'
        }

        widgets={
            'type': forms.Select(choices=[('flexible', 'flexible'), ('rigid', 'rigid'), ('context_dependent', 'context dependent (can be either flexible or rigid)'),('unknown','unknown')], attrs={'class': 'form-control'}),
        }

   

