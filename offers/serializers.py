from rest_framework import serializers

from .models import GroupOffers, BranchOffers, MenuOffers, ItemOffers


class GroupOffersPostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = GroupOffers
        fields = (
            'id',
            'name',
            'image',
            'description',
            'discount',
            'group',
            'start_date',
            'end_date',
        )


class BranchOffersPostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = BranchOffers
        fields = (
            'id',
            'name',
            'image',
            'description',
            'discount',
            'branch',
            'start_date',
            'end_date',
        )


class MenuOffersPostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = MenuOffers
        fields = (
            'id',
            'name',
            'image',
            'description',
            'discount',
            'menu',
            'start_date',
            'end_date',
        )


class ItemOffersPostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = ItemOffers
        fields = (
            'id',
            'name',
            'image',
            'description',
            'discount',
            'item',
            'start_date',
            'end_date',
        )


class GroupOffersUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = GroupOffers
        fields = (
            'id',
            'name',
            'image',
            'description',
            'discount',
            'start_date',
            'end_date',
        )


class BranchOffersUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = BranchOffers
        fields = (
            'id',
            'name',
            'image',
            'description',
            'discount',
            'start_date',
            'end_date',
        )


class MenuOffersUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = MenuOffers
        fields = (
            'id',
            'name',
            'image',
            'description',
            'discount',
            'start_date',
            'end_date',
        )


class ItemOffersUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = ItemOffers
        fields = (
            'id',
            'name',
            'image',
            'description',
            'discount',
            'start_date',
            'end_date',
        )


class MenuOffersGetSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = MenuOffers
        fields = (
            'id',
            'name',
            'image',
            'description',
            'menu',
            'discount',
            'start_date',
            'end_date',
            'created_at',
            'updated_at',
        )


class GroupOffersGetSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = GroupOffers
        fields = (
            'id',
            'name',
            'image',
            'description',
            'group',
            'discount',
            'start_date',
            'end_date',
            'created_at',
            'updated_at',
        )


class BranchOffersGetSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = BranchOffers
        fields = (
            'id',
            'name',
            'image',
            'description',
            'branch',
            'discount',
            'start_date',
            'end_date',
            'created_at',
            'updated_at',
        )


class ItemOffersGetSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = ItemOffers
        fields = (
            'id',
            'name',
            'image',
            'description',
            'item',
            'discount',
            'start_date',
            'end_date',
            'created_at',
            'updated_at',
        )
