# Generated by Django 3.0.3 on 2020-09-19 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_winner_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winner',
            name='seller',
            field=models.CharField(max_length=64),
        ),
    ]