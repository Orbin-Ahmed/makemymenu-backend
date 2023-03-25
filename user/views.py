import os
import random
from datetime import timedelta, datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.contrib.auth.models import AnonymousUser
from branch.models import Branch
from company.models import Company, TransferModel
from subscription.models import Subscription
from .models import User, Registration_verification, Password_verification, FAQ
from .serializers import UserPostSerializer, UserFetchSerializer, UserUpdateSerializer, FAQSerializer


def send_verification_email(user_object, token):
    subject = 'Email verification from MakeMyMenu'
    # message = f'Hi {user_object.first_name}, Congratulations on creating an account at MakeMyMenu.IO.\n' \
    #           f' Here is your OTP to verify your email and get started :{token}'
    html_message = render_to_string("email-template-welcome.html",
                                    {"verification_code": token, "name": user_object.first_name})
    message = f'{token}'
    email_from = os.getenv("MAILHOST")
    recipient_list = [user_object.email]
    # print(email_from, recipient_list)
    send_mail(subject, message, email_from, recipient_list, html_message=html_message)


def send_reset_email(user_object, token):
    subject = 'Password Reset from MakeMyMenu'
    # message = f'Hi {user_object.first_name}, this email is from MakeMyMenu.IO for a password reset request.\n' \
    #           f' Click this link to reset your password: makemymenu.io/reset-pass/{token}/'
    email_from = os.getenv("MAILHOST")
    message = f'{token}'
    html_message = render_to_string("email-template-reset-pass.html",
                                    {"Invitation_link": os.getenv("MANAGER_ACCEPT_URL") + 'reset-pass/' + str(token),
                                     "name": user_object.first_name})
    recipient_list = [user_object.email]
    # print(email_from, recipient_list)
    send_mail(subject, message, email_from, recipient_list, html_message=html_message)


# Create your views here.


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserPostSerializer
    permission_classes = [AllowAny]
    http_method_names = ('post', 'get', 'patch', 'put')

    # create = anyone
    # read (retrieve/list) = self
    # update = self.verified

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = self.permission_classes
        elif self.action == 'update' and self.request.user!=AnonymousUser():
            if self.request.user.verified:
                permission_classes = [IsAuthenticatedOrReadOnly]
            else:
                permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'destroy':
            return UserPostSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return UserUpdateSerializer
        else:
            return UserFetchSerializer

    def get_queryset(self):
        if self.action == 'retrieve' or self.action == 'list':
            queryset = User.objects.filter(id=self.request.user.id)
        else:
            queryset = self.queryset
        return queryset

    def perform_create(self, serializer):
        # Hash password but passwords are not required
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
        else:
            return Response("invalid password provided", status=400)
        serializer.validated_data['username'] = self.request.data['email']
        serializer.validated_data['password'] = password
        token = random.randint(100000, 999999)
        user_object = serializer.save()
        Registration_verification.objects.create(token=token, user=user_object)
        send_verification_email(user_object, token)

    def perform_update(self, serializer):
        # Hash password but passwords are not required
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        if 'nid' in self.request.data:
            if self.request.data['nid'] == '':
                serializer.save(nid=None)
        serializer.save()


@api_view(['get'])
@permission_classes([IsAuthenticated])
def user_token(request):
    permission_classes([IsAuthenticated])
    serializer = UserFetchSerializer(request.user)
    # serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=200)


@api_view(['post'])
def login_view(request):
    try:
        email = request.data['email']
        password = request.data['password']
    except:
        return Response("must provide all data", status=404)
    try:
        username = User.objects.get(email=email).username
        user = authenticate(request, username=username, password=password)
    except:
        return Response("Invalid credentials", status=404)
    if user is None:
        return Response("invalid credentials", status=401)
    elif not user.verified:
        token = random.randint(100000, 999999)
        reg_object = Registration_verification.objects.filter(user=user)
        for reg in reg_object:
            reg.delete()
        Registration_verification.objects.create(token=token, user=user)
        send_verification_email(user, token)
        return Response("Unverified user", status=418)
    else:
        login(request, user)
        try:
            Token.objects.filter(user=user).delete()
        except:
            pass
        token = Token.objects.create(user=user)
        return Response({"Token": token.key}, status=200)


