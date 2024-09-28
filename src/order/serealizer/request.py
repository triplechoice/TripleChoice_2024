import json
import random
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.forms import model_to_dict

from authentication.email import send_activation_email
from authentication.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.exceptions import ValidationError

from order.models.request import Request, RequestHistory, RequestReview, RequstReviewAttachment, SelectedRequestReview
from product.models.product_models import Part


class RequestSerializer(ModelSerializer):
    is_logged_in = serializers.ReadOnlyField()

    def create(self, validated_data):
        user_email = validated_data['contact_info']['email']
        user_obj = User.objects.filter(email=user_email).first()

        if user_obj is None:
            # TODO::add user more info and change user name
            username = user_email
            password = make_password(validated_data['contact_info']['password'])
            user_obj = User.objects.create(email=user_email, first_name=validated_data['contact_info']['first_name'],
                                           last_name=validated_data['contact_info']['last_name'], password=password,
                                           username=username, is_active=False)

            group = Group.objects.filter(name='customer').first()
            user_obj.groups.add(group)
            send_activation_email(self.context['request'], user_obj)

            validated_data["is_logged_in"] = "new_created_user"

        elif user_obj and self.context["request"].user.is_anonymous:
            matchcheck = check_password(validated_data['contact_info']['password'], user_obj.password)
            if matchcheck:
                validated_data['is_logged_in'] = "user_already_exists"
            else:
                validated_data['is_logged_in'] = "wrong_password_given"
                return validated_data

        elif not self.context["request"].user.is_anonymous:
            validated_data["is_logged_in"] = "previously_logged_in"

        order_id = random.randrange(1000, 1000000000)
        self.save_request(validated_data, order_id, user_obj)

        return validated_data

    def update(self, instance, validated_data):
        order_id = instance.order_id
        kwargs = model_to_dict(instance, exclude=['id', 'part', 'user', 'is_deleted'])
        kwargs['part_id'] = instance.part.id
        kwargs['user_id'] = instance.user.id
        kwargs['modified_number'] = instance.modified_number + 1
        RequestHistory.objects.create(**kwargs)
        instance.delete()
        user_email = validated_data['contact_info']['email']
        user_obj = User.objects.filter(email=user_email).first()
        modified_number = instance.modified_number + 1
        self.save_request(validated_data, order_id, user_obj, modified_number)
        return validated_data

    def save_request(self, validated_data, order_id, user_obj, modified_number=0):
        data = {'order_id': order_id, 'quantity': validated_data['quantity'], 'type': validated_data['type'],
                'answer': validated_data['answer'], 'part_id': validated_data['answer']['id'],
                'modified_number': modified_number, 'contact_info': validated_data['contact_info'],
                'comment': validated_data['comment'], 'image_comment': validated_data.get('image_comment'),
                'user': user_obj, 'customer_status': 'submitted', 'admin_status': 'pending',
                'zip_code': validated_data['zip_code']}
        Request.objects.create(**data)

    class Meta:
        model = Request
        fields = '__all__'


class RequestReviewSerializer(ModelSerializer):
    class Meta:
        model = RequestReview
        fields = '__all__'


class SelectedReviewSerializer(Serializer):
    id = serializers.IntegerField()


class SelectedRequestReviewSerializer(Serializer):
    request_id = serializers.IntegerField()
    reviews = serializers.ListField()


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ['id', 'title']


class GetRequestInfoSerializer(serializers.ModelSerializer):
    part = PartSerializer(many=False)

    class Meta:
        model = Request
        fields = ['id', 'order_id', 'cost', 'lead_time', 'quantity', 'part']


class GetRequestReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestReview
        fields = '__all__'


class RequestApiAbstractSerializer(ModelSerializer):
    # Request = serializers.CharField(source='order_id', read_only=True)
    part = serializers.SerializerMethodField(source='part')
    # quantity = serializers.CharField(source='quantity', read_only=True)
    type = serializers.SerializerMethodField(source='type', read_only=True)
    # Status = serializers.SerializerMethodField(source='supplier_status', read_only=True)
    date = serializers.SerializerMethodField(source='date', read_only=True)


class SupplierRequestApiSerializer(RequestApiAbstractSerializer):
    status = serializers.SerializerMethodField(source='supplier_status', read_only=True)

    class Meta:
        model = Request
        fields = ['id', 'order_id', 'part', 'quantity', 'status', 'type', 'date']

    def get_part(self, obj):
        return obj.part.title

    def get_type(self, obj):
        return obj.type.capitalize()

    def get_date(self, obj):
        return obj.updated_at.strftime('%m/%d/%Y')

    def get_status(self, obj):
        return obj.get_supplier_status_display()


