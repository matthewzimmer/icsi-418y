# Generated by Django 2.1.3 on 2018-11-12 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_delete_appuser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scraperequest',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='scraperesult',
            old_name='symbol_id',
            new_name='symbol',
        ),
    ]
