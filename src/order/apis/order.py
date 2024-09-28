import json
import os

import stripe
from django.conf import settings
from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import transaction
from django.shortcuts import redirect, render, resolve_url
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework import status
from urllib3.util import url

from authentication.mixins import PermissionMixin
from order.forms.review_form import RequestReviewForm
from order.models.request import Request, RequestReview, SelectedRequestReview
from order.serealizer.request import RequestSerializer, RequestReviewSerializer, SelectedRequestReviewSerializer
from utils.services.disposable_email import DisposableEmail

from rest_framework.exceptions import PermissionDenied, APIException
from order.models.order import OrderInfo, ShippingAddress, BillingAddress
from rest_framework.viewsets import ModelViewSet
from order.serealizer.order import OrderSerializer, ShippingAddressSerializer, BillingAddressSerializer
from utils.services.stripe import StripePayment

from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class RequestView(ListAPIView, CreateAPIView, UpdateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def perform_create(self, serializer):
        # here you will send `created_by` in the `validated_data`
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        data_dict = json.loads(request.data['form_data'])
        data_dict['image_comment'] = request.FILES.get('file_comment')
        serializer = self.get_serializer(data=data_dict)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.id != instance.user.id:
            raise PermissionDenied("this in not logged in users order")

        return self.update(request, *args, **kwargs)


class CheckDisposableEmail(APIView, DisposableEmail):
    def get(self, request):
        email = request.GET.get('email')
        domain = email.split('@')[1]
        result = self.check_disposable_email(domain)
        return Response({'result': result})


class RequestPartView(RetrieveAPIView):
    serializer_class = RequestSerializer
    queryset = Request.objects.all()

    def get(self, request, *args, **kwargs):
        part_view_data = self.retrieve(request, *args, **kwargs)

        if request.user.id != part_view_data.data["user"]:
            raise PermissionDenied("this is not  logged in users order")

        return part_view_data


class RequestDeleteView(PermissionMixin, APIView):
    permission_required = ('order.delete_request',)
    serializer_class = RequestSerializer
    queryset = Request.objects.all()

    def get(self, request, pk, *args, **kwargs):
        instance = Request.objects.filter(id=pk, user=request.user).first()
        if not instance:
            raise PermissionDenied
        if instance.customer_status != 'submitted':
            messages.error(request, "You can not delete the request in this state", extra_tags='error')
            return redirect(reverse('customer:customer_requests'))
        instance.soft_delete()
        messages.success(request, "Request deleted successfully", extra_tags='success')
        return redirect('customer:customer_requests')


class ApiRequestReviewView(APIView):
    def get(self, request, request_id, *args, **kwargs):
        queryset = RequestReview.objects.filter(request__order_id=request_id)
        serializer = RequestReviewSerializer(queryset, many=True)
        return Response(serializer.data)


class ApiRequestReviewCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SelectedRequestReviewSerializer(data=request.data)
        try:
            if serializer.is_valid():
                ins = SelectedRequestReview.objects.filter(request_id=serializer.validated_data['request_id']).first()
                if ins:
                    ins.review.set(RequestReview.objects.filter(id__in=serializer.validated_data['reviews']))
                    ins.save()
                else:
                    selected_review = SelectedRequestReview.objects.get_or_create(
                        request_id=serializer.validated_data['request_id'])
                    selected_review.review.set(serializer.validated_data['reviews'])

            return Response({"message": "Data store successfully"})
        except Exception:
            return Response({"message": Exception})


class OrderView(ModelViewSet):
    queryset = OrderInfo.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ['post', 'put']


class StripCheck(APIView):
    def get(self, request):
        print('aaa')


class OrderDeleteView(PermissionMixin, APIView, StripePayment):
    permission_required = ('order.delete_orderinfo',)
    serializer_class = OrderSerializer
    queryset = OrderInfo.objects.all()

    def get(self, request, pk, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = OrderInfo.objects.filter(id=pk, user=request.user).first()
                if instance is None:
                    messages.error(request,
                                   message="Permission required for this action",
                                   extra_tags='error')
                    return redirect('customer:customer_orders')

                if instance.status == 'received' or instance.status == 'processing':
                    instance.soft_delete()
                    self.refund(instance)
                    messages.success(request, "Request deleted successfully", extra_tags='success')
                    return redirect('customer:customer_orders')
                messages.error(request, "You can not delete the order in this state", extra_tags='error')
                return redirect(reverse('customer:customer_orders'))

        except Exception as e:
            messages.error(request,
                           message=f'{instance.payment_info["charges"]["data"][0]["id"]} has already been refunded.',
                           extra_tags='error')
            return redirect('customer:customer_orders')


class GetOrderView(APIView):
    def get(self, request, order_id):
        order = OrderInfo.objects.filter(id=order_id).first()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
