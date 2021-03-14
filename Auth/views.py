from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from Auth.serializers import CarSerializer, MechanicSerializer, AdminSerializer, DriverSerializer
from Auth.models import Car, Mechanic, Admin, Driver


class CarViewSet(ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    permission_classes = []
    name_parameter = openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[name_parameter])
    @action(detail=False, methods=['GET'])
    def current(self, request):
        name = self.request.query_params.get('name')
        car: Car = get_object_or_404(Car, user__username=name)
        return Response(CarSerializer(car).data, status=HTTP_200_OK)


class MechanicViewSet(ModelViewSet):
    serializer_class = MechanicSerializer
    queryset = Mechanic.objects.all()
    permission_classes = []
    name_parameter = openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[name_parameter])
    @action(detail=False, methods=['GET'])
    def current(self, request):
        name = self.request.query_params.get('name')
        mechanic: Mechanic = get_object_or_404(Mechanic, user__username=name)
        return Response(MechanicSerializer(mechanic).data, status=HTTP_200_OK)


class AdminViewSet(ModelViewSet):
    serializer_class = AdminSerializer
    queryset = Admin.objects.all()
    permission_classes = []
    name_parameter = openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[name_parameter])
    @action(detail=False, methods=['GET'])
    def current(self, request):
        name = self.request.query_params.get('name')
        admin: Admin = get_object_or_404(Admin, user__username=name)
        return Response(AdminSerializer(admin).data, status=HTTP_200_OK)


class DriverViewSet(ModelViewSet):
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()
    permission_classes = []
    name_parameter = openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[name_parameter])
    @action(detail=False, methods=['GET'])
    def current(self, request):
        name = self.request.query_params.get('name')
        driver: Driver = get_object_or_404(Driver, user__username=name)
        return Response(DriverSerializer(driver).data, status=HTTP_200_OK)
