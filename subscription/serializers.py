from branch.models import Branch
from branch.serializers import BranchGetSerializer
from company.serializers import CompanyGetSerializer
from .models import Subscription
from rest_framework import serializers
import os


class SubscriptionGetSerializer(serializers.ModelSerializer):
    subscriber = serializers.CharField(source='branch.company.name')
    total = serializers.SerializerMethodField(read_only=True)
    branches = serializers.SerializerMethodField(read_only=True)

    def get_branches(self, instance):
        company = instance.branch.company
        branch_list = Branch.objects.filter(company=company, is_deleted=False)
        return len(branch_list)

    def get_total(self, instance):
        level_1 = os.getenv('LEVEL1')
        level_2 = os.getenv('LEVEL2')
        level_3 = os.getenv('LEVEL3')
        level_4 = os.getenv('LEVEL4')
        level_5 = os.getenv('LEVEL5')
        level = instance.subscription_level
        if level == 1:
            price = level_1
        elif level == 2:
            price = level_2
        elif level == 3:
            price = level_3
        elif level == 4:
            price = level_4
        elif level == 5:
            price = level_5
        else:
            raise Exception
        if level > 2:
            branch_list = Branch.objects.filter(company=instance.branch.company, is_deleted=False)
            if len(branch_list) < 1:
                price = float(price)
            else:
                price = len(branch_list) * float(price)
        return str(price)

    class Meta:
        model = Subscription
        fields = (
            'id',
            'subscriber',
            'branches',
            'subscription_level',
            'start_date',
            'end_date',
            'total',
            # 'payment_method',
            # 'payment_id',
            # 'created_at',
            # 'updated_at'
        )


class SubscriptionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = (
            'id',
            'branch',
            'subscription_level',
            'start_date',
            'end_date',
            'payment_method',
            'payment_id',
        )


class SubscriptionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = (
            'id',
            'subscription_level',
            'payment_method',
            'payment_id'
        )
