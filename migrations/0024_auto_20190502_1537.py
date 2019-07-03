# Generated by Django 2.2.1 on 2019-05-02 15:37

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('context_text', '0023_auto_20190424_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='details_json',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]