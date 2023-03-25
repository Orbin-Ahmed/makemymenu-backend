from rest_framework import serializers

from branch.models import Branch
from user.models import User, FAQ


class UserPostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'first_name',
                  'last_name',
                  'image',
                  'date_of_birth',
                  'nid',
                  'phone',
                  'email',
                  'password',
                  )


class UserFetchSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, allow_null=True, use_url=True, required=False)
    designation = serializers.SerializerMethodField()

    def get_designation(self, instance):
        if Branch.objects.filter(manager=instance):
            return "Manager"
        elif Branch.objects.filter(company__owner=instance):
            return "Owner"
        else:
            return None

    class Meta:
        model = User
        fields = ('id',
                  # 'username',
                  'first_name',
                  'last_name',
                  'image',
                  'date_of_birth',
                  'nid',
                  'designation',
                  'phone',
                  'email',
                  'created_at',
                  'updated_at',
                  'verified'
                  )


class UserUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, allow_null=True, use_url=True, required=False)
    password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'image',
                  'phone',
                  'date_of_birth',
                  'nid',
                  'password',
                  )


# class ContactUsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ContactUs
#         fields = ('subject', 'message')


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ('faq_question', 'faq_answer')