class ModeratorRequestApiSerializer(RequestApiAbstractSerializer):
    status = serializers.SerializerMethodField(source='moderator_status', read_only=True)

    class Meta:
        model = Request
        fields = ['id', 'order_id', 'part', 'quantity', 'status', 'type', 'date']

    def get_part(self, obj):
        return obj.part.title

    def get_type(self, obj):
        return obj.type.capitalize()

    def get_date(self, obj):
        return obj.updated_at.strftime('%m/%d/%Y')

    def get_status(self, obj):
        return obj.get_moderator_status_display()


class CustomerRequestApiSerializer(ModelSerializer):
    # Request = serializers.CharField(source='order_id', read_only=True)
    part = serializers.SerializerMethodField(source='part')
    type = serializers.SerializerMethodField(source='type', read_only=True)
    status = serializers.SerializerMethodField(source='customer_status', read_only=True)
    date = serializers.SerializerMethodField(source='updated_at', read_only=True)
    slug = serializers.SerializerMethodField(source='part__slug', read_only=True)

    class Meta:
        model = Request
        fields = ['id', 'order_id', 'part', 'quantity', 'type', 'status', 'date', 'slug']

    def get_part(self, obj):
        return obj.part.title

    def get_type(self, obj):
        return obj.type.capitalize()

    def get_status(self, obj):
        return obj.get_customer_status_display()

    def get_date(self, obj):
        return obj.updated_at.strftime('%m/%d/%Y')

    def get_slug(self, obj):
        return obj.part.slug


class RequestHistoryApiSerializer(ModelSerializer):
    part = serializers.SerializerMethodField(source='part', read_only=True)
    update_at = serializers.SerializerMethodField(source='updated_at', read_only=True)
    order_id = serializers.SerializerMethodField(source='order_id', read_only=True)

    class Meta:
        model = RequestHistory
        fields = ['id', 'order_id', 'part', 'quantity', 'update_at']

    def get_order_id(self, obj):
        return f'{obj.order_id}-m{obj.modified_number}'

    def get_part(self, obj):
        return f'{obj.part.title}'

    def get_update_at(self, obj):
        return obj.updated_at.strftime('%m/%d/%Y')


class RequestReviewAttachmentSerializer(ModelSerializer):
    class Meta:
        model = RequstReviewAttachment
        fields = ['id', 'file']


class RequestReviewShowSerializer(ModelSerializer):
    lead_time = serializers.SerializerMethodField(source='lead_time', read_only=True)
    cost = serializers.SerializerMethodField(source='cost', read_only=True)
    attachments = RequestReviewAttachmentSerializer(many=True, read_only=True)
    type = serializers.SerializerMethodField(source='request_type', read_only=True)

    class Meta:
        model = RequestReview
        fields = ['id', 'title', 'attachments', 'type', 'quantity', 'lead_time', 'cost', 'is_deleted']

    def get_lead_time(self, obj):
        return f'{obj.lead_time} {obj.get_unit_display()}'

    def get_cost(self, obj):
        return f'{obj.cost} {obj.get_cost_unit_display()}'

    def get_type(self, obj):
        return obj.request.get_type_display()


class SupplierSelectedRequestReviewSerializer(ModelSerializer):
    class Meta:
        model = SelectedRequestReview
        fields = ('id',)


class SupplierRequestReviewSerializer(ModelSerializer):
    lead_time = serializers.SerializerMethodField(source='supplier_lead_time', read_only=True)
    cost = serializers.SerializerMethodField(source='supplier_cost', read_only=True)
    attachments = RequestReviewAttachmentSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = RequestReview
        fields = ['id', 'title', 'attachments', 'quantity', 'lead_time', 'cost', 'reviews']

    def get_lead_time(self, obj):
        return f'{obj.supplier_lead_time} {obj.get_supplier_unit_display()}'

    def get_cost(self, obj):
        return f'{obj.supplier_cost} {obj.get_supplier_cost_unit_display()}'

    def get_reviews(self, obj):
        reviews = obj.selectedrequestreview_set.all()  # will return product query set associate with this category
        response = SupplierSelectedRequestReviewSerializer(reviews, many=True).data
        return response
