from django import forms
from .models import Wydatek

class WydatekForm(forms.ModelForm):
    class Meta:
        model = Wydatek
        fields = ['nazwa', 'kwota', 'kategoria', 'data_wydatku', 'uzytkownik', 'opis']
        widgets = {
            'data_wydatku': forms.DateInput(attrs={'type': 'date'}),
        }