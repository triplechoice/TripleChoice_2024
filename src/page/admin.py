from django.contrib import admin

# Register your models here.
from page.models import PageSEO, Page, Website


class PageSEOAdmin(admin.StackedInline):
    model = PageSEO
    extra = 2


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    inlines = (PageSEOAdmin,)
    
@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ["title", ]
    
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
