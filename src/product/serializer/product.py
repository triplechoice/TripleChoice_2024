import json
import random

from django.template.defaultfilters import slugify
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from product.models import Attribute, Classification
from product.models.product_models import Part, PartClassification, PartClassificationAttribute
from utils.serializers.unit import UnitSerializer


class AttributeSerializer(ModelSerializer):
    unit_value = serializers.SerializerMethodField('empty')
    value = serializers.SerializerMethodField('empty')
    unit = UnitSerializer(many=True)

    def empty(self, *args):
        return ""

    class Meta:
        model = Attribute
        fields = '__all__'


class ClassificationSerializer(ModelSerializer):
    class Meta:
        model = Classification
        fields = '__all__'


class PartAttributeSerializer(serializers.Serializer):
    value = serializers.IntegerField()
    isOptional = serializers.BooleanField(allow_null=True)


class PartClassificationSerializer(serializers.Serializer):
    isOptional = serializers.BooleanField(allow_null=True)
    value = serializers.IntegerField()
    attribute = serializers.ListField(child=PartAttributeSerializer())


class PartSerializer(serializers.ModelSerializer):
    classifications = serializers.ListField(child=PartClassificationSerializer(), write_only=True)

    class Meta:
        model = Part
        fields = '__all__'

    def create(self, validated_data):
        """
        @param validated_data:
        @return:
        """
        # check slug uniqueness
        slug = slugify(validated_data['title'])
        if Part.objects.filter(slug=slug).exists():
            slug = slug + '-' + str(random.randint(1, 100))
        part_data = {'title': validated_data['title'], 'description': validated_data['description'], 'slug': slug}
        # store part data
        part = Part.objects.create(**part_data)
        for classifications in validated_data['classifications']:
            classification = dict(classifications)
            classification_data = {'part': part, 'classification_id': classification['value'],
                                   'is_optional': classification['isOptional']}
            # store part classification
            part_classification = PartClassification.objects.create(**classification_data)
            for attribute in classification['attribute']:
                if attribute['value'] != '':
                    attribute_data = {'part_classification': part_classification,
                                      'attribute_id': attribute['value'], 'is_optional': attribute['isOptional']}
                    # store part attribute
                    attribute = PartClassificationAttribute.objects.create(**attribute_data)
        return validated_data

    def update(self, instance, validated_data):
        slug = slugify(validated_data['title'])
        if Part.objects.filter(slug=slug).exists():
            slug = slug + '-' + str(random.randint(1, 100))
        instance.slug = slug
        instance.title = validated_data.get('title')
        instance.description = validated_data.get('description')
        part_classifications = PartClassification.objects.filter(part=instance)
        part_classifications.delete()
        for classifications in validated_data['classifications']:
            classification = dict(classifications)
            classification_data = {'part': instance, 'classification_id': classification['value'],
                                   'is_optional': classification['isOptional']}
            # store part classification
            part_classification = PartClassification.objects.create(**classification_data)
            for attribute in classification['attribute']:
                if attribute['value'] != '':
                    attribute_data = {'part_classification': part_classification,
                                      'attribute_id': attribute['value'], 'is_optional': attribute['isOptional']}
                    # store part attribute
                    attribute = PartClassificationAttribute.objects.create(**attribute_data)

        instance.save()
        return instance


class PartClassificationAttributeListSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(many=False)

    class Meta:
        model = PartClassificationAttribute
        fields = ('id', "attribute", "is_optional")


class PartClassificationListSerializer(serializers.ModelSerializer):
    classification = ClassificationSerializer(many=False)
    partclassificationattribute_set = PartClassificationAttributeListSerializer(many=True)

    class Meta:
        model = PartClassification
        fields = ('id', 'is_optional', 'classification', 'partclassificationattribute_set')


class PartDetailsSerializer(serializers.ModelSerializer):
    partclassification_set = PartClassificationListSerializer(many=True)

    class Meta:
        model = Part
        fields = ('id', 'title', 'slug', 'description', 'partclassification_set')
