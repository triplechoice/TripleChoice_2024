from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from customer.filters import CustomerOrderInfoFilter, CustomerRequestFilter, RequestHistoryFilter, RequestReviewFilter
from order.models.order import OrderInfo
from order.models.request import Request, RequestHistory, RequestReview
from order.paginations import RequestPagination
from order.serealizer.order import OrderInfoShowSerializer
from order.serealizer.request import CustomerRequestApiSerializer, RequestHistoryApiSerializer, \
    RequestReviewShowSerializer


class CustomerRequestView(ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = CustomerRequestApiSerializer
    filterset_class = CustomerRequestFilter
    pagination_class = RequestPagination
    http_method_names = ['get']

    def get_queryset(self):
        order_by = '-id'
        if self.request.GET.get('order_by'):
            order_by = self.request.GET.get('order_by').lower()
            if 'request' in order_by:
                order_by = order_by.replace('request', 'order_id')
            if 'date' in order_by:
                order_by = order_by.replace('date', 'updated_at')
            if 'status' in order_by.lower():
                order_by = order_by.replace('status', 'customer_status')
            if 'part' in order_by.lower():
                order_by = order_by.replace('part', 'part__title')

        return Request.objects.filter(user_id=self.request.user.id).order_by(order_by)


class CustomerOrderView(ModelViewSet):
    queryset = OrderInfo.objects.all()
    serializer_class = OrderInfoShowSerializer
    filterset_class = CustomerOrderInfoFilter
    pagination_class = RequestPagination
    http_method_names = ['get']

    def get_queryset(self):
        order_by = '-id'
        if self.request.GET.get('order_by'):
            order_by = self.request.GET.get('order_by').lower()
            if 'date' in order_by:
                order_by = order_by.replace('date', 'updated_at')
        return OrderInfo.objects.filter(user_id=self.request.user.id).order_by(order_by)


class RequestHistoryApiView(ModelViewSet):
    queryset = RequestHistory.objects.all()
    serializer_class = RequestHistoryApiSerializer
    pagination_class = RequestPagination
    filterset_class = RequestHistoryFilter

    def get_queryset(self):
        order_by = '-id'
        if self.request.GET.get('order_by'):
            order_by = self.request.GET.get('order_by').lower()
            if 'update_at' in order_by:
                order_by = order_by.replace('update_at', 'updated_at')
        return RequestHistory.objects.filter(order_id=self.request.query_params.get('order_id')).order_by(order_by)


class RequestReviewApiView(ModelViewSet):
    queryset = RequestReview.all_objects.all()
    serializer_class = RequestReviewShowSerializer
    filterset_class = RequestReviewFilter
    pagination_class = RequestPagination

    def get_queryset(self):
        order_by = '-id'
        if self.request.GET.get('order_by'):
            order_by = self.request.GET.get('order_by').lower()
            if 'type' in order_by:
                order_by = order_by.replace('type', 'request__type')
        return RequestReview.all_objects.filter(selectedrequestreview__request_id=self.request.GET.get('request_id'),
                                                request__user=self.request.user).order_by(order_by)


class RequestCancelView(APIView):

    def get(self, request, pk):
        request_obj = Request.objects.filter(id=pk, user=request.user).first()
        if request_obj is None:
            raise PermissionDenied
        if request_obj:
            request_obj.admin_status = 'cancelled'
            request_obj.moderator_status = 'cancelled'
            request_obj.customer_status = 'cancelled'
            request_obj.supplier_status = 'cancelled'
            request_obj.save()
        messages.success(request, message='Request cancelled successfully')
        return redirect('/user/requests/')
