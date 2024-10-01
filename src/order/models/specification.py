from django.db import models
from order.models.request import Request  # Ensure this import is correct based on your project structure

class Specifications(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    value = models.TextField()  # Use TextField for larger values

    def __str__(self):
        return f"{self.title}: {self.value}"
