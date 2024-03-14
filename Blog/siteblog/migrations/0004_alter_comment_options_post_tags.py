# Generated by Django 5.0.2 on 2024-03-02 16:08

import taggit.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('siteblog', '0003_alter_post_slug_comment'),
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created'], 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
