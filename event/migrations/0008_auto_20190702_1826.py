# Generated by Django 2.1.7 on 2019-07-02 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0007_auto_20190701_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='ordered_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]