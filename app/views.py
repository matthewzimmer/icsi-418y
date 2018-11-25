import csv

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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
    if len(symbols) > 0:
        scrape_results = ScrapeResult.objects.filter(symbol_id__in=symbol_ids)
    else:
        scrape_results = ScrapeResult.objects.all()
    scrape_results = scrape_results.order_by('-posted_at')

    # CSV
    if request.GET.get('format') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="results.csv"'

        writer = csv.writer(response)
        writer.writerow(['Posted At', 'Symbol', 'Headline', 'Article'])
        for result in scrape_results:
            writer.writerow([result.posted_at, result.symbol.name, result.headline, result.article])

    # PDF
    elif request.GET.get('format') == 'pdf':
        response = HttpResponse("Coming Soon")

    # HTML
    else:
        response = render(request, 'results.html', {'scrape_results': scrape_results})
    return response
