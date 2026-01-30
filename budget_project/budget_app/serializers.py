from rest_framework import serializers
from django.utils import timezone
from .models import Kategoria, Wydatek, Oszczednosci, Przychod

class KategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategoria
        fields = '__all__'

class WydatekSerializer(serializers.ModelSerializer):
    # Wyświetla nazwę kategorii zamiast tylko jej ID (opcjonalne, ale czytelne)
    kategoria_nazwa = serializers.ReadOnlyField(source='kategoria.nazwa')

    class Meta:
        model = Wydatek
        fields = '__all__'
        read_only_fields = ['uzytkownik'] # Użytkownik będzie przypisywany automatycznie w widoku

    # Walidacja: Idiotoodporność dla kwoty
    def validate_kwota(self, value):
        if value <= 0:
            raise serializers.ValidationError("Kwota wydatku musi być większa niż zero!")
        return value

    # Walidacja: Data nie może być z dalekiej przyszłości (np. więcej niż rok)
    def validate_data_wydatku(self, value):
        if value.date() > timezone.now().date():
             # Tu możesz zdecydować, czy dopuszczasz daty przyszłe (np. planowane wydatki)
             # Jeśli prowadzący chce "blokady przyszłości", odkomentuj poniższe:
             # raise serializers.ValidationError("Data nie może być z przyszłości!")
             pass
        return value

class PrzychodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Przychod
        fields = '__all__'
        read_only_fields = ['uzytkownik']

    def validate_kwota(self, value):
        if value <= 0:
            raise serializers.ValidationError("Przychód musi być dodatni!")
        return value

class OszczednosciSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oszczednosci
        fields = '__all__'
        read_only_fields = ['uzytkownik']