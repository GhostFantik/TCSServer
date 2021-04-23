from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from Repairs.serializers import RepairRequestSerializer, RepairSerializer, TagSerializer, TypeRepairSerializer
from Repairs.models import RepairRequest, Repair, Tag, TypeRepair
from Auth.permissions import (IsReadOnlyAllRolePermission, IsMechanicPermission, IsAdminPermission)
from Auth.models import User


# GET - All POST - Admin PATCH - Admin, DELETE - nobody
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsReadOnlyAllRolePermission|IsAdminPermission|IsAdminUser]
    http_method_names = ['get', 'post', 'head', 'options', 'patch']


# GET - ALL POST - superuser, READONLY delete - nobody, patch - nobody
class TypeRepairViewSet(viewsets.ModelViewSet):
    queryset = TypeRepair.objects.all()
    serializer_class = TypeRepairSerializer
    permission_classes = [IsReadOnlyAllRolePermission|IsAdminUser]
    http_method_names = ['get', 'post', 'head', 'options']


# GET - All, POST - All
class RepairRequestViewSet(mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    queryset = RepairRequest.objects.all()
    serializer_class = RepairRequestSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        user: User = self.request.user
        if user.role == 'C':
            return RepairRequest.objects.filter(car__user__username=user.username).all()
        return RepairRequest.objects.all()


# GET - all, POST - Admin, Mechanic, PATCH - Admin, Mechanic, DELETE - Admin, Mechanic
class RepairViewSet(viewsets.ModelViewSet):
    queryset = Repair.objects.all()
    serializer_class = RepairSerializer
    permission_classes = [IsReadOnlyAllRolePermission|IsMechanicPermission|IsAdminPermission|IsAdminUser]
    http_method_names = ['get', 'post', 'head', 'options', 'delete', 'patch']

    def get_queryset(self):
        user: User = self.request.user
        if user.role == 'C':
            return Repair.objects.filter(car__user__username=user.username).all()
        return Repair.objects.all()
