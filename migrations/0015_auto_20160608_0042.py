# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-08 00:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sourcenet', '0014_auto_20160607_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='alternate_name',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sourcenet.Organization'),
        ),
        migrations.AddField(
            model_name='article_author',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='article_author',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sourcenet.Organization'),
        ),
        migrations.AddField(
            model_name='person',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sourcenet.Organization'),
        ),
    ]