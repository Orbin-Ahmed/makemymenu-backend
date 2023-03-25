import base64
import io
import os

from PIL import Image
from django.contrib.auth.models import AnonymousUser
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import render_to_string
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from company.models import Company
from user.models import User
from .models import Branch, Localization, Date_time_format, Notification_settings
from .serializers import (BranchGetSerializer, BranchUpdateSerializer, BranchPostSerializer,
                          LocalizationSerializer, FormatSerializer, Notification_settingsSerializer)


def converter(image):
    im = Image.open(image)
    # Create a BytesIO object to hold the image data in memory
    buffer = io.BytesIO()

    # Save the image in WebP format to the buffer
    im.save(buffer, "png")

    # Seek to the start of the buffer so the data can be read
    buffer.seek(0)

    return buffer


def send_email(manager_email, branch_object, data):
    subject = f'Invite to be Branch Manager for {branch_object.company.name}'
    message = f'Invitation for manager'
    url = os.getenv("MANAGER_ACCEPT_URL") + 'user-sign-up/?branch_id=' + str(data["branch_id"]) + "&email=" + str(
        data["email"])
    html_message = render_to_string("email-template-branch-manager-invite.html",
                                    {'company_name': branch_object.company.name, 'Invitation_link': url})
    email_from = os.getenv("MAILHOST")
    recipient_list = [manager_email]
    send_mail(subject, message, email_from, recipient_list, html_message=html_message)


# Create your views here.


class BranchView(ModelViewSet):
    queryset = Branch.objects.filter(is_deleted=False)
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = BranchGetSerializer

    def get_queryset(self):
        # Todo:
        # update = authenticatedUser
        # delete = Company.Owner__is_boss
        # retrieve = authenticatedUser
        # list = anyone [may change]
        try:
            if self.action == 'destroy':
                queryset = self.queryset.filter(company__owner=self.request.user)
            else:
                queryset = self.queryset.filter(Q(manager=self.request.user) |
                                                Q(company__owner=self.request.user))
        except:
            queryset = self.queryset
        return queryset

    def get_permissions(self):
        # create = if company.owner == self.request.user & branch<1
        # update = branch.company.owner , branch.manager
        # delete = branch.company.owner
        # read = all
        if self.action == 'create' and self.request.user != AnonymousUser():
            try:
                if Company.objects.get(owner=self.request.user) and \
                        len(Branch.objects.filter(company__owner=self.request.user, is_deleted=False).values()) < 1:
                    permissions = self.permission_classes
                else:
                    try:
                        branch_object = Branch.objects.filter(company__owner=self.request.user, is_deleted=False)
                        if branch_object.first().company.subscription.subscription_level > 2:
                            permissions = self.permission_classes
                        else:
                            permissions = [IsAdminUser]
                    except:
                        permissions = [IsAdminUser]
            except:
                permissions = [IsAdminUser]

        elif (self.action == 'partial_update' or self.action == 'update') and self.request.user != AnonymousUser():
            try:
                if Branch.objects.filter(
                        (Q(company__owner=self.request.user) | Q(manager=self.request.user)) & Q(is_deleted=False)):
                    permissions = self.permission_classes
                else:
                    permissions = [IsAdminUser]
            except AttributeError:
                permissions = [IsAdminUser]

        elif self.action == 'destroy' and self.request.user != AnonymousUser():
            try:
                if Branch.objects.filter(company__owner=self.request.user, is_deleted=False):
                    permissions = self.permission_classes
                else:
                    permissions = [IsAdminUser]
            except:
                permissions = [IsAdminUser]

        else:
            permissions = self.permission_classes

        return [permission() for permission in permissions]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'destroy':
            return BranchPostSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return BranchUpdateSerializer
        else:
            return self.serializer_class

    def create(self, request, *args, **kwargs):
        company_object = Company.objects.get(owner=self.request.user)
        request.data['company'] = company_object.id
        if not Branch.objects.filter(company=company_object):
            request.data['name'] = "Default Branch"
            # request.data['address'] = company_object.address
            # request.data['email'] = company_object.email
            # request.data['phone'] = company_object.phone_no
            request.data['title'] = "HQ"
            request.data["email"] = self.request.user.email
            request.data["is_default"] = True
            return super().create(request, *args, **kwargs)
        else:
            if Branch.objects.filter(email=self.request.data['email']):
                return Response({
                    "message": "Branch with this email address already exists"}, status=400)
            try:
                email = self.request.data['email']
            except:
                email = None
            if email is None:
                self.request.data['email'] = self.request.user.email
            return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        branch_object = serializer.save()
        Localization.objects.create(branch=branch_object)
        Date_time_format.objects.create(branch=branch_object)
        Notification_settings.objects.create(branch=branch_object)
        try:
            manager_email = self.request.data['manager']
            data = {
                "email": manager_email,
                "branch_id": branch_object.id
            }
            send_email(manager_email, branch_object, data)
        except:
            pass

    # def perform_update(self, serializer):
    #     branch_object = serializer.save()
    #     if branch_object.company.owner == self.request.user:
    #         company_object = branch_object.company
    #         if branch_object.name == company_object.name:
    #             company_object.email = branch_object.email
    #             company_object.phone_no = branch_object.phone
    #             company_object.address = branch_object.address
    #             company_object.save()

    def destroy(self, request, *args, **kwargs):
        # branches = Branch.objects.filter(company__owner=self.request.user)
        instance = self.get_object()
        if not instance.is_default:
            return super().destroy(request, *args, **kwargs)
        else:
            return Response("you cannot delete default branch", status=400)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    @action(detail=False, methods=['POST'])
    def qr_update(self, request):
        image = request.POST.get('QR')
        format, imgstr = image.split(';base64,')
        ext = format.split('/')[-1]

        data = ContentFile(base64.b64decode(imgstr))

        if Branch.objects.filter(company__owner=self.request.user):
            branch_list = Branch.objects.filter(company__owner=self.request.user)
            for branch in branch_list:
                file_name = str(branch.id) + '.' + ext
                branch.QR.save(file_name, data, save=True)
        elif Branch.objects.filter(manager=self.request.user):
            branch = Branch.objects.get(manager=self.request.user)
            file_name = str(branch.id) + '.' + ext
            branch.QR.save(file_name, data, save=True)
        else:
            return Response("jhamela", status=400)
        return Response("Successfully Updated QR", status=200)

    @action(detail=False, methods=['POST'])
    def wifi_update(self, request):
        image = request.POST.get('Wifi')
        format, imgstr = image.split(';base64,')
        ext = format.split('/')[-1]

        data = ContentFile(base64.b64decode(imgstr))

        if Branch.objects.filter(company__owner=self.request.user):
            branch_list = Branch.objects.filter(company__owner=self.request.user)
            for branch in branch_list:
                file_name = str(branch.id) + '.' + ext
                branch.Wifi.save(file_name, data, save=True)
        elif Branch.objects.filter(manager=self.request.user):
            branch = Branch.objects.get(manager=self.request.user)
            file_name = str(branch.id) + '.' + ext
            branch.Wifi.save(file_name, data, save=True)
        else:
            return Response("jhamela", status=400)
        return Response("Successfully Updated QR", status=200)


