from rest_framework import serializers
from order.models.request import Request, RequestHistory, RequestReview, RequestReviewAttachment, SelectedRequestReview
from order.models.order import OrderInfo  # Import OrderInfo if needed

class SupplierRequestReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestReview
        fields = '__all__'  # Adjust this to include specific fields if necessary

class GetRequestInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request  # Make sure Request is imported
        fields = '__all__'  # Specify the fields you want to serialize

class GetRequestReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestReview
        fields = '__all__'
