import re

from rest_framework import serializers

from branch.models import Branch
from item.serializers import ItemGetSerializer
# from offers.serializers import MealOffersGetSerializer
from .models import Group


class GroupPostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    video_link = serializers.URLField(allow_null=True, allow_blank=True, required=False)

    def validate_video_link(self, value):
        youtube_regex = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+'
        if type(value) == str and value != "":
            if not re.match(youtube_regex, value) or value is None:
                raise serializers.ValidationError('Invalid YouTube link')
        return value

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'item',
            'description',
            'price',
            'discount',
            'category',
            'image',
            'video_link',
            # 'offers',
            'status',
        )


class GroupBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ('name',)


class GroupGetSerializer(serializers.ModelSerializer):
    # offers = MealOffersGetSerializer(read_only=True, many=True)
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    item = ItemGetSerializer(read_only=True, many=True)
    branch = GroupBranchSerializer(many=True)

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'branch',
            'item',
            'description',
            'price',
            'discount',
            'category',
            'image',
            'video_link',
            # 'offers',
            'status',
            # 'created_at',
            'updated_at',
        )


class GroupUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    video_link = serializers.URLField(allow_null=True, allow_blank=True, required=False)

    def validate_video_link(self, value):
        youtube_regex = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+'
        if type(value) == str and value != "":
            if not re.match(youtube_regex, value):
                raise serializers.ValidationError('Invalid YouTube link')
        return value

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'description',
            'item',
            'price',
            'discount',
            'category',
            'image',
            'video_link',
            'status'
            # 'offers'
        )
