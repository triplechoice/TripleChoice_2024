from datetime import datetime

import django_filters
from django.db.models import Q

from order.models.request import Request, RequestReview


class RequestFilter(django_filters.FilterSet):
    def my_custom_filter_with_description(self, queryset, *args, **kwargs):
        value = args[0]

        if "/" in value:
            temp_data = value.split("/")
            if len(temp_data) >= 3:
                if len(temp_data[2]) == 4:
                    value = datetime.strptime(value, '%m/%d/%Y')
                    return self.filter(Q(Q(updated_at__date=value)))
            return self
        if value.isnumeric():
            return self.filter(Q(Q(order_id__icontains=value) | Q(quantity=int(value))))

        return self.filter(
            Q(Q(part__title__icontains=value) | Q(type__iexact=value) | Q(supplier_status__icontains=value)))

    field = django_filters.CharFilter(method=my_custom_filter_with_description)

    class Meta:
        model = Request
        fields = ['field']

    @property
    def qs(self):
        queryset = super(RequestFilter, self).qs
        return queryset.filter(part__partsupplier__supplier__pk=self.request.user.id).exclude(
            supplier_status=None).exclude(supplier_status="").exclude(user_id=self.request.user.id)


class ModeratorRequestFilter(django_filters.FilterSet):
    def my_custom_filter_with_description(self, queryset, *args, **kwargs):
        value = args[0]

        if "/" in value:
            temp_data = value.split("/")
            if len(temp_data) >= 3:
                if len(temp_data[2]) == 4:
                    value = datetime.strptime(value, '%m/%d/%Y')
                    return self.filter(Q(Q(updated_at__date=value)))
            return self

        if value.isnumeric():
            return self.filter(Q(Q(order_id__icontains=value) | Q(quantity=int(value))))

        return self.filter(
            Q(Q(part__title__icontains=value) | Q(type__iexact=value) | Q(
                moderator_status__icontains=value)))

    field = django_filters.CharFilter(method=my_custom_filter_with_description)

    class Meta:
        model = Request
        fields = ['field']

    @property
    def qs(self):
        queryset = super(ModeratorRequestFilter, self).qs
        return queryset.exclude(user_id=self.request.user.id)


class SupplierReviewRequestFilter(django_filters.FilterSet):
    def my_custom_filter_with_description(self, queryset, *args, **kwargs):
        value = args[0]
        if value.isnumeric():
            return self.filter(Q(Q(quantity=int(value))))

        return self.filter(
            Q(Q(title__icontains=value)))

    field = django_filters.CharFilter(method=my_custom_filter_with_description)

    class Meta:
        model = RequestReview
        fields = ['field']

    @property
    def qs(self):
        queryset = super(SupplierReviewRequestFilter, self).qs
        return queryset.filter(request=self.request.query_params.get('request_id'),
                               user=self.request.user)


class ModeratorReviewRequestFilter(django_filters.FilterSet):
    def my_custom_filter_with_description(self, queryset, *args, **kwargs):
        value = args[0]
        if value.isnumeric():
            return self.filter(Q(Q(quantity=int(value))))

        return self.filter(
            Q(Q(title__icontains=value)))

    field = django_filters.CharFilter(method=my_custom_filter_with_description)

    class Meta:
        model = RequestReview
        fields = ['field']

    @property
    def qs(self):
        queryset = super(ModeratorReviewRequestFilter, self).qs
        return queryset.filter(request=self.request.query_params.get('request_id'))