@api_view(['get'])
@permission_classes([IsAuthenticatedOrReadOnly])
def logout_view(request):
    Token.objects.filter(user=request.user).delete()
    return Response("Successfully logged out", status=200)


@api_view(['GET', 'POST'])
def register_verify(request):
    if request.method == 'POST':
        try:
            email = request.data["email"]
            otp = request.data["token"]
        except:
            return Response("Invalid data", status=400)
        tokens = Registration_verification.objects.all()
        for x in tokens:
            expire_date = x.created_at + timedelta(days=1)
            if expire_date < timezone.now():
                x.delete()
        try:
            user = User.objects.get(email=email)
            tok = Registration_verification.objects.get(token=otp, user=user)
        except:
            return Response("Invalid token", status=400)
        user.verified = True
        user.save()
        tok.delete()
        tok = Token.objects.create(user=user)
        return Response({
            "Token": tok.key
        }, status=202)
    else:
        token = random.randint(100000, 999999)
        try:
            email = request.GET.get('email')
        except:
            return Response("Invalid input", status=400)
        registration_object = Registration_verification.objects.filter(user__email=email)
        if registration_object:
            for x in registration_object:
                x.delete()
        try:
            user_object = User.objects.get(email=email)
        except:
            return Response("user does not exist", status=400)
        Registration_verification.objects.create(token=token, user=user_object)
        send_verification_email(user_object, token)
        return Response("success", status=200)


@api_view(['GET'])
def user_summary(request):
    user_email = request.GET.get('email')
    try:
        user_object = User.objects.get(email=user_email)
    except:
        return Response("Invalid input", status=400)
    information = []
    if user_object.verified:
        information.append({"verified": True})
    else:
        information.append({"verified": False})
    if Branch.objects.filter(manager=user_object):
        information.append({"is_manager": True})
    else:
        information.append({"is_manager": False})
    if Company.objects.filter(owner=user_object):
        information.append({"has_company": True})
    else:
        information.append({"has_company": False})
    if Branch.objects.filter(company__owner=user_object):
        information.append({"has_branch": True})
    else:
        information.append({"has_branch": False})
    if Subscription.objects.filter(branch__company__owner=user_object):
        information.append({"has_subscription": True})
    else:
        information.append({"has_subscription": False})
    return Response(information, status=200)


@api_view(['GET', 'POST'])
def reset_password(request):
    if request.method == 'GET':
        email = request.GET.get("email")
        try:
            user = User.objects.get(email=email)
        except:
            return Response("invalid email", status=400)
        token = random.randint(100000, 999999)
        if Password_verification.objects.filter(user=user):
            x = Password_verification.objects.filter(user=user)
            for y in x:
                y.delete()
        Password_verification.objects.create(user=user, token=token)
        send_reset_email(user, token)
        return Response("ok", status=200)
    else:
        try:
            password = request.data['password']
            token = request.data['token']
        except:
            return Response("invalid input", status=400)
        try:
            reset_object = Password_verification.objects.get(token=token)
        except:
            return Response("invalid token", status=400)
        reset_object.user.set_password(password)
        reset_object.user.save()
        reset_object.delete()
        return Response("done", status=200)


