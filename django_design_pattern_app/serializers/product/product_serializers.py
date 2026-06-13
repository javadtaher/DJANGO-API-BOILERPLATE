from rest_framework import serializers


class ManageCategorySerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['add', 'delete'])
    name = serializers.CharField(required=False)
    slug = serializers.CharField()
    parent = serializers.CharField(required=False, allow_null=True)


class ManageProductSerializer(serializers.Serializer):
    action = serializers.CharField(required=True)
    name = serializers.CharField(max_length=255, required=True)
    slug = serializers.SlugField(max_length=255, required=True)
    category = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=False, allow_null=True)
    price = serializers.IntegerField(required=True)
