# Generated by Django 4.1.13 on 2024-02-11 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='item_count',
        ),
    ]
