from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from app.models import Symbol, ScrapeResult


@login_required
def index(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        return redirect('/search')


def login(request):
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/login')


@login_required
def search(request):
    return render(request, 'search.html')


@login_required
def results(request):
    symbol_names = request.GET.get('symbols')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    symbols = Symbol.objects.filter(name__in=symbol_names.split(','))
    symbol_ids = symbols.values_list('id', flat=True)
    scrape_results = ScrapeResult.objects.filter(symbol_id__in=symbol_ids)
    return render(request, 'results.html', {'GET': request.GET, 'scrape_results': scrape_results})
