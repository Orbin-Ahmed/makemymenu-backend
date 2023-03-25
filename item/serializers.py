import re

from rest_framework import serializers

from branch.models import Branch
from .models import Item


class ItemPostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    video_link = serializers.URLField(allow_null=True, allow_blank=True, required=False)

    def validate_video_link(self, value):
        youtube_regex = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+'
        if type(value) == str and value != "":
            if not re.match(youtube_regex, value):
                raise serializers.ValidationError('Invalid YouTube link')
        return value

    class Meta:
        model = Item
        fields = (
            'id',
            'name',
            'description',
            'price',
            'discount',
            'category',
            'image',
            'video_link',
            'status',
            'barcode'
        )


class ItemBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ('name',)


class ItemGetSerializer(serializers.ModelSerializer):
    # offers = ItemOffersGetSerializer(read_only=True, many=True)
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    branch = ItemBranchSerializer(many=True)

    # def get_branch(self, instance):
    #     return [branch.name for branch in instance.objects.filter(branch=bra)]
    class Meta:
        model = Item
        fields = (
            'id',
            'name',
            'branch',
            'description',
            'price',
            'discount',
            'category',
            'image',
            'video_link',
            'barcode',
            # 'offers',
            'status',
            # 'created_at',
            'updated_at',
        )


class ItemUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    video_link = serializers.URLField(allow_null=True, allow_blank=True, required=False)

    def validate_video_link(self, value):
        youtube_regex = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+'
        if type(value) == str and value != "":
            if not re.match(youtube_regex, value):
                raise serializers.ValidationError('Invalid YouTube link')
        return value

    class Meta:
        model = Item
        fields = (
            'id',
            'name',
            'description',
            'price',
            'video_link',
            'barcode',
            'discount',
            'category',
            'image',
            'status',
        )
