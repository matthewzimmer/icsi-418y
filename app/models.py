from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


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
    scraped_at = models.DateTimeField(blank=True)

    def __str__(self):
        return "Requested by {0} at {1}".format(self.user.email, self.created_at)

    class Meta:
        verbose_name_plural = "Scrape Requests"
        db_table = "app_scrape_requests"


class ScrapeResult(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    posted_at = models.DateTimeField()
    article = models.TextField(null=False)
    symbol = models.ForeignKey(Symbol, null=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    scrape_request_id = models.ForeignKey(ScrapeRequest, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return "[{0}] {1}".format(self.symbol.name, self.article[0:-1])

    class Meta:
        verbose_name_plural = "Scrape Results"
        db_table = "app_scrape_results"
