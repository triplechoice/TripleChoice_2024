import json
import os
import random

import stripe
from django.db import transaction
from django.forms import model_to_dict
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.serializers import ModelSerializer
from order.models.order import OrderInfo, BillingAddress, ShippingAddress, OrderInfoHistory
from order.models.request import Request


class BillingAddressSerializer(ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = '__all__'


class ShippingAddressSerializer(ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    billing_address = BillingAddressSerializer()
    shipping_address = ShippingAddressSerializer()
    unit = serializers.CharField(write_only=True, allow_blank=True)

    class Meta:
        model = OrderInfo
        fields = '__all__'

    def create(self, validated_data):
        try:
            with transaction.atomic():
                unit = validated_data.pop('unit')
                billing_address = validated_data.pop('billing_address')
                shopping_address = validated_data.pop('shipping_address')
                bil_add = BillingAddress.objects.create(**billing_address)
                sho_add = ShippingAddress.objects.create(**shopping_address)
                order_id = random.randrange(1000, 1000000000)
                review = validated_data.get('review')
                if review == "None":
                    validated_data.pop('review')
                order = OrderInfo.objects.create(order_id=order_id, billing_address=bil_add, shipping_address=sho_add,
                                                 **validated_data)

                request_order_id = order.request.order_id
                request_obj = Request.objects.get(order_id=request_order_id)
                request_obj.admin_status = "completed"
                request_obj.customer_status = "quote_submitted"
                request_obj.supplier_status = "quote_submitted"
                request_obj.moderator_status = "quote_submitted"
                request_obj.save()
                stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
                # TODO::add form currency
                payment_intent = stripe.PaymentIntent.create(
                    amount=int(validated_data['total']),
                    currency=unit.lower(),
                    payment_method_types=["card"],
                )
                # To create a PaymentIntent for confirmation, see our guide at: https://stripe.com/docs/payments/payment-intents/creating-payment-intents#creating-for-automatic
                confirm_payment = stripe.PaymentIntent.confirm(
                    payment_intent.id,
                    payment_method="pm_card_visa",
                )
                order.payment_info = json.loads(str(confirm_payment))
                order.status = 'received'
                order.save()
                return order
        except Exception as e:
            raise APIException(e)

    def update(self, instance, validated_data):
        order_id = instance.order_id
        modified_number = instance.modified_number + 1
        kwargs = model_to_dict(instance, exclude=['id', 'is_deleted'])
        kwargs['modified_number'] = modified_number
        request = validated_data.pop('request')
        kwargs['request'] = request
        bill_add_id = kwargs.pop('billing_address')
        ship_add_id = kwargs.pop('shipping_address')
        user_id = kwargs.pop('user')
        kwargs['billing_address_id'] = bill_add_id
        kwargs['shipping_address_id'] = ship_add_id
        kwargs['user_id'] = user_id
        OrderInfoHistory.objects.create(**kwargs)
        instance.delete()
        billing_address = validated_data.pop('billing_address')
        shopping_address = validated_data.pop('shipping_address')
        bil_add = BillingAddress.objects.create(**billing_address)
        sho_add = ShippingAddress.objects.create(**shopping_address)
        updated_order = OrderInfo.objects.create(order_id=order_id, billing_address=bil_add, shipping_address=sho_add,
                                                 request=request, modified_number=modified_number, **validated_data)
        return updated_order


class OrderInfoShowSerializer(ModelSerializer):
    date = serializers.SerializerMethodField(source='created_at', read_only=True)
    status = serializers.SerializerMethodField(source='status', read_only=True)
    payment_method = serializers.SerializerMethodField(source='payment_method', read_only=True)

    class Meta:
        model = OrderInfo
        fields = ['id', 'order_id', 'quantity', 'payment_method', 'status', 'subtotal', 'tax', 'total', 'date']

    def get_date(self, obj):
        return obj.created_at.strftime('%m/%d/%Y')

    def get_status(self, obj):
        if obj.status == 'shipped':
            return f'{obj.get_status_display().capitalize()} {obj.tracking_number}'
        return obj.get_status_display().capitalize()

    def get_payment_method(self, obj):
        return obj.get_payment_method_display().capitalize()
