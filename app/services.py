import datetime
import time

from django.db import transaction
from django.utils import timezone

from app.models import ScrapeResult, Symbol


class Service:
    @classmethod
    def execute(cls, **args):
        instance = cls(**args)
        with transaction.atomic():
            instance.process()
        return instance

    def process(self):
        raise NotImplementedError()


class AcquireScrapeResults(Service):
    def __init__(self, scrape_request):
        self.scrape_request = scrape_request
        self.scrape_results = []

    def process(self):
        time.sleep(5)
        self.scrape_results.append({
            'symbol': 'GE',
            'headline': 'A nice headline.',
            'posted_at': timezone.datetime(2018, 11, 26, 12, 0, 0),
            'article': 'A fulfilling article.',
        })


class PersistScrapeResults(Service):
    def __init__(self, scrape_request, scrape_results):
        self.scrape_request = scrape_request
        self.scrape_results = scrape_results
        self.created_results = []
        self.updated_results = []

    def process(self):
        for result in self.scrape_results:
            # Look for existing scrape result based on uniqueness (what is that?)
            scrape_result = ScrapeResult.objects.filter(
                symbol=Symbol.objects.get_or_create(name=result['symbol'])[0],
                headline=result['headline'],
                posted_at=result['posted_at'],
            ).first()
            if scrape_result is None:
                scrape_result = ScrapeResult.objects.create(
                    symbol=Symbol.objects.get_or_create(name=result['symbol'])[0],
                    headline=result['headline'],
                    posted_at=result['posted_at'],
                    scrape_request=self.scrape_request,
                )
            # Update the ScrapeResult
            scrape_result.article = result['article']
            scrape_result.save()
