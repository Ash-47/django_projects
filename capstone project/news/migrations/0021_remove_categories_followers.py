# Generated by Django 3.0.3 on 2020-11-17 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0020_auto_20201117_1911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='followers',
        ),
    ]