# Generated by Django 2.1.2 on 2018-11-07 04:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapeRequest',
            fields=[
                ('id', models.IntegerField(max_length=30, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('scraped_at', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ScrapeResult',
            fields=[
                ('id', models.IntegerField(max_length=30, primary_key=True, serialize=False)),
                ('posted_at', models.DateTimeField()),
                ('article', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('scrape_request_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ScrapeRequest')),
            ],
        ),
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('id', models.IntegerField(max_length=30, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(max_length=30, primary_key=True, serialize=False)),
                ('login', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='scraperesult',
            name='symbol_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Symbol'),
        ),
        migrations.AddField(
            model_name='scraperequest',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.User'),
        ),
    ]