import os

from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import AnonymousUser

from branch.models import Branch
from company.models import Company
from .models import Subscription
from .serializers import SubscriptionGetSerializer, SubscriptionPostSerializer, SubscriptionUpdateSerializer


def confirm_subscription(email, data):
    subject = "Subscription Confirmation Email from MakeMyMenu.IO"
    message = "subscription confirmation message"
    html_message = render_to_string("email-template-subscription-plan.html",
                                    {"name": data[0], "package_name": data[1], "package_price": data[2],
                                     "package_validity": data[3], "expiry_date": data[4]})
    send_mail(subject, message, os.getenv("MAILHOST"), email, html_message=html_message)


def renew_subscription(email, data):
    subject = "Subscription Renewal Email from MakeMyMenu.IO"
    message = "subscription renewal confirmation message"
    html_message = render_to_string("email-template-subscription-renew.html",
                                    {"name": data[0], "package_name": data[1], "package_price": data[2],
                                     "package_validity": data[3], "expiry_date": data[4]})
    send_mail(subject, message, os.getenv("MAILHOST"), email, html_message=html_message)


# Create your views here.

class SubscriptionViewSet(ModelViewSet):
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = SubscriptionGetSerializer
    http_method_names = ['post', 'get']

    def get_permissions(self):
        # Todo:
        # create = self.request.user == Company.owner
        # update = when renewed ( not this viewset)
        # delete = self.request.user == Company.owner
        # retrieve = self.request.user == Company.owner
        # list = all
        if self.action == 'list' and self.request.user != AnonymousUser():
            permission_classes = self.permission_classes
        else:
            try:
                if Company.objects.get(owner=self.request.user):
                    permission_classes = self.permission_classes
                else:
                    permission_classes = [IsAdminUser]
            except:
                permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        # if self.action == 'list':
        #     return self.queryset
        # else:
        #     return self.queryset.filter(company__owner=self.request.user)
        return self.queryset.filter(branch__company__owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return SubscriptionGetSerializer
        else:
            return SubscriptionPostSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        print(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        print(serializer.data)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data['branch'] = Branch.objects.get(company__owner=self.request.user, is_default=True).id
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        subscription_object = serializer.save()
        subscription_level = subscription_object.subscription_level
        if subscription_level == 1:
            package_name = "Easy Menu"
        elif subscription_level == 2:
            package_name = "Creator Pro"
        elif subscription_level == 3:
            package_name = "Business Booster"
        elif subscription_level == 4:
            package_name = "Enterprise Excel"
        elif subscription_level == 5:
            package_name = "Custom"
        else:
            return Response(status=400)
        new_serializer = SubscriptionGetSerializer(subscription_object)
        data = [subscription_object.branch.company.owner.first_name,
                package_name,
                new_serializer.data['total'],
                "1 month",
                new_serializer.data['end_date']]
        confirm_subscription([subscription_object.branch.company.owner.email], data)
        try:
            return Response("success", status=200)
        except:
            return Response("error", status=400)


@api_view(['PATCH', 'PUT'])
def update_subscription(request):
    try:
        if not Subscription.objects.get(branch__company__owner=request.user):
            return Response("Invalid User for renewal", status=400)
    except:
        return Response("Invalid User for renewal", status=400)
    subscription_object = Subscription.objects.get(branch__company__owner=request.user)
    serializer = SubscriptionUpdateSerializer(subscription_object, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    subscription_object = serializer.save()
    if serializer.validated_data['subscription_level'] < subscription_object.subscription_level:
        return Response("Subscription level cannot be decreased", status=400)
    subscription_level = subscription_object.subscription_level
    if subscription_level == 1:
        package_name = "Easy Menu"
    elif subscription_level == 2:
        package_name = "Creator Pro"
    elif subscription_level == 3:
        package_name = "Business Booster"
    elif subscription_level == 4:
        package_name = "Enterprise Excel"
    elif subscription_level == 5:
        package_name = "Custom"
    else:
        return Response(status=400)
    new_serializer = SubscriptionGetSerializer(subscription_object)
    data = [subscription_object.branch.company.owner.first_name,
            package_name,
            new_serializer.data['total'],
            "1 month",
            new_serializer.data['end_date']]
    renew_subscription([subscription_object.branch.company.owner.email], data=data)
    return Response(serializer.data, status=200)
