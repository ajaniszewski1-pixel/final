from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib.auth.models import User
from .models import Wydatek, Przychod, Kategoria
from .forms import WydatekForm
from datetime import date

def dashboard(request):
    # 1. OBSŁUGA FORMULARZA (ZAPISYWANIE)
    if request.method == "POST":
        form = WydatekForm(request.POST)
        if form.is_valid():
            wydatek = form.save(commit=False)
            # Ręcznie przypisujemy osobę wybraną z listy rozwijanej w arkuszu
            uzytkownik_id = request.POST.get('uzytkownik')
            if uzytkownik_id:
                wydatek.uzytkownik_id = uzytkownik_id
            else:
                wydatek.uzytkownik = request.user
            
            wydatek.save()
            return redirect('dashboard')
    else:
        form = WydatekForm()

    # 2. POBIERANIE DANYCH (Zmienne zdefiniowane tutaj są dostępne dla contextu)
    wszystkie_wydatki = Wydatek.objects.all().order_by('-data_wydatku')
    przychody = Przychod.objects.all()
    kategorie = Kategoria.objects.all()
    uzytkownicy = User.objects.all()

    # 3. PODZIAŁ WYDATKÓW NA STAŁE I ZMIENNE
    # Filtrujemy bazując na polu 'typ' w modelu Kategoria
    wydatki_stale = wszystkie_wydatki.filter(kategoria__typ__icontains='stal') 
    wydatki_zmienne = wszystkie_wydatki.filter(kategoria__typ__icontains='zmienn')

    # 4. OBLICZENIA DO STATYSTYK I WYKRESU
    suma_przychodow = przychody.aggregate(total=Sum('kwota'))['total'] or 0
    suma_wydatkow = wszystkie_wydatki.aggregate(total=Sum('kwota'))['total'] or 0
    
    # Dodatkowe sumy dla nagłówków tabel (opcjonalnie)
    suma_stale = wydatki_stale.aggregate(total=Sum('kwota'))['total'] or 0
    suma_zmienne = wydatki_zmienne.aggregate(total=Sum('kwota'))['total'] or 0
    
    bilans = suma_przychodow - suma_wydatkow

    # 5. PRZEKAZANIE DANYCH DO SZABLONU
    context = {
        'suma_stale': suma_stale,
        'suma_zmienne': suma_zmienne,
        'suma_oszczednosci': 0,
        'form': form,
        'wydatki_stale': wydatki_stale,
        'wydatki_zmienne': wydatki_zmienne,
        'przychody': przychody,
        'kategorie': kategorie,
        'uzytkownicy': uzytkownicy,
        'suma_przychodow': suma_przychodow,
        'suma_wydatkow': suma_wydatkow,
        'suma_stale': suma_stale,
        'suma_zmienne': suma_zmienne,
        'bilans': bilans,
        'dzisiejsza_data': date.today().strftime('%Y-%m-%d'),
    }
    
    return render(request, 'budget_app/dashboard.html', context)