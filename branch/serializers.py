from rest_framework import serializers
from branch.models import Branch, Localization, Date_time_format, Notification_settings
from company.serializers import CompanyGetSerializer
from user.serializers import UserFetchSerializer


class BranchPostSerializer(serializers.ModelSerializer):
    # QR = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    # email = serializers.EmailField(required=False)
    is_default = serializers.BooleanField(required=False)

    class Meta:
        model = Branch
        fields = (
            'id',
            # 'manager',
            'company',
            # 'QR',
            'name',
            'address',
            'phone',
            'email',
            'title',
            'is_default'
        )


class BranchUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = (
            'name',
            'address',
            'title',
            'phone',
            'placeholder_item',
            'placeholder_meals'
        )


class BranchGetSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.name')
    # company_email = serializers.CharField(source='company.email')
    manager_email = serializers.CharField(source='manager.email', allow_null=True)
    manager_name = serializers.CharField(source='manager.get_name', allow_null=True)
    manager_phone = serializers.CharField(source='manager.phone', allow_null=True)
    QR = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    Wifi = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    # total = serializers.SerializerMethodField()
    #
    # def get_total(self, instance):
    #     instance.menu
    class Meta:
        model = Branch
        fields = (
            'id',
            'company',
            # 'company_email',
            'manager_email',
            'manager_name',
            'manager_phone',
            'name',
            'address',
            'phone',
            'email',
            'title',
            'QR',
            'QR_counter',
            'Wifi'
        )


class LocalizationSerializer(serializers.ModelSerializer):
    country = serializers.CharField(required=False)
    time_zone = serializers.CharField(required=False)
    currency = serializers.CharField(required=False)
    language = serializers.CharField(required=False)

    class Meta:
        model = Localization
        fields = ('branch', 'country', 'time_zone', 'currency', 'language')


class FormatSerializer(serializers.ModelSerializer):
    date_format = serializers.CharField(required=False)
    currency_precision = serializers.CharField(required=False)
    time_format = serializers.CharField(required=False)
    number_format = serializers.CharField(required=False)
    begin_week = serializers.CharField(required=False)

    class Meta:
        model = Date_time_format
        fields = ('branch', 'date_format', 'currency_precision', 'time_format', 'number_format', 'begin_week')


class Notification_settingsSerializer(serializers.ModelSerializer):
    system_update = serializers.BooleanField(required=False)
    change_log = serializers.BooleanField(required=False)

    class Meta:
        model = Notification_settings
        fields = ('branch', 'system_update', 'change_log')
