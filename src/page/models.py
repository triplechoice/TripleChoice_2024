from django.db import models

# Create your models here.
from tinymce.models import HTMLField


class Page(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = HTMLField()

    def __str__(self):
        return self.title


class PageSEO(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Website(models.Model):
    title = models.CharField(max_length=120)
    contact_number = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.title
    class Meta:
        db_table= "website"
