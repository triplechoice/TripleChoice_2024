import json
import os
import subprocess

import boto3
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
from .extractor import fetch_latest_order
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
        print("*"*100)
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.id != instance.user.id:
            raise PermissionDenied("this in not logged in users order")

        return self.update(request, *args, **kwargs)





# Create a local DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-west-2',
    endpoint_url='http://localhost:8001',  # Adjust if you're using an actual AWS instance
    aws_access_key_id="anything",  # Replace with actual key if on AWS
    aws_secret_access_key="anything"  # Replace with actual secret if on AWS
)

# Define the table name
table_name = 'YourTableName'  # Replace with your actual table name
table = dynamodb.Table(table_name)

# Function to get pump data from DynamoDB
def get_pump_data():
    response = table.scan()
    return response['Items']

# Function to predict head based on flow rate using the pump curve
def predict_head(flow_rate, pump_curve):
    # Calculate predicted head using polynomial coefficients
    predicted_head = sum(coef * (flow_rate ** i) for i, coef in enumerate(reversed(pump_curve)))
    return predicted_head

class PumpDataView(APIView):
    def get(self, request):
        try:
            # Parse the input parameters from the request query params
            input_flow_rate = float(request.query_params.get('input_flow_rate', 0))
            head_input = float(request.query_params.get('head_input', 0))

            # Fetch pump data from DynamoDB
            pump_data_list = get_pump_data()

            # Prepare a list for results
            results = []

            # Check for all pumps
            for pump_data in pump_data_list:
                pump_name = pump_data['Name']
                pump_curve = [float(coef) for coef in pump_data['PumpCurve']]  # Convert to float for calculation

                # Predict the head using the input flow rate
                head_predicted = predict_head(input_flow_rate, pump_curve)

                # Determine if it's a matching pump
                is_match = head_input < head_predicted < head_input * 1.25
                match_status = "Match" if is_match else "No Match"

                # Append the results
                results.append({
                    'Pump Name': pump_name,
                    'Input Flow Rate (GPM)': input_flow_rate,
                    'Input Head (ft)': head_input,
                    'Predicted Head (ft)': head_predicted,
                    'Match Pump': match_status
                })

            # Return the results as JSON
            print("This is results: ", results)
            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PumpMatchInputAPIView(APIView):
    def post(self, request):
        # Get the values from the request data
        input_flow_rate = request.data.get('input_flow_rate')
        head_input = request.data.get('head_input')

        if input_flow_rate is None or head_input is None:
            return Response({"error": "Both 'input_flow_rate' and 'head_input' are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Convert to float
            input_flow_rate = float(input_flow_rate)
            head_input = float(head_input)

            return Response({"input_flow_rate": input_flow_rate, "head_input": head_input})
        except ValueError:
            return Response({"error": "Invalid input. 'input_flow_rate' and 'head_input' must be numbers."}, status=status.HTTP_400_BAD_REQUEST)

class OrderPumpMatchView(APIView):
    def post(self, request, *args, **kwargs):
        # Parse the input parameters from the request query params
        input_flow_rate = request.data.get('input_flow_rate')
        head_input = request.data.get('head_input')
        # input_flow_rate = input_flow_rate
        # head_input = head_input

        # Fetch pump data from DynamoDB
        pump_data_list = get_pump_data()

        # Prepare a list for results
        results = []

        # Check for all pumps
        for pump_data in pump_data_list:
            pump_name = pump_data['Name']
            pump_curve = [float(coef) for coef in
                          pump_data['PumpCurve']]  # Convert to float for calculation

            # Predict the head using the input flow rate
            head_predicted = predict_head(input_flow_rate, pump_curve)

            # Determine if it's a matching pump
            is_match = head_input < head_predicted < head_input * 1.25
            match_status = "Match" if is_match else "No Match"

            # Append the results
            results.append({
                'Pump Name': pump_name,
                'Input Flow Rate (GPM)': input_flow_rate,
                'Input Head (ft)': head_input,
                'Predicted Head (ft)': head_predicted,
                'Match Pump': match_status
            })

        # Return the results as JSON
        print("This is results: ", results)
        return Response(results, status=status.HTTP_200_OK)
        # # Fetch the latest order
        # order_details = fetch_latest_order()
        # if order_details:
        #     order_id, quantity, comment, specifications, title, created_at = order_details
        #
        #     # Print order details for debugging purposes
        #     print(f"Order ID: {order_id}, Title: {title}")
        #
        #     # Extract flow rate and head input from specifications
        #     input_flow_rate = None
        #     head_input = None
        #     for spec in specifications.get('partclassification_set', []):
        #         for attr in spec['partclassificationattribute_set']:
        #             if attr['attribute']['title'] == "Flow":
        #                 input_flow_rate = float(attr['attribute']['value'])
        #             if attr['attribute']['title'] == "Head":
        #                 head_input = float(attr['attribute']['value'])
        #     # Parse the input parameters from the request query params
        #     input_flow_rate = input_flow_rate
        #     head_input = head_input
        #
        #     # Fetch pump data from DynamoDB
        #     pump_data_list = get_pump_data()
        #
        #     # Prepare a list for results
        #     results = []
        #
        #     # Check for all pumps
        #     for pump_data in pump_data_list:
        #         pump_name = pump_data['Name']
        #         pump_curve = [float(coef) for coef in
        #                       pump_data['PumpCurve']]  # Convert to float for calculation
        #
        #         # Predict the head using the input flow rate
        #         head_predicted = predict_head(input_flow_rate, pump_curve)
        #
        #         # Determine if it's a matching pump
        #         is_match = head_input < head_predicted < head_input * 1.25
        #         match_status = "Match" if is_match else "No Match"
        #
        #         # Append the results
        #         results.append({
        #             'Pump Name': pump_name,
        #             'Input Flow Rate (GPM)': input_flow_rate,
        #             'Input Head (ft)': head_input,
        #             'Predicted Head (ft)': head_predicted,
        #             'Match Pump': match_status
        #         })
        #
        #     # Return the results as JSON
        #     print("This is results: ", results)
        #     return Response(results, status=status.HTTP_200_OK)
        #
        # return Response({"error": "No order found"}, status=status.HTTP_404_NOT_FOUND)




















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
