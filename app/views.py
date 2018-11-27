import csv
import io
import random

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Table, Paragraph, TableStyle, SimpleDocTemplate

from app.models import Symbol, ScrapeResult, ScrapeRequest
from app.services import AcquireScrapeResults, PersistScrapeResults


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
def acquire(request):
    # Look for an existing ScrapeRequest object for the current user
    # with a NULL scraped_at.
    scrape_request = ScrapeRequest.objects.filter(
        user=request.user,
        scraped_at=None
    ).first()
    # If not found, create a new ScrapeRequest object
    # (persist to the database!)
    if scrape_request is None:
        scrape_request = ScrapeRequest.objects.create(user=request.user)
    # Feed the ScrapeRequest object into the Scraper service...and wait till it's done
    service = AcquireScrapeResults.execute(scrape_request=scrape_request)
    # Persist scrape results from Scraper service
    PersistScrapeResults.execute(
        scrape_request=scrape_request,
        scrape_results=service.scrape_results,
    )
    # Return a message to the user informing them of the # of new scrape results available
    if random.random() < .5:
        data = {
            'success': True,
            'message': '{0} new results scraped.'.format(len(service.scrape_results)),
            'error': None
        }
    else:
        data = {
            'success': False,
            'error': 'Failure occurred! Flipped a Tails!'
        }
    return JsonResponse(data)


@login_required
def results(request):
    symbol_names = request.GET.get('symbols')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if len(symbol_names) > 0:
        symbols = Symbol.objects.filter(name__in=symbol_names.split(','))
    else:
        symbols = Symbol.objects.all()
    symbol_ids = symbols.values_list('id', flat=True)

    scrape_requests = ScrapeRequest.objects.filter(user=request.user)
    scrape_request_ids = scrape_requests.values_list('id', flat=True)

    scrape_results = ScrapeResult.objects.filter(scrape_request_id__in=scrape_request_ids)
    scrape_results = scrape_results.filter(symbol_id__in=symbol_ids)
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
        response = results_as_pdf(scrape_results)

    # HTML
    else:
        response = render(request, 'results.html', {'scrape_results': scrape_results})
    return response


def results_as_pdf(scrape_results):
    buff = io.BytesIO()
    doc = SimpleDocTemplate(buff, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30,
                            bottomMargin=18)
    doc.pagesize = landscape(A4)
    elements = []

    data = [
        ['Posted At', 'Symbol', 'Headline', 'Article'],
    ]
    for result in scrape_results:
        data.append([str(result.posted_at), result.symbol.name, result.headline, result.article])

    style = TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                        ('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
                        ('VALIGN', (0, 0), (0, -1), 'CENTER'),
                        ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
                        ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                        ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                        ])

    # Configure style and word wrap
    s = getSampleStyleSheet()
    s.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
    s = s["BodyText"]
    s.wordWrap = 'CJK'
    data2 = [[Paragraph(cell, s) for cell in row] for row in data]
    t = Table(data2)
    t.setStyle(style)

    # Send the data and build the file
    elements.append(t)
    doc.build(elements)

    response = HttpResponse(content_type='application/pdf')
    pdf_name = "results.pdf"
    response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    response.write(buff.getvalue())
    buff.close()
    return response