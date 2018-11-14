from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from app.models import ScrapeRequest, Symbol, ScrapeResult


class SymbolTestCase(TestCase):
    def setUp(self):
        Symbol.objects.create(name="FOO")

    def test_symbol_can_be_created(self):
        symbol = Symbol.objects.get(name="FOO")
        self.assertEqual(symbol.name, "FOO")


class ScrapeRequestTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('user', 'email@test.com', 'mypassword123')
        ScrapeRequest.objects.create(user=self.user)

    def test_scrape_requests_can_be_created(self):
        scrape_request = ScrapeRequest.objects.filter(user=self.user, scraped_at=None).first()
        self.assertIsNotNone(scrape_request)

    def test_scrape_requests_can_be_completed(self):
        scrape_request = ScrapeRequest.objects.filter(user=self.user, scraped_at=None).first()
        scrape_request.scrape_did_complete()
        self.assertIsNotNone(scrape_request.scraped_at)


class ScrapeResultTestCase(TestCase):
    def setUp(self):
        self.symbol_name = 'GE'
        self.headline = "[{0}] Lorem Ipsum".format(self.symbol_name)
        self.article = "Lorem ipsum dolor sit amet, mea debet assueverit repudiandae ex, est no dolor aeterno deserunt. Per et vitae dignissim. Impetus ornatus ad sed, ut has iisque consulatu. Eam ex voluptatum mediocritatem, at democritum dissentiunt nam, sea id voluptua inciderint. Has ea posse soleat."

        self.symbol = Symbol.objects.create(name=self.symbol_name)
        self.user = User.objects.create_superuser('user', 'email@test.com', 'mypassword123')
        self.scrape_request = ScrapeRequest.objects.create(user=self.user)

        ScrapeResult.objects.create(
            headline=self.headline,
            symbol=self.symbol,
            article=self.article,
            posted_at=timezone.now(),
            scrape_request=self.scrape_request,
        )

    def test_scrape_result_can_be_created(self):
        scrape_result = ScrapeResult.objects.filter(
            symbol=self.symbol,
            scrape_request=self.scrape_request,
            headline=self.headline,
        ).first()
        self.assertIsNotNone(scrape_result)