from django.db import models

class Item(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    tags = models.CharField(max_length=255)
    stock_status = models.CharField(max_length=20, choices=[
        ('in_stock', 'In Stock'),
        ('out_of_stock', 'Out of Stock'),
    ])
    available_stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    name = models.CharField(max_length=255)

def __str__(self):
    return self.name