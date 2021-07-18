from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from Auth.serializers import CarSerializer, MechanicSerializer, AdminSerializer, DriverSerializer, UserSerializer
from Auth.models import Car, Mechanic, Admin, Driver
from Auth.permissions import (IsMechanicReadOnlyPermission, IsCarReadOnlyPermission, IsAdminReadOnlyPermission,
                              IsReadOnlyAllRolePermission, IsAdminPermission)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    # HARDCODE
    def get(self, request: Request):
        if request.user.role == 'A':
            return Response(AdminSerializer(get_object_or_404(Admin, user__username=request.user.username)).data,
                            status=HTTP_200_OK)
        if request.user.role == 'C':
            return Response(CarSerializer(get_object_or_404(Car, user__username=request.user.username)).data,
                            status=HTTP_200_OK)
        if request.user.role == 'M':
            return Response(MechanicSerializer(get_object_or_404(Mechanic, user__username=request.user.username)).data,
                            status=HTTP_200_OK)
        if request.user.role == 'D':
            return Response(DriverSerializer(get_object_or_404(Driver, user__username=request.user.username)).data,
                            status=HTTP_200_OK)
        if request.user.is_staff:
            return Response(UserSerializer(request.user).data, status=HTTP_200_OK)


# GET - ADMIN, Mechanic, Car, POST - We, Admin, PATCH - Admin, DELETE - Admin
class CarViewSet(ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects \
        .annotate(count_requests=Count('requests_repairs', filter=Q(requests_repairs__completed=False))) \
        .order_by('-count_requests', 'mark', 'user__username')
    permission_classes = [IsMechanicReadOnlyPermission|IsCarReadOnlyPermission|IsAdminPermission|IsAdminUser]
    http_method_names = ['get', 'post', 'head', 'options', 'delete', 'patch']
    name_parameter = openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[name_parameter])
    @action(detail=False, methods=['GET'])
    def current(self, request):
        name = self.request.query_params.get('name')
        car: Car = get_object_or_404(Car, user__username=name)
        if car.user.company != self.request.user.company:
            raise PermissionDenied()
        return Response(CarSerializer(car).data, status=HTTP_200_OK)

    def get_queryset(self):
        return Car.objects\
            .filter(user__company=self.request.user.company)\
            .annotate(count_requests=Count('requests_repairs', filter=Q(requests_repairs__completed=False))) \
            .order_by('-count_requests', 'mark', 'user__username')


# GET - Admin, Mechanic, POST - Admin, PATCH - Admin, DELETE - Admin
class MechanicViewSet(ModelViewSet):
    serializer_class = MechanicSerializer
    queryset = Mechanic.objects.order_by('user__last_name')
    permission_classes = [IsAdminReadOnlyPermission|IsAdminPermission|IsAdminUser]
    http_method_names = ['get', 'post', 'head', 'options', 'delete', 'patch']
    name_parameter = openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[name_parameter])
    @action(detail=False, methods=['GET'])
    def current(self, request):
        name = self.request.query_params.get('name')
        mechanic: Mechanic = get_object_or_404(Mechanic, user__username=name)
        return Response(MechanicSerializer(mechanic).data, status=HTTP_200_OK)


# READONLY - ADMIN, others - us
class AdminViewSet(ModelViewSet):
    serializer_class = AdminSerializer
    queryset = Admin.objects.order_by('user__last_name')
    permission_classes = [IsAdminReadOnlyPermission|IsAdminUser]
    http_method_names = ['get', 'post', 'head', 'options', 'delete', 'patch']
    name_parameter = openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[name_parameter])
    @action(detail=False, methods=['GET'])
    def current(self, request):
        name = self.request.query_params.get('name')
        admin: Admin = get_object_or_404(Admin, user__username=name)
        return Response(AdminSerializer(admin).data, status=HTTP_200_OK)


# GET - Admin, Mechanic, Car, Driver. POST - Admin, PATCH - Admin, DELETE - Admin
class DriverViewSet(ModelViewSet):
    serializer_class = DriverSerializer
    queryset = Driver.objects.order_by('user__last_name')
    permission_classes = [IsReadOnlyAllRolePermission|IsAdminPermission|IsAdminUser]
    http_method_names = ['get', 'post', 'head', 'options', 'delete', 'patch']
    name_parameter = openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[name_parameter])
    @action(detail=False, methods=['GET'])
    def current(self, request):
        name = self.request.query_params.get('name')
        driver: Driver = get_object_or_404(Driver, user__username=name)
        return Response(DriverSerializer(driver).data, status=HTTP_200_OK)
