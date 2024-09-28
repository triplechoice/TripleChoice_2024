from authentication.models import User
from django.db import models
from django.template.defaultfilters import slugify

from triple_choice.db.mixins import AuthorMixin, TimeStampMixin
from utils.models import Unit


class Classification(AuthorMixin, TimeStampMixin):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Attribute(AuthorMixin, TimeStampMixin):
    TYPE_CHOICE = (
        ('text', 'Text'),
        ('number', 'Number'),
        ('select', 'Select')
    )
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, choices=TYPE_CHOICE, default='text')
    options = models.CharField(max_length=255, null=True, blank=True)
    unit = models.ManyToManyField(Unit, blank=True)

    def __str__(self):
        return self.title


class Part(AuthorMixin, TimeStampMixin):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    
    class Meta:
        ordering=('title',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class PartSupplier(AuthorMixin, TimeStampMixin):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    supplier = models.ManyToManyField(User)


class PartClassification(AuthorMixin, TimeStampMixin):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    classification = models.ForeignKey(Classification, related_name='classifications', on_delete=models.CASCADE)
    is_optional = models.CharField(max_length=255, blank=True, default='False')

    def __str__(self):
        return self.part.title


class PartClassificationAttribute(AuthorMixin, TimeStampMixin):
    part_classification = models.ForeignKey(PartClassification, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    is_optional = models.CharField(max_length=50, blank=True, default='False')

    def __str__(self):
        return self.attribute.title
