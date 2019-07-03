# Generated by Django 2.2.1 on 2019-05-04 21:18

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('context_text', '0024_auto_20190502_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='article_data_notes',
            name='note_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='article_data_notes',
            name='source_identifier',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='article_data_notes',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='article_notes',
            name='note_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='article_notes',
            name='source_identifier',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='article_notes',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='article_rawdata',
            name='note_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='article_rawdata',
            name='source_identifier',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='article_rawdata',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='article_text',
            name='note_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='article_text',
            name='source_identifier',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='article_text',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]