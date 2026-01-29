from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Kategoria(models.Model):
    TYPY = [
        ('staly', 'Wydatek stały'),
        ('zmienny', 'Wydatek zmienny'),
    ]
    nazwa = models.CharField(max_length=100)
    typ = models.CharField(max_length=10, choices=TYPY, default='zmienny')

    def __str__(self):
        return f"{self.nazwa} ({self.get_typ_display()})"

    class Meta:
        verbose_name_plural = "Kategorie"

class Wydatek(models.Model):
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Osoba", null=True, blank=True)
    nazwa = models.CharField(max_length=200)
    kwota = models.DecimalField(max_digits=10, decimal_places=2)
    kategoria = models.ForeignKey(Kategoria, on_delete=models.CASCADE)
    data_wydatku = models.DateTimeField(default=timezone.now)
    opis = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Wydatki"

class Oszczednosci(models.Model):

    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Osoba", null=True, blank=True)
    nazwa = models.CharField(max_length=100)
    kwota_docelowa = models.DecimalField(max_digits=10, decimal_places=2)
    opis = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Oszczędności"

class Przychod(models.Model):
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Osoba")
    nazwa = models.CharField(max_length=100, verbose_name="Źródło przychodu")
    kwota = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Kwota")
    data_przychodu = models.DateField(auto_now_add=True)
    class Meta:
        verbose_name = "Przychód"
        verbose_name_plural = "Przychody"
    def __str__(self):
        return f"{self.nazwa} - {self.kwota} zł"

    class Meta:
        verbose_name_plural = "Przychody"


    