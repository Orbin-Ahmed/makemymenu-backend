from django.db.models import Q
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.contrib.auth.models import AnonymousUser
from branch.models import Branch
from group.models import Group
from menu.models import Menu
from .models import Item
from .serializers import ItemGetSerializer, ItemUpdateSerializer, ItemPostSerializer


# Create your views here.


class ItemView(ModelViewSet):
    serializer_class = ItemGetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Item.objects.filter(is_deleted=False)
    http_method_names = ('post', 'get', 'put', 'patch')

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
            return ItemPostSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return ItemUpdateSerializer
        else:
            return self.serializer_class

    def get_queryset(self):
        if self.request.user == AnonymousUser():
            return self.queryset
        else:
            queryset = self.queryset.filter(
                Q(branch__manager=self.request.user) | Q(branch__company__owner=self.request.user)).distinct('id')
            return queryset

    @action(detail=False, methods=['POST'])
    def create_multiple(self, request):
        """
        post method -> body -> items: [{name, price, category  }]
        response: 201, 400
        """
        _list = self.request.data['items']
        response = []
        for item in _list:
            try:
                serializer = ItemPostSerializer(data=item)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                response.append(serializer.data)
            except:
                return Response("stopped at " + str(item), status=400)
        return Response(response, status=201)

    def perform_create(self, serializer):
        item_object = serializer.save()
        print(item_object.name)
        if Branch.objects.filter(company__owner=self.request.user):
            branches = Branch.objects.filter(company__owner=self.request.user, is_deleted=False)
            for branch in branches:
                item_object.branch.add(branch)
        elif Branch.objects.filter(manager=self.request.user):
            branch = Branch.objects.get(manager=self.request.user, is_deleted=False)
            item_object.branch.add(branch)
        else:
            return Response("genjam", status=400)

    @action(detail=False, methods=['GET'])
    def get_category(self, request):
        if Branch.objects.filter(company__owner=self.request.user):
            queryset = self.queryset.filter(branch__company__owner=self.request.user).distinct('category')
            serializer = ItemGetSerializer(queryset, many=True)
            category_list = []
            for x in serializer.data:
                category_list.append(x['category'])
        elif Branch.objects.filter(manager=self.request.user):
            queryset = self.queryset.filter(branch__manager=self.request.user).distinct('category')
            serializer = ItemGetSerializer(queryset, many=True)
            category_list = []
            for x in serializer.data:
                category_list.append(x['category'])
        else:
            category_list = None
        return Response(category_list)

    @action(detail=False, methods=['POST'])
    def delete_multiple(self, request):
        ids = request.data['id']
        for one_id in ids:
            int_id = int(one_id)
            item_object = Item.objects.get(id=int_id)
            if Menu.objects.filter(
                    item=item_object, is_deleted=False) and Group.objects.filter(item=item_object, is_deleted=False):
                return Response("This item belongs to some Menu and some Combo", status=400)
            elif Group.objects.filter(item=item_object, is_deleted=False):
                return Response("This item belongs to some Combo", status=400)
            elif Menu.objects.filter(item=item_object, is_deleted=False):
                return Response("This item belongs to some Menu", status=400)
            else:
                self.perform_destroy(item_object)
        return Response("Successfully deleted", status=200)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        if Branch.objects.filter(company__owner=self.request.user):
            branches = Branch.objects.filter(company__owner=self.request.user)
            for branch in branches:
                instance.branch.remove(branch)
        elif Branch.objects.filter(manager=self.request.user):
            branch = Branch.objects.get(manager=self.request.user)
            instance.branch.remove(branch)
        else:
            return Response("genjam", status=400)
        instance.full_clean()
        instance.save()


@api_view(['post'])
@permission_classes([IsAuthenticatedOrReadOnly])
def multiple_update(request):
    """
    post method -> body -> items: [id(int)], status: status(char), category: category(char)\n
    both status and category works, at least need one\n
    response: 200, 400
    """
    items = []
    try:
        items = request.data['items']
    except:
        pass
    if not items:
        return Response("No item list", status=400)
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
        for item in items:
            item_object = Item.objects.get(id=item)
            item_object.category = category
            item_object.save()
    if status is not None:
        for item in items:
            print(item)
            item_object = Item.objects.get(id=item)
            item_object.status = status
            item_object.save()
            print(item_object.status)
    return Response("Item successfully updated", status=200)
