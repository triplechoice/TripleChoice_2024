from datetime import datetime
import django_filters
from django.db.models import Q

from order.models.order import OrderInfo
from order.models.request import Request, RequestHistory, RequestReview


class CustomerOrderInfoFilter(django_filters.FilterSet):
    def my_custom_filter_with_description(self, queryset, *args, **kwargs):
        value = args[0]
        if "/" in value:
            temp_data = value.split("/")
            if len(temp_data) >= 3:
                if len(temp_data[2]) == 4:
                    value = datetime.strptime(value, '%m/%d/%Y')
                    return self.filter(Q(Q(created_at__date=value)))
            return self
        if value.isnumeric():
            return self.filter(Q(Q(order_id__icontains=value) | Q(quantity=int(value)) | Q(subtotal=float(value)) | Q(
                tax=float(value)) | Q(total=float(value))))

        return self.filter(Q(Q(payment_method__icontains=value) | Q(status__icontains=value)))

    field = django_filters.CharFilter(method=my_custom_filter_with_description)

    class Meta:
        model = OrderInfo
        fields = ['field']

    @property
    def qs(self):
        queryset = super(CustomerOrderInfoFilter, self).qs
        return queryset.filter(user=self.request.user.id)


class CustomerRequestFilter(django_filters.FilterSet):
    def my_custom_filter_with_description(self, queryset, *args, **kwargs):
        value = args[0]
        if "/" in value:
            temp_data = value.split("/")
            if len(temp_data) >= 3:
                if len(temp_data[2]) == 4:
                    value = datetime.strptime(value, '%m/%d/%Y')
                    return self.filter(Q(Q(updated_at__date=value))).order_by('-id')
            return self
        if value.isnumeric():
            return self.filter(Q(Q(order_id__icontains=value) | Q(quantity=int(value))))

        return self.filter(
            Q(Q(type__icontains=value) | Q(part__title__icontains=value) | Q(customer_status__icontains=value)))

    field = django_filters.CharFilter(method=my_custom_filter_with_description)

    class Meta:
        model = Request
        fields = ['field']

    @property
    def qs(self):
        queryset = super(CustomerRequestFilter, self).qs
        return queryset.filter(user=self.request.user.id)


class RequestHistoryFilter(django_filters.FilterSet):
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
            return self.filter(Q(Q(quantity=int(value))))

        return self.filter(Q(Q(part__title__icontains=value)))

    field = django_filters.CharFilter(method=my_custom_filter_with_description)

    class Meta:
        model = RequestHistory
        fields = ['field']

    @property
    def qs(self):
        queryset = super(RequestHistoryFilter, self).qs
        return queryset.filter(order_id=self.request.query_params.get('order_id'))


class RequestReviewFilter(django_filters.FilterSet):
    def my_custom_filter_with_description(self, queryset, *args, **kwargs):
        value = args[0]
        if value.isnumeric():
            return self.filter(
                Q(Q(quantity=int(value))) | (Q(cost=float(value))) | (Q(lead_time=float(value))))
        return self.filter(
            Q(Q(title__icontains=value)) | (Q(request__type__icontains=value)))

    field = django_filters.CharFilter(method=my_custom_filter_with_description)

    class Meta:
        model = RequestReview
        fields = ['field']

    @property
    def qs(self):
        queryset = super(RequestReviewFilter, self).qs
        return queryset.filter(selectedrequestreview__request_id=self.request.query_params.get('request_id'),
                               request__user=self.request.user)
