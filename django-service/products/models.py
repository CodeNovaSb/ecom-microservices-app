from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    product_image = models.URLField()
    alt_text = models.CharField(max_length=200)
    stock_quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name
