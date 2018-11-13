from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User


class Symbol(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=5, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "app_symbols"


class ScrapeRequest(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    user = models.ForeignKey(User, null=False, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    scraped_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "Requested by {0} at {1}".format(self.user.email, self.created_at)

    def scrape_did_complete(self):
        if self.scraped_at is None:
            self.scraped_at = timezone.now()
            self.save()

    class Meta:
        verbose_name_plural = "Scrape Requests"
        db_table = "app_scrape_requests"


class ScrapeResult(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    scrape_request = models.ForeignKey(ScrapeRequest, null=False, on_delete=models.CASCADE)
    symbol = models.ForeignKey(Symbol, null=False, on_delete=models.CASCADE)
    headline = models.TextField(null=False)
    article = models.TextField(null=False)
    posted_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return "[{0}] {1}".format(self.symbol.name, self.article[0:-1])

    class Meta:
        verbose_name_plural = "Scrape Results"
        db_table = "app_scrape_results"