class localizationView(ModelViewSet):
    queryset = Localization.objects.filter(is_deleted=False)
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = LocalizationSerializer
    http_method_names = ('get', 'patch')

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(branch=kwargs['pk'])
        except:
            return Response("no branch id provided", status=400)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = self.queryset.get(branch=kwargs['pk'])
        except:
            return Response("no branch id provided", status=400)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class FormatView(ModelViewSet):
    queryset = Date_time_format.objects.filter(is_deleted=False)
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = FormatSerializer
    http_method_names = ('get', 'patch')

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(branch=kwargs['pk'])
        except:
            return Response("no branch id provided", status=400)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = self.queryset.get(branch=kwargs['pk'])
        except:
            return Response("no branch id provided", status=400)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class Notification_settingsView(ModelViewSet):
    queryset = Notification_settings.objects.filter(is_deleted=False)
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = Notification_settingsSerializer
    http_method_names = ('get', 'patch')

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(branch=kwargs['pk'])
        except:
            return Response("no branch id provided", status=400)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = self.queryset.get(branch=kwargs['pk'])
        except:
            return Response("no branch id provided", status=400)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


@api_view(['post'])
@permission_classes([IsAuthenticated])
def manager_invite(request):
    manager_email = request.data['email']
    branch_object = Branch.objects.get(company__owner=request.user)
    if User.objects.filter(email=manager_email):
        return Response("User with this email already exists", status=400)

    data = {
        "email": manager_email,
        "branch_id": branch_object.id
    }

    send_email(manager_email, branch_object, data)
    return Response("success", status=200)


@api_view(['get'])
def get_qr(request):
    branch_id = request.GET.get('branch_id')
    branch_object = Branch.objects.get(id=branch_id)

    menu = None
    wifi = None
    try:
        menu = request.GET.get('menu')
    except:
        pass
    try:
        wifi = request.GET.get('wifi')
    except:
        pass
    if menu is None:
        wifi = branch_object.Wifi
        converted = converter(wifi)
        file_name = wifi.name.split(".")[0]
        file_name = file_name + ".png"
        image = ImageFile(io.BytesIO(converted.read()), name=file_name)
        return Response(image, status=200)

    elif wifi is None:
        menu = branch_object.QR
        converted = converter(menu)
        file_name = menu.name.split(".")[0]
        file_name = file_name + ".png"
        image = ImageFile(io.BytesIO(converted.read()), name=file_name)
        return Response(image, status=200)

    elif menu is not None and wifi is not None:
        return Response("Duitai disos", status=400)
    else:
        return Response("kisui des nai", status=400)
