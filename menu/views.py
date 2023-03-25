import random
from datetime import datetime, timedelta

from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from branch.models import Branch
from group.models import Group
from item.models import Item
from .models import MenuStat
from .serializers import *


# Create your views here.


class MenuView(ModelViewSet):
    queryset = Menu.objects.filter(is_deleted=False)
    serializer_class = MenuGetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ('post', 'get', 'patch', 'put')

    def get_permissions(self):
        # create = branch.company.owner/ manager
        # update = branch.company.owner/ manager
        # delete = branch.company.owner/ manager
        # retrieve = all(may change)
        # list = all( may change )

        if self.action == 'list' or self.action == 'retrieve' or self.request.user == AnonymousUser():
            permission_classes = self.permission_classes
        else:
            if Branch.objects.filter(
                    Q(company__owner=self.request.user) |
                    Q(manager=self.request.user)):
                permission_classes = self.permission_classes
            else:
                permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'destroy':
            return MenuPostSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return MenuUpdateSerializer
        else:
            return self.serializer_class

    def get_queryset(self):
        # if not self.action == 'list' or self.action == 'retrieve':
        #     queryset = self.queryset.filter(Q(branch__manager=self.request.user) |
        #                                     Q(branch__company__owner=self.request.user))
        #     return queryset
        # else:
        #     return self.queryset
        queryset = self.queryset.filter(Q(branch__manager=self.request.user) |
                                        Q(branch__company__owner=self.request.user)).distinct('id')
        return queryset

    def perform_create(self, serializer):
        menu_object = serializer.save()
        try:
            item = self.request.data.getlist('item')
            for i in item:
                item_object = Item.objects.get(id=int(i))
                menu_object.item.add(item_object)
        except:
            pass
        try:
            group = self.request.data.getlist('group')
            for i in group:
                group_object = Group.objects.get(id=int(i))
                menu_object.group.add(group_object)
            # serializer.validated_data['group'] = meals
        except:
            pass
        if Branch.objects.filter(manager=self.request.user):
            branch = Branch.objects.get(manager=self.request.user, is_deleted=False)
            menu_object.branch.add(branch)
            if Menu.objects.filter(branch=branch).count() == 1:
                PrimaryMenu.objects.update_or_create(branch=branch, menu=menu_object)
        elif Branch.objects.filter(company__owner=self.request.user):
            branches = Branch.objects.filter(company__owner=self.request.user, is_deleted=False)
            for branch in branches:
                menu_object.branch.add(branch)
                if Menu.objects.filter(branch=branch).count() == 1:
                    PrimaryMenu.objects.create(branch=branch, menu=menu_object)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        if not data['item'] and not data['group']:
            return Response("Must have at least one item or group", status=400)
        if not data['item']:
            for i in instance.item.all():
                instance.item.remove(i)
            data.pop('item')
        if not data['group']:
            for i in instance.group.all():
                instance.group.remove(i)
            data.pop('group')
        serializer = self.get_serializer(instance, data=data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        if Branch.objects.filter(company__owner=self.request.user):
            branches = Branch.objects.filter(company__owner=self.request.user)
            for branch in branches:
                instance.branch.remove(branch)
        elif Branch.objects.filter(manager=self.request.user):
            branch = Branch.objects.get(manager=self.request.user)
            instance.branch.remove(branch)
        else:
            return Response("genjam", status=400)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        check = []
        new_list = []
        for menu in serializer.data:
            for branch in menu["branch"]:
                if branch["id"] not in check:
                    check.append(branch["id"])
                    try:
                        p_menu = PrimaryMenu.objects.get(branch__id=branch["id"])
                    except PrimaryMenu.DoesNotExist:
                        p_menu = None
                    # print(serializer.data[0])
                    # menu_id = serializer.data[0]['id']
                    # serializer = MenuGetSerializer(Menu.objects.get(id=menu_id))
                    # print(serializer.data)
                    primary = False
                    if p_menu:
                        if p_menu.menu.id == menu['id']:
                            primary = True
                    data = {
                        'id': menu['id'],
                        'name': menu['name'],
                        'image': menu['image'],
                        'video_link': menu['video_link'],
                        'description': menu['description'],
                        'status': menu['status'],
                        'primary': primary,
                        'updated_at': menu['updated_at']
                    }
                    new_map = {"id": branch["id"],
                               "name": branch["name"],
                               "menu": [data],
                               }
                    new_list.append(new_map)
                else:
                    for x in new_list:
                        if x['id'] == branch["id"]:
                            try:
                                p_menu = PrimaryMenu.objects.get(branch__id=branch["id"])
                            except PrimaryMenu.DoesNotExist:
                                p_menu = None
                            primary = False
                            if p_menu:
                                if p_menu.menu.id == menu['id']:
                                    primary = True
                            data = {
                                'id': menu['id'],
                                'name': menu['name'],
                                'image': menu['image'],
                                'video_link': menu['video_link'],
                                'description': menu['description'],
                                'status': menu['status'],
                                'primary': primary,
                                'updated_at': menu['updated_at']
                            }
                            x['menu'].append(data)
        list2 = []
        for i in new_list:
            branch_object = Branch.objects.get(id=i['id'])
            if branch_object.manager == self.request.user:
                list2.append(i)
        if list2:
            return Response(list2, status=200)
        else:
            return Response(new_list, status=200)


class PrimaryMenuView(ModelViewSet):
    queryset = PrimaryMenu.objects.filter(is_deleted=False)
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PrimaryMenuSerializer
    http_method_names = ('post', 'get')

    def get_permissions(self):
        if self.action == 'create' and self.request.user != AnonymousUser():
            if Branch.objects.filter(Q(manager=self.request.user) | Q(company__owner=self.request.user)):
                permission_classes = [IsAuthenticatedOrReadOnly]
            else:
                permission_classes = [IsAdminUser]
        else:
            permission_classes = self.permission_classes

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        if not PrimaryMenu.objects.filter(branch=self.request.data['branch']):
            return super().create(request, *args, **kwargs)
        else:
            instance = PrimaryMenu.objects.get(branch=self.request.data['branch'])
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def pm_update(self, request):
        try:
            branch_id = int(request.data['branch'])
        except:
            return Response("branch id not provided", status=400)
        data = request.data.copy()
        try:
            data.pop('menu')
        except:
            pass
        name = request.data.get('promo_name')
        image = request.data.get('promo_image')
        video = request.data.get('promo_vid')
        if name:
            if image or video:
                primary_object = PrimaryMenu.objects.get(branch=branch_id)
                serializer = self.get_serializer(primary_object, data=data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            else:
                # no image or video
                return Response("No image or video provided", status=400)
        else:
            return Response("No name provided", status=400)


@api_view(['post'])
def counter(request):
    menu_id = request.data['menu_id']
    menu_object = Menu.objects.get(id=menu_id)
    menu_object.QR_counter = menu_object.QR_counter + 1
    menu_object.save()
    primary_object = PrimaryMenu.objects.filter(menu=menu_object)
    for primary in primary_object:
        primary.branch.QR_counter += 1
        primary.branch.save()
        company_id = primary.branch.company.id
        today = datetime.today()
        try:
            m_stat = MenuStat.objects.get(branch_id=primary.branch.id, company_id=primary.branch.company_id, date=today)
            m_stat.total += 1
            m_stat.save()
        except MenuStat.DoesNotExist:
            MenuStat.objects.create(branch_id=primary.branch.id,
                                    company_id=primary.branch.company_id, date=today, total=1)

    return Response("HIT " + str(menu_object.QR_counter), status=200)


@api_view(['get'])
@permission_classes([IsAuthenticated])
def set_primary(request):
    menu_id = request.GET.get('menu_id')
    branch_id = request.GET.get('branch_id')
    data = {
        "menu": menu_id,
        "branch": branch_id
    }
    serializer = PrimaryMenuSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    if Menu.objects.get(id=menu_id).status != "Available":
        return Response("Cannot set primary", status=400)
    serializer.save()
    return Response(serializer.validated_data, status=200)


@api_view(['get'])
def get_primary(request):
    branch_id = request.GET.get("branch_id")
    try:
        primary_object = PrimaryMenu.objects.get(branch=branch_id)
    except:
        return Response("invalid branch_id", status=400)
    serializer = PrimaryMenuSerializer(primary_object)
    return Response(serializer.data, status=200)


@api_view(['get'])
def get_menu(request):
    the_id = request.GET.get("id")
    menu = Menu.objects.get(id=the_id)
    menu = MenuGetSerializer(menu)
    return Response(menu.data, status=200)


@api_view(['get'])
def get_category_menu(request):
    """

    params -> id of the menu \n
    return -> check kor

    """
    the_id = request.GET.get("id")
    try:
        menu = Menu.objects.get(id=the_id)
        # menu = MenuGetSerializer(menu)
        item_category = {}
        group_category = {}
        category = {}
        category2 = {}

        for _item in menu.item.all():
            if _item.category.title() in item_category.keys():
                item_category[_item.category.title()].append(ItemGetSerializer(_item).data)
            else:
                item_category[_item.category.title()] = [ItemGetSerializer(_item).data]
        new_list = []
        for i, j in item_category.items():
            category["category"] = i
            category['items'] = j
            new_list.append(category)
            category = {}

        for _group in menu.group.all():
            if _group.category.title() in group_category.keys():
                group_category[_group.category.title()].append(GroupGetSerializer(_group).data)
            else:
                group_category[_group.category.title()] = [GroupGetSerializer(_group).data]
        new_list2 = []
        for i, j in group_category.items():
            category2["category"] = i
            category2['items'] = j
            new_list2.append(category2)
            category2 = {}

        if menu.image:
            image = menu.image.url
        else:
            image = None

        menu_obj = {
            'branch': [branch.name for branch in menu.branch.all()],
            'group_category': new_list2,
            'item_category': new_list,
            'name': menu.name,
            'description': menu.description,
            'status': menu.status,
            'image': image,
            'video_link': menu.video_link
        }
        return Response(menu_obj, status=200)
    except Menu.DoesNotExist:
        return Response({}, status=400)


@api_view(['post'])
def get_stat(request):
    try:
        branch_id = request.data['branch_id']
    except:
        branch_id = None
    try:
        company_id = request.data['company_id']
    except:
        company_id = None

    try:
        menu_id = request.data['menu_id']
    except:
        menu_id = None
    try:
        stat_type = request.data['stat_type']
    except:
        stat_type = None
    month = {}
    day = {}
    today = datetime.now()
    if stat_type is None:
        return Response({"msg": 'Invalid Stat Type', 'month': month, 'day': day}, status=400)
    if stat_type == 1:
        target_date = today - timedelta(days=7)
        for i in range(7):
            _date = target_date + timedelta(days=i+1)
            day[str(_date.date())] = 0
            month[_date.month] = 0
    elif stat_type == 2:
        target_date = today - timedelta(days=30)
        for i in range(30):
            _date = target_date + timedelta(days=i+1)
            day[str(_date.date())] = 0
            month[_date.month] = 0
    elif stat_type == 3:
        target_date = today - timedelta(days=365)
        for i in range(365):
            _date = target_date + timedelta(days=i+1)
            day[str(_date.date())] = 0
            month[_date.month] = 0
    else:
        return Response({"msg": 'Invalid Stat Type', 'month': month, 'day': day}, status=400)

    # if menu_id is not None:
    #     _stat = MenuStat.objects.filter(menu_id=menu_id,
    #                                     date__gte=target_date)
    if branch_id is not None:
        _stat = MenuStat.objects.filter(branch_id=branch_id,
                                        date__gte=target_date)
    elif company_id is not None:
        _stat = MenuStat.objects.filter(company_id=company_id,
                                        date__gte=target_date)
    else:
        return Response({'msg': 'No Branch or Company', 'month': month, 'day': day}, status=400)
    for stat in _stat:
        if str(stat.date) in day.keys():
            day[str(stat.date)] += stat.total
        else:
            day[str(stat.date)] = stat.total

        if stat.date.month in month.keys():
            month[stat.date.month] += stat.total
        else:
            month[stat.date.month] = stat.total
    return Response({'msg': f'Stat data for {stat_type}', 'month': month, 'day': day}, status=200)


@api_view(['post'])
def multiple_update(request):
    """
    post method -> body -> menus: [id(int)], status: status(char) \n
    response: 200, 400
    """
    try:
        menus = request.data['menus']
    except:
        return Response("provide menu list", status=400)
    status = None
    try:
        status = request.data['status']
    except:
        pass
    if status is None:
        return Response("No Status specified", status=400)
    else:
        for menu in menus:
            menu_object = Menu.objects.get(id=menu)
            menu_object.status = status
            menu_object.save()
    return Response("Menu successfully updated", status=200)


@api_view(['GET'])
def item_suggestions(request):
    """
    query params: 'menu_id': int, 'item_id': int \n
    return:  item list serialized randomly, max = 5
    """
    menu_id = request.GET.get('menu_id')
    item_id = request.GET.get('item_id')
    queryset = Menu.objects.get(id=menu_id).item.all().exclude(id=item_id).distinct('name')
    serializer = ItemGetSerializer(queryset, many=True)
    if len(list(queryset)) > 5:
        data = random.sample(serializer.data, 5)
    else:
        data = random.sample(serializer.data, len(list(queryset)))
    return Response(data, status=200)
