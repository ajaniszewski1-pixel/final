from django.contrib import admin
from .models import Kategoria, Wydatek, Oszczednosci, Przychod

# Rejestracja prostego modelu
admin.site.register(Kategoria)

# Rejestracja z dodatkowymi opcjami wyświetlania
@admin.register(Wydatek)
class WydatekAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'kwota', 'data_wydatku', 'uzytkownik')
    list_filter = ('uzytkownik', 'kategoria', 'data_wydatku')
    search_fields = ('nazwa',)

@admin.register(Oszczednosci)
class OszczednosciAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'uzytkownik', 'kwota_docelowa')
    search_fields = ('nazwa',)

@admin.register(Przychod)
class PrzychodAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'uzytkownik', 'kwota', 'data_przychodu') 
    list_filter = ('uzytkownik', 'data_przychodu')
    search_fields = ('nazwa',)