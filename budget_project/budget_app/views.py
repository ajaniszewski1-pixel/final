from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import Wydatek, Oszczednosci, Kategoria, Przychod
from .forms import WydatekForm

def dashboard(request):
    if request.method == "POST":
        form = WydatekForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = WydatekForm()

    wydatki = Wydatek.objects.all().order_by('-data_wydatku')
    przychody = Przychod.objects.all()
    
    suma_przychodow = przychody.aggregate(total=Sum('kwota'))['total'] or 0
    suma_wydatkow = wydatki.aggregate(total=Sum('kwota'))['total'] or 0
    bilans = suma_przychodow - suma_wydatkow
    suma_przychodow = round(float(suma_przychodow), 2)
    suma_wydatkow = round(float(suma_wydatkow), 2)
    bilans = round(suma_przychodow - suma_wydatkow, 2)
    
    # Obliczamy procent wydatków względem przychodów
    if suma_przychodow > 0:
        procent_wydatkow = min(int((suma_wydatkow / suma_przychodow) * 100), 100)
    else:
        procent_wydatkow = 0

    context = {
        'form': form,
        'wydatki': wydatki,
        'przychody': przychody,
        'suma_przychodow': suma_przychodow,
        'suma_wydatkow': suma_wydatkow,
        'bilans': bilans,
        'procent_wydatkow': procent_wydatkow,
    }
    return render(request, 'budget_app/dashboard.html', context)