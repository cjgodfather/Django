# Generated by Django 2.1.7 on 2019-06-18 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.SlugField(default=1),
            preserve_default=False,
        ),
    ]
