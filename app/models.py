from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class User(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True, null=False)


class ScrapeRequest(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    user_id = models.ForeignKey(User, null=False, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    scraped_at = models.DateTimeField(blank=True)

    class Meta:
        db_table = "app_scrape_requests"


class Symbol(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=5, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = "app_symbols"


class ScrapeResult(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    posted_at = models.DateTimeField()
    article = models.TextField(null=False)
    symbol_id = models.ForeignKey(Symbol, null=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    scrape_request_id = models.ForeignKey(ScrapeRequest, null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = "app_scrape_results"
