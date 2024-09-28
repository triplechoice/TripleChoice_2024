from django_filters import rest_framework as filters
from product.models.product_models import Part
import django_filters


class PartFilter(filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='istartswith')

    class Meta:
        model = Part
        fields = '__all__'

    def filter_queryset(self, queryset):
        if self.request.GET:
            title = (self.request.GET['title'])
        else:
            title = self.request.data.get('title')

        queryset = queryset.filter(title__istartswith=title)
        return queryset


class PartExactTitleFilter(filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='exact')

    class Meta:
        model = Part
        fields = '__all__'
