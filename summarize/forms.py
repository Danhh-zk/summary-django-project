from django import forms
from .models import Submission

class sumForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['title', 'field', 'paper']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'field': forms.TextInput(attrs={'class': 'form-control'}),
            'paper': forms.FileInput(attrs={'class': 'form-control'})
        }
