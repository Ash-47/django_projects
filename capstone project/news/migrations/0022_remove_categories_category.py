# Generated by Django 3.0.3 on 2020-11-17 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0021_remove_categories_followers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='category',
        ),
    ]
