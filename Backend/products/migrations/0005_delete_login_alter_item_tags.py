# Generated by Django 4.1.13 on 2024-02-12 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_item_created_at'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Login',
        ),
        migrations.AlterField(
            model_name='item',
            name='tags',
            field=models.CharField(max_length=255),
        ),
    ]