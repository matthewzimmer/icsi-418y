# Generated by Django 2.1.3 on 2018-11-13 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20181112_0053'),
    ]

    operations = [
        migrations.AddField(
            model_name='scraperesult',
            name='headline',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]