class ManagerCreateView(ModelViewSet):
    serializer_class = UserPostSerializer
    http_method_names = 'post'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        value = self.perform_create(serializer)
        return value

    def perform_create(self, serializer):
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
        else:
            return Response("invalid password provided", status=400)

        serializer.validated_data['username'] = serializer.validated_data['email']
        serializer.validated_data['password'] = password
        branch_object = None
        company_object = None
        try:
            branch_object = Branch.objects.get(id=self.request.data['branch_id'], is_deleted=False)
        except:
            pass
        try:
            company_object = Company.objects.get(id=self.request.data['company_id'], is_deleted=False)
        except:
            pass
        user_object = serializer.save()
        user_object.verified = True
        user_object.save()
        if branch_object is not None:
            branch_object.manager = user_object
            branch_object.save()
            token = Token.objects.update_or_create(user=branch_object.manager)
            token2 = list(token)[0]
            return Response({
                "token": str(token2)}, status=200)
        elif company_object is not None:
            try:
                transfer_object = TransferModel.objects.get(company=company_object,
                                                            token=self.request.data['token'],
                                                            new_email=self.request.data['email'])
            except:
                return Response("Invalid sign-up", status=400)
            if timezone.now() <= transfer_object.created_at + timedelta(hours=24):
                return Response("you need to wait 24 hours to sign-up", status=400)
            old_email = company_object.owner.email
            old_name = company_object.owner.first_name
            company_object.owner = user_object
            company_object.email = user_object.email
            company_object.phone_no = user_object.phone
            company_object.save()
            new_email = company_object.owner.email
            subject = "Company ownership transfer completed"
            message = "Company ownership transfer completed"
            html_message = render_to_string("email-template-ownership-transfer-success.html",
                                            {"name": company_object.owner.first_name})
            html_message2 = render_to_string("email-template-ownership-transfer-success.html",
                                            {"name": old_name})
            send_mail(subject, message, os.getenv("MAILHOST"), [new_email], html_message=html_message)
            send_mail(subject, message, os.getenv("MAILHOST"), [old_email], html_message=html_message2)
            token = Token.objects.update_or_create(user=company_object.owner)
            return Response({
                "token": token[0].key}, status=200)
        else:
            user_object.delete()
            return Response(serializer.data, status=400)


@api_view(['get'])
def TnC(request):
    file1 = open('TnC.txt', 'r')
    lines = file1.readlines()
    text = []
    # Strips the newline character
    for line in lines:
        response = {}
        line = line.strip('\n')
        line = line.split(':')
        response["title"] = line[0]
        response["value"] = line[1]
        text.append(response)
    return Response(text, status=200)


@api_view(['get'])
def about_us(request):
    file1 = open('AboutUs.txt', 'r')
    lines = file1.readlines()
    response = []
    for line in lines:
        response.append(line.strip('\n'))
    return Response(response, status=200)


class FAQView(ModelViewSet):
    queryset = FAQ.objects.all()
    # permission_classes = [IsAdminUser, IsAuthenticatedOrReadOnly]
    serializer_class = FAQSerializer
    http_method_names = ['GET']


@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def feedback(request):
    subject = request.data['subject']
    message = request.data['message']
    html_message1 = render_to_string("email_template_feedback.html", {"subject": subject, "description": message})
    html_message2 = render_to_string("email_template_feedback_admin.html", {"subject": subject, "description": message})
    send_mail(subject, message, os.getenv("MAILHOST"), [os.getenv("MAILHOST")], html_message=html_message2)
    send_mail(subject, message, os.getenv("MAILHOST"), [request.user.email], html_message=html_message1)
    return Response("sent feedback", status=200)


@api_view(['POST'])
def contact_us(request):
    name = request.data["name"]
    subject = request.data["subject"]
    email = request.data["email"]
    message = request.data["message"]
    html_message1 = render_to_string("email_template_contact_us_user.html", {"name": name})
    html_message2 = render_to_string("email_template_contact_us_admin.html",
                                     {"name": name, "user_name": name, "subject": subject, "Description": message})
    send_mail(subject, message, os.getenv("MAILHOST"), [os.getenv("MAILHOST")], html_message=html_message2)
    send_mail(subject, message, os.getenv("MAILHOST"), [email], html_message=html_message1)
    return Response("sent Contact Info and message", status=200)
