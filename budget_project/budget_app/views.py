from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from datetime import date

# Importy dla API (Django REST Framework)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Wydatek, Przychod, Kategoria, Oszczednosci 
from .forms import WydatekForm

# --- 1. GŁÓWNY WIDOK DASHBOARD ---
@login_required
def dashboard(request):
    # OBSŁUGA FORMULARZA (Tworzenie - CRUD: Create)
    if request.method == "POST":
        form = WydatekForm(request.POST)
        if form.is_valid():
            wydatek = form.save(commit=False)
            uzytkownik_id = request.POST.get('uzytkownik')
            
            # Admin może przypisać kogoś innego, User tylko siebie
            if request.user.is_superuser and uzytkownik_id:
                wydatek.uzytkownik_id = uzytkownik_id
            else:
                wydatek.uzytkownik = request.user
            
            wydatek.save()
            return redirect('dashboard')
    else:
        form = WydatekForm()

    # POBIERANIE DANYCH (Odczyt - CRUD: Read)
    if request.user.is_superuser:
        wszystkie_wydatki = Wydatek.objects.all().order_by('-data_wydatku')
        oszczednosci = Oszczednosci.objects.all()
        przychody = Przychod.objects.all()
    else:
        # Widok własny + profil 'Wszyscy'
        wszystkie_wydatki = Wydatek.objects.filter(
            Q(uzytkownik=request.user) | Q(uzytkownik__username='Wszyscy')
        ).order_by('-data_wydatku')
        
        oszczednosci = Oszczednosci.objects.filter(
            Q(uzytkownik=request.user) | Q(uzytkownik__username='Wszyscy')
        )
        przychody = Przychod.objects.filter(uzytkownik=request.user)

    kategorie = Kategoria.objects.all()
    uzytkownicy = User.objects.all()

    # PODZIAŁ I OBLICZENIA
    wydatki_stale = wszystkie_wydatki.filter(kategoria__typ__icontains='stal') 
    wydatki_zmienne = wszystkie_wydatki.filter(kategoria__typ__icontains='zmienn')

    suma_przychodow = przychody.aggregate(total=Sum('kwota'))['total'] or 0
    suma_wydatkow = wszystkie_wydatki.aggregate(total=Sum('kwota'))['total'] or 0
    suma_stale = wydatki_stale.aggregate(total=Sum('kwota'))['total'] or 0
    suma_zmienne = wydatki_zmienne.aggregate(total=Sum('kwota'))['total'] or 0
    suma_oszczednosci = oszczednosci.aggregate(total=Sum('kwota_docelowa'))['total'] or 0
    
    bilans = suma_przychodow - suma_wydatkow

    context = {
        'form': form,
        'wszystkie_wydatki': wszystkie_wydatki,
        'wydatki_stale': wydatki_stale,
        'wydatki_zmienne': wydatki_zmienne,
        'oszczednosci': oszczednosci,
        'przychody': przychody,
        'kategorie': kategorie,
        'uzytkownicy': uzytkownicy,
        'suma_przychodow': suma_przychodow,
        'suma_wydatkow': suma_wydatkow,
        'suma_stale': suma_stale,
        'suma_zmienne': suma_zmienne,
        'suma_oszczednosci': suma_oszczednosci,
        'bilans': bilans,
        'dzisiejsza_data': date.today().strftime('%Y-%m-%d'),
    }
    return render(request, 'budget_app/dashboard.html', context)

# --- 2. DODATKOWY ELEMENT CRUD: USUWANIE ---
@login_required
@require_POST
def usun_wydatek(request, pk):
    # Zabezpieczenie: tylko właściciel lub admin może usunąć
    if request.user.is_superuser:
        wydatek = get_object_or_404(Wydatek, pk=pk)
    else:
        wydatek = get_object_or_404(Wydatek, pk=pk, uzytkownik=request.user)
    
    wydatek.delete()
    return redirect('dashboard')

# --- 3. ENDPOINTY API (POZA CRUD) ---

class BudgetSummaryAPI(APIView):
    """Zestawienie miesięczne: suma przychodów, wydatków i bilans"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_superuser:
            wszystkie = Wydatek.objects.all()
            przychody_sum = Przychod.objects.aggregate(total=Sum('kwota'))['total'] or 0
        else:
            wszystkie = Wydatek.objects.filter(Q(uzytkownik=request.user) | Q(uzytkownik__username='Wszyscy'))
            przychody_sum = Przychod.objects.filter(uzytkownik=request.user).aggregate(total=Sum('kwota'))['total'] or 0
            
        wydatki_sum = wszystkie.aggregate(total=Sum('kwota'))['total'] or 0
        
        return Response({
            "suma_przychodow": float(przychody_sum),
            "suma_wydatkow": float(wydatki_sum),
            "bilans": float(przychody_sum - wydatki_sum)
        })

class BudgetTrendsAPI(APIView):
    """Procentowy udział kategorii w wydatkach (do wykresu kołowego)"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_superuser:
            wszystkie = Wydatek.objects.all()
        else:
            wszystkie = Wydatek.objects.filter(Q(uzytkownik=request.user) | Q(uzytkownik__username='Wszyscy'))
            
        suma_total = wszystkie.aggregate(total=Sum('kwota'))['total'] or 0
        
        if suma_total == 0:
            return Response([])

        # Grupowanie po nazwie kategorii
        dane = (
            wszystkie.values('kategoria__nazwa')
            .annotate(suma=Sum('kwota'))
            .order_by('-suma')
        )
        
        trends = [
            {
                "kategoria": item['kategoria__nazwa'],
                "procent": round((item['suma'] / suma_total) * 100, 2),
                "kwota": float(item['suma'])
            } for item in dane
        ]
        
        return Response(trends)