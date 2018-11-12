from django.contrib import admin
from .models import Symbol, ScrapeRequest, ScrapeResult

admin.site.register(Symbol)
admin.site.register(ScrapeRequest)
admin.site.register(ScrapeResult)
