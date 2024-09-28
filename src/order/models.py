from django.db import models

# Create your models here.
from product.models.product_models import Part, Classification
from triple_choice.db.mixins import AuthorMixin, TimeStampMixin


class Order(AuthorMixin, TimeStampMixin):
    TYPE = (
        ("query", "Query"),
        ("quote", "Quote"),
    )

    order_id = models.CharField(max_length=255)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    answer = models.JSONField()
    quantity = models.FloatField()
    type = models.CharField(max_length=10, choices=TYPE)

    def __str__(self):
        return self.order_id
