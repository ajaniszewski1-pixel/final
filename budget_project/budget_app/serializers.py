from rest_framework import serializers
from .models import Transaction  # Importujesz swój model

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'  # Lub lista konkretnych pól ze zdjęcia (kwota, data, opis...)

    # Tutaj dodajemy "Idiotoodporność" 
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Kwota musi być dodatnia!")
        return value