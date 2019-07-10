# Generated by Django 2.1.7 on 2019-06-30 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_auto_20190625_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_type',
            field=models.CharField(choices=[('General admission', 'GENERAL ADMISSION'), ('Early bird', 'EARLY BIRD'), ('Children', 'CHILDREN'), ('Senior', 'SENIOR')], max_length=1),
        ),
    ]
