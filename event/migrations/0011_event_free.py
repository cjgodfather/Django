# Generated by Django 2.1.7 on 2019-07-08 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0010_auto_20190704_0115'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='free',
            field=models.BooleanField(default=False),
        ),
    ]