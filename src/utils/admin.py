from django.contrib import admin

# Register your models here.
from utils.models import Unit


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    pass
