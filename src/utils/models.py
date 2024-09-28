from django.db import models

# Create your models here.
from triple_choice.db.mixins import AuthorMixin, TimeStampMixin


class Unit(AuthorMixin, TimeStampMixin):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
