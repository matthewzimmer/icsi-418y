from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import datetime
from django.core import validators
from django import forms


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
    if len(symbol_names) > 0:
        scrape_results = ScrapeResult.objects.filter(symbol_id__in=symbol_ids)
    else:
        scrape_results = ScrapeResult.objects.all()

    if len(start_date) > 0:
        scrape_results = scrape_results.filter(posted_at__gte=start_date)
    if len(end_date) > 0:
        scrape_results = scrape_results.filter(posted_at__lte=end_date)

    return render(request, 'results.html', {'GET': request.GET, 'scrape_results': scrape_results})


