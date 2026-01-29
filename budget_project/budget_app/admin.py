from django.contrib import admin
from .models import Wydatek
from .models import Kategoria, Wydatek, Oszczednosci, Przychod


admin.site.register(Kategoria)


@admin.register(Wydatek)
class WydatekAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'kwota', 'data_wydatku', 'notatki')
    list_filter = ('uzytkownik', 'kategoria', 'data_wydatku')
    search_fields = ('nazwa',)

@admin.register(Oszczednosci)
class OszczednosciAdmin(admin.ModelAdmin):
    list_display = ('uzytkownik', 'nazwa', 'kwota_docelowa', 'opis')

@admin.register(Przychod)
class PrzychodAdmin(admin.ModelAdmin):

    list_display = ('uzytkownik', 'nazwa', 'kwota', 'data_przychodu') 
    list_filter = ('uzytkownik', 'data_przychodu')
    search_fields = ('nazwa',)