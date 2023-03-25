from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from django.contrib.auth.models import AnonymousUser

from menu.models import Menu
from .models import Group
from branch.models import Branch
from .serializers import GroupPostSerializer, GroupUpdateSerializer, GroupGetSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q


# Create your views here.


class GroupView(ModelViewSet):
    serializer_class = GroupGetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Group.objects.filter(is_deleted=False)
    http_method_names = ('post', 'get', 'patch', 'put')

    def get_permissions(self):
        # create = menu.branch.manager/ menu.branch.company.owner
        # update = menu.branch.manager/ menu.branch.company.owner
        # delete = menu.branch.manager/ menu.branch.company.owner
        # retrieve = all
        # list = all

        if self.action == 'retrieve':
            permission_classes = self.permission_classes
        else:
            if self.request.user != AnonymousUser():
                if Branch.objects.filter(
                        Q(manager=self.request.user.id) | Q(company__owner=self.request.user.id)):
                    permission_classes = self.permission_classes
                else:
                    permission_classes = [IsAdminUser]
            else:
                permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'destroy':
            return GroupPostSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return GroupUpdateSerializer
        else:
            return self.serializer_class

    def get_queryset(self):
        if self.request.user == AnonymousUser():
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(
                Q(branch__manager=self.request.user) | Q(branch__company__owner=self.request.user.id)).distinct('id')
        return queryset

    def perform_create(self, serializer):
        group_object = serializer.save()
        if Branch.objects.filter(company__owner=self.request.user):
            branches = Branch.objects.filter(company__owner=self.request.user, is_deleted=False)
            for branch in branches:
                group_object.branch.add(branch)
        elif Branch.objects.filter(manager=self.request.user):
            branch = Branch.objects.get(manager=self.request.user, is_deleted=False)
            group_object.branch.add(branch)
        else:
            return Response("genjam", status=400)

    @action(detail=False, methods=['GET'])
    def get_category(self, request):
        queryset = self.queryset.distinct('category')
        serializer = GroupGetSerializer(queryset, many=True)
        category_list = []
        for x in serializer.data:
            category_list.append(x['category'])
        return Response(category_list)

    @action(detail=False, methods=['POST'])
    def delete_multiple(self, request):
        ids = request.data.get('id')
        for one_id in ids:
            int_id = int(one_id)
            group_object = Group.objects.get(id=int_id)
            if Menu.objects.filter(group=group_object, is_deleted=False):
                return Response("This group belongs to some Menu", status=400)
            else:
                self.perform_destroy(group_object)
        return Response("Successfully deleted", status=200)

    def perform_destroy(self, instance):
        # this deletes meals from whole branch/ branches depending on manager/owner
        instance.is_deleted = True
        if Branch.objects.filter(company__owner=self.request.user):
            branches = Branch.objects.filter(company__owner=self.request.user)
            for branch in branches:
                instance.branch.remove(branch)
                instance.save()
        elif Branch.objects.filter(manager=self.request.user):
            branch = Branch.objects.get(manager=self.request.user)
            instance.branch.remove(branch)
            instance.save()
        else:
            return Response("genjam", status=400)


@api_view(['post'])
def multiple_update(request):
    """
    post method -> body -> meals: [id(int)], status: status(char), category: category(char)\n
    both status and category works, at least need one \n
    response: 200, 400
    """
    groups = []
    try:
        groups = request.data['groups']
    except:
        pass
    if not groups:
        return Response("No group list", status=400)
    category = None
    status = None
    try:
        category = request.data['category']
    except:
        pass
    try:
        status = request.data['status']
    except:
        pass
    if category is None and status is None:
        return Response("No category or Status specified", status=400)
    if category is not None:
        for group in groups:
            item_object = Group.objects.get(id=group)
            item_object.category = category
            item_object.save()
    if status is not None:
        for group in groups:
            item_object = Group.objects.get(id=group)
            item_object.status = status
            item_object.save()
    return Response("Group successfully updated", status=200)
