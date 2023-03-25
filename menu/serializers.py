import re

from rest_framework import serializers

from branch.serializers import BranchGetSerializer
from group.serializers import GroupGetSerializer
from item.serializers import ItemGetSerializer
from offers.serializers import MenuOffersGetSerializer
from .models import Menu, PrimaryMenu


class MenuPostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    # item = ItemPostSerializer(many=True, required=False)
    # group = MealPostSerializer(many=True, required=False)

    class Meta:
        model = Menu
        fields = (
            'id',
            'name',
            # 'item',
            # 'group',
            # 'branch',
            # 'is_primary',
            'image',
            'video_link',
            'description',
            'status',
        )


class MenuUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = Menu
        fields = (
            'name',
            'image',
            'video_link',
            'description',
            'status',
            'item',
            'group'
            # 'is_primary',
            # 'offers'
        )


class MenuGetSerializer(serializers.ModelSerializer):
    offers = MenuOffersGetSerializer(read_only=True, many=True)
    branch = BranchGetSerializer(read_only=True, many=True)
    item = ItemGetSerializer(read_only=True, many=True)
    group = GroupGetSerializer(read_only=True, many=True)
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = Menu
        fields = (
            'id',
            'name',
            'branch',
            'item',
            'group',
            'image',
            'video_link',
            'QR_counter',
            'description',
            'offers',
            'status',
            # 'created_at',
            'updated_at',
        )


class PrimaryMenuSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='branch.company.name', read_only=True)
    company_logo = serializers.ImageField(source='branch.company.image', read_only=True, use_url=True)
    promo_image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    promo_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    promo_vid = serializers.URLField(allow_null=True, allow_blank=True, required=False)
    placeholder_item = serializers.CharField(source='branch.placeholder_item', required=False)
    placeholder_group = serializers.CharField(source='branch.placeholder_meals', required=False)

    def validate_promo_vid(self, value):
        youtube_regex = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+'
        if type(value) == str and value != "":
            if not re.match(youtube_regex, value):
                raise serializers.ValidationError('Invalid YouTube link')
        return value

    class Meta:
        model = PrimaryMenu
        fields = ('branch', 'company_name', 'company_logo', 'menu', 'promo_image',
                  'promo_name', 'promo_vid', 'placeholder_item', 'placeholder_group')
