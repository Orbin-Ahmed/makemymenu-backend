from rest_framework import serializers

from branch.models import Branch
from company.models import Company, TransferModel
from user.serializers import UserFetchSerializer


class CompanyPostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = Company
        fields = (
            'id',
            'owner',
            'name',
            'image',
            'trade_license',
            'type',
            'type_status'
        )


class CompanyUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = Company
        fields = (
            # 'name',
            # 'address',
            'image',
            # 'phone_no',
            'trade_license'
        )


class CompanyGetSerializer(serializers.ModelSerializer):
    owner = UserFetchSerializer(read_only=True)
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    total_branch = serializers.SerializerMethodField()

    def get_total_branch(self, instance):
        branches = Branch.objects.filter(company=instance)
        return branches.count()

    class Meta:
        model = Company
        fields = (
            'id',
            'owner',
            'name',
            'image',
            'total_branch',
            # 'address',
            # 'phone_no',
            # 'email',
            'trade_license',
            'type',
            'type_status',
            # 'created_at',
            # 'updated_at'
        )
