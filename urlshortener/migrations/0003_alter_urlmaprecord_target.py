# Generated by Django 5.0.1 on 2024-02-01 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urlshortener', '0002_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlmaprecord',
            name='target',
            field=models.URLField(max_length=2000, verbose_name='target URL'),
        ),
    ]