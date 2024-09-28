from django.db import models

from triple_choice.db.mixins import AuthorMixin, TimeStampMixin


class Classification(AuthorMixin, TimeStampMixin):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title