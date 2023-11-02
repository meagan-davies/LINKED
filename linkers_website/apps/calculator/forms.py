from django import forms
from django.forms import ModelForm #add data to database, and they are models
from .models import calc
from django.forms.widgets import Textarea

class CapitalizedTextarea(Textarea):
    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs['oninput'] = 'this.value = this.value.toUpperCase();'
        return attrs
    
class CalcForm(ModelForm):
    class Meta:
        model = calc
        fields = '__all__'
        labels = {
            'sequence': 'Amino Acid Sequence',
        }

        widgets = {
            'sequence': CapitalizedTextarea(attrs={
                'class': 'form-control',
                'placeholder': 'Amino Acids Sequence',
                'id': 'sequence',
            }),
        }

        def clean_sequence(self):
            sequence = self.cleaned_data.get('sequence', '')

            acceptable_letters = ['A', 'C', 'D', 'E','F','G','H','I','K','M','N','P','Q','R','S','T','V','W']

            if not all(letter in acceptable_letters for letter in sequence):
                raise forms.ValidationError('Sequence can only contain A, C, G, or T.')

            return sequence