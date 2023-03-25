from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from .serializers import (
    GroupOffersPostSerializer,
    GroupOffersGetSerializer,
    GroupOffersUpdateSerializer,
    MenuOffersPostSerializer,
    MenuOffersGetSerializer,
    MenuOffersUpdateSerializer,
    BranchOffersGetSerializer,
    BranchOffersUpdateSerializer,
    BranchOffersPostSerializer,
    ItemOffersUpdateSerializer,
    ItemOffersGetSerializer,
    ItemOffersPostSerializer
)
from .models import GroupOffers, BranchOffers, MenuOffers, ItemOffers
from branch.models import Branch
from django.db.models import Q


# Create your views here.


class BranchOffersView(ModelViewSet):
    queryset = BranchOffers.objects.all()

    def get_permissions(self):
        if self.action == "list" and self.request.user != AnonymousUser():
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            if Branch.objects.filter(Q(manager=self.request.user.id) | Q(company__owner=self.request.user.id)):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'destroy':
            return BranchOffersPostSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return BranchOffersUpdateSerializer
        else:
            return BranchOffersGetSerializer

    def get_queryset(self):
        if not self.action == 'list':
            queryset = BranchOffers.objects.filter(
                Q(branch__manager=self.request.user) | Q(branch__company__owner=self.request.user.id))
            return queryset
        else:
            return self.queryset


class GroupOffersView(ModelViewSet):
    queryset = GroupOffers.objects.all()

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            if Branch.objects.filter(Q(manager=self.request.user.id) | Q(company__owner=self.request.user.id)):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'destroy':
            return GroupOffersPostSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return GroupOffersUpdateSerializer
        else:
            return GroupOffersGetSerializer

    def get_queryset(self):
        if not self.action == 'list':
            queryset = GroupOffers.objects.filter(
                Q(meal__menu__branch__manager=self.request.user) |
                Q(meal__menu__branch__company__owner=self.request.user))
            return queryset


class MenuOffersView(ModelViewSet):
    queryset = MenuOffers.objects.all()

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            if Branch.objects.filter(Q(manager=self.request.user.id) | Q(company__owner=self.request.user.id)):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'destroy':
            return MenuOffersPostSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return MenuOffersUpdateSerializer
        else:
            return MenuOffersGetSerializer

    def get_queryset(self):
        if not self.action == 'list':
            queryset = MenuOffers.objects.filter(
                Q(menu__branch__manager=self.request.user) | Q(menu__branch__company__owner=self.request.user.id))
            return queryset
        else:
            return self.queryset


class ItemOffersView(ModelViewSet):
    queryset = ItemOffers.objects.all()

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            if Branch.objects.filter(Q(manager=self.request.user.id) | Q(company__owner=self.request.user.id)):
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'destroy':
            return ItemOffersPostSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return ItemOffersUpdateSerializer
        else:
            return ItemOffersGetSerializer

    def get_queryset(self):
        if not self.action == 'list':
            queryset = ItemOffers.objects.filter(
                Q(item__menu__branch__manager=self.request.user) |
                Q(item__menu__branch__company__owner=self.request.user))
            return queryset
        else:
            return self.queryset
