import os

from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from .serializers import *
from .models import Company
import random
from django.contrib.auth.models import AnonymousUser


def ownership_transfer_email(to_email, from_email, name, token, company_id, company_name):
    subject = "Ownership Transfer email"
    message = "Ownership Transfer hobe"
    invitation_link = os.getenv('MANAGER_ACCEPT_URL') + 'user-sign-up/?company_id=' + company_id + "&email=" + str(to_email) + "&token=" + str(token)
    html_message1 = render_to_string("email-template-ownership-inform.html", {"name": name})
    html_message2 = render_to_string("email-template-ownership-transfer.html",
                                     {"Invitation_link": invitation_link, "company_name": company_name})
    email_from = os.getenv("MAILHOST")
    send_mail(subject, message, email_from, [from_email], html_message=html_message1)
    send_mail(subject, message, email_from, [to_email], html_message=html_message2)


# Create your views here.


class CompanyView(ModelViewSet):
    # Todo:
    # create = any
    # update = owner
    # delete = owner
    # retrieve = anyone [may change]
    # list = anyone [may change]
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CompanyPostSerializer
    http_method_names = ('post', 'get', 'patch', 'put')

    def get_permissions(self):
        if self.request.user == AnonymousUser():
            permission_classes = [IsAdminUser]
        else:
            if self.action == "update" or self.action == "partial_update":
                if self.queryset.filter(owner=self.request.user):
                    permission_classes = self.permission_classes
                else:
                    permission_classes = [IsAdminUser]
            else:
                if not self.request.user.verified:
                    permission_classes = [IsAdminUser]
                else:
                    permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        # Todo:
        # update = company__owner == self.request.user
        # delete = company__owner == self.request.user
        # retrieve = company__owner == self.request.user
        # list = anyone [may change]
        # try:
        #     if self.action == 'list':
        #         queryset = self.queryset
        #     else:
        #         queryset = self.queryset.filter(owner=self.request.user)
        # except:
        #     queryset = None
        queryset = self.queryset.filter(owner=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            return CompanyUpdateSerializer
        elif self.action == 'retrieve' or self.action == 'list':
            return CompanyGetSerializer
        else:
            return CompanyPostSerializer

    def create(self, request, *args, **kwargs):
        self.request.data['owner'] = self.request.user.id
        # try:
        #     email = self.request.data['email']
        # except:
        #     email = None
        # if email is None:
        #     self.request.data['email'] = self.request.user.email
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            trade_license = request.data['trade_license']
        except:
            trade_license = None
        if trade_license is None:
            return super().update(request, *args, **kwargs)
        else:
            if instance.trade_license is None or instance.trade_license == "":
                return super().update(request, *args, **kwargs)
            else:
                return Response("You have already updated your trade license once", status=400)

    # def perform_update(self, serializer):
    #     company_object = serializer.save()
    #     try:
    #         branch_object = Branch.objects.get(name=company_object.name)
    #         branch_object.email = company_object.email
    #         branch_object.phone = company_object.phone_no
    #         branch_object.address = company_object.address
    #         branch_object.save()
    #     except:
    #         pass


@api_view(['get'])
@permission_classes([IsAuthenticatedOrReadOnly])
def ownership_transfer(request):
    to_email = request.GET.get('email')
    from_email = request.user.email
    if to_email == from_email:
        return Response("you cannot transfer ownership to yourself", status=400)
    if not Company.objects.filter(owner__email=from_email):
        return Response("Not an owner", status=401)
    company_object = Company.objects.get(owner=request.user)
    token = random.randint(100000, 999999)
    try:
        TransferModel.objects.create(company=company_object, token=token, new_email=to_email)
    except:
        transfer_object = TransferModel.objects.get(company=company_object)
        transfer_object.delete()
        TransferModel.objects.create(company=company_object, token=token, new_email=to_email)
    name = company_object.owner.first_name + company_object.owner.last_name
    company_name = company_object.name
    company_id = company_object.id
    ownership_transfer_email(to_email, from_email, name, token,
                             company_id=str(company_id), company_name=company_object.name)
    return Response("Ownership transfer success", status=200)